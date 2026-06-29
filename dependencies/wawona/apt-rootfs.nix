# apt-rootfs — prefix tree with apt CLI and embedded module catalog (App Store).
{
  lib,
  pkgs,
  catalogJson,
  modulesJsonl,
}:

pkgs.runCommand "wawona-apt-rootfs" {
  passthru = {
    inherit catalogJson modulesJsonl;
  };
} ''
  mkdir -p $out/usr/bin $out/usr/share/wawona/apt $out/usr/lib/wawona/apt $out/usr/share/man/man8

  cp ${../../apt/bin/apt} $out/usr/bin/apt
  chmod +x $out/usr/bin/apt

  cp ${../../apt/lib/apt-common.sh} $out/usr/lib/wawona/apt/apt-common.sh

  cp ${catalogJson} $out/usr/share/wawona/apt/catalog.json
  cp ${modulesJsonl} $out/usr/share/wawona/apt/modules.jsonl

  cp ${../../apt/share/man/man8/apt.8} $out/usr/share/man/man8/apt.8
''
