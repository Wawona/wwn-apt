# apt-common.sh — shared helpers for Wawona App Store module CLI

APT_VERSION="1.0.0"
APT_SHARE_REL="usr/share/wawona/apt"
APT_MODULES_DIR="${HOME}/Library/Application Support/Wawona/modules"
APT_INSTALLED_JSON="${APT_MODULES_DIR}/installed.json"
APT_MODULE_SOCK="${HOME}/Library/Application Support/Wawona/module-manager.sock"

apt_rootfs_base() {
	if [ -n "${WAWONA_ROOTFS:-}" ] && [ -d "${WAWONA_ROOTFS}/${APT_SHARE_REL}" ]; then
		printf '%s\n' "${WAWONA_ROOTFS}"
		return 0
	fi
	if [ -n "${WAWONA_BUNDLE_ROOTFS:-}" ] && [ -d "${WAWONA_BUNDLE_ROOTFS}/${APT_SHARE_REL}" ]; then
		printf '%s\n' "${WAWONA_BUNDLE_ROOTFS}"
		return 0
	fi
	return 1
}

apt_share_dir() {
	base="$(apt_rootfs_base)" || return 1
	printf '%s/%s\n' "$base" "$APT_SHARE_REL"
}

apt_load_catalog() {
	share="$(apt_share_dir)" || {
		echo "apt: module catalog not found (is Wawona rootfs installed?)" >&2
		return 1
	}
	APT_JSONL="${share}/modules.jsonl"
	APT_CATALOG_JSON="${share}/catalog.json"
	APT_BUNDLED_JSON="${share}/bundled.json"
	if [ ! -f "$APT_JSONL" ]; then
		echo "apt: modules.jsonl missing under ${share}" >&2
		return 1
	fi
	export APT_JSONL APT_CATALOG_JSON APT_BUNDLED_JSON
}

apt_about_text() {
	cat <<'EOF'
Wawona apt — App Store module compatibility layer

The apt command lists, installs, and removes Wawona modules that have been
reviewed and approved for distribution through the App Store. It is not a
general-purpose package manager.

  apt search [pattern]   List approved modules in the embedded catalog
  apt install <module>   Install an optional module (StoreKit + ODR)
  apt remove <module>    Remove an optional module you installed

Required software (zsh, coreutils, waypipe, apt) is always bundled and cannot
be installed or removed through this command.
  apt list [--installed] Show catalog entries or installed modules
  apt show <module>      Display module metadata

Modules are acquired only through Apple-approved mechanisms (StoreKit and
App Store-hosted On-Demand Resources). Users cannot add third-party
repositories or install user-supplied binaries.
EOF
}

apt_usage() {
	cat <<'EOF'
Usage: apt [--about] <command> [arguments]

Commands:
  search [pattern]     Search the approved module catalog
  install <module>       Install an approved module (StoreKit + ODR)
  remove <module>        Remove a locally installed module
  list [--installed]     List catalog or installed modules
  show <module>          Show module details
  help                   Show this help

Unsupported (by design):
  edit-sources, add-repository, update, upgrade, dist-upgrade

Exit codes: 0 success, 1 usage/policy error, 2 module manager unavailable,
           3 module not found, 4 dependency/conflict error
EOF
}

apt_reject_repo_commands() {
	echo "apt: third-party package repositories are not supported in Wawona." >&2
	echo "apt: only modules from the embedded App Store catalog may be installed." >&2
	return 1
}

apt_json_field() {
	line="$1"
	field="$2"
	echo "$line" | sed -n "s/.*\"${field}\":\"\\([^\"]*\\)\".*/\\1/p" | head -n 1
}

apt_each_module() {
	while IFS= read -r line || [ -n "$line" ]; do
		[ -n "$line" ] || continue
		echo "$line"
	done < "$APT_JSONL"
}

apt_find_module_line() {
	want="$1"
	apt_each_module | while IFS= read -r line; do
		id="$(apt_json_field "$line" id)"
		if [ "$id" = "$want" ]; then
			echo "$line"
			break
		fi
	done
}

apt_module_installed() {
	id="$1"
	[ -f "$APT_INSTALLED_JSON" ] || return 1
	grep -q "\"${id}\"" "$APT_INSTALLED_JSON" 2>/dev/null
}

apt_try_module_manager() {
	if [ -n "${WAWONA_MODULE_MANAGER:-}" ] && [ -S "$APT_MODULE_SOCK" ]; then
		return 0
	fi
	return 1
}

apt_module_manager_unavailable() {
	echo "apt: module manager is not available." >&2
	echo "apt: use Wawona Settings to install approved modules, or update the app when module support is enabled." >&2
}

apt_is_bundled_required() {
	id="$1"
	# Fallback when bundled.json is not yet embedded.
	case "$id" in
	zsh|coreutils|waypipe|apt) return 0 ;;
	esac
	if [ ! -f "${APT_BUNDLED_JSON:-}" ]; then
		return 1
	fi
	grep -q "\"id\":\"${id}\"" "$APT_BUNDLED_JSON" 2>/dev/null
}

apt_reject_bundled_mutation() {
	id="$1"
	action="$2"
	echo "apt: '${id}' is required bundled software and is always included in Wawona." >&2
	echo "apt: it cannot be ${action} via apt." >&2
	return 4
}

apt_search_match() {
	pattern="$1"
	id="$2"
	name="$3"
	desc="$4"
	[ -z "$pattern" ] && return 0
	echo "$id $name $desc" | grep -qi "$pattern"
}
