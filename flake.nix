{
  description = "wwn-apt: App Store module catalog, apt CLI stub, ODR+StoreKit integration spec.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    rust-overlay.url = "github:oxalica/rust-overlay";
    rust-overlay.inputs.nixpkgs.follows = "nixpkgs";
    wwn-toolchain.url = "github:Wawona/wwn-toolchain";
    wwn-toolchain.inputs.nixpkgs.follows = "nixpkgs";
    wwn-toolchain.inputs.rust-overlay.follows = "rust-overlay";
  };

  outputs = { self, nixpkgs, rust-overlay, wwn-toolchain, ... }:
    let
      darwinSystems = [ "x86_64-darwin" "aarch64-darwin" ];
      linuxSystems = [ "x86_64-linux" "aarch64-linux" ];
      allSystems = darwinSystems ++ linuxSystems;
      forAll = nixpkgs.lib.genAttrs allSystems;
      inherit (wwn-toolchain.lib) withPlatformVariants;

      pkgsFor = system: import nixpkgs {
        inherit system;
        overlays = [ (import rust-overlay) ];
        config = { allowUnfree = true; allowUnsupportedSystem = true; };
      };

      catalogBundle = pkgs: pkgs.runCommand "wawona-apt-catalog" {
        nativeBuildInputs = [ pkgs.python3 pkgs.python3Packages.pyyaml ];
      } '' 
        ${pkgs.python3}/bin/python3 ${./scripts/generate-catalog-json.py} \
          ${./catalog/modules} --bundled ${./catalog/bundled.yaml} -o $out
      '';

      aptRootfsFor = pkgs:
        pkgs.callPackage ./dependencies/wawona/apt-rootfs.nix {
          catalogJson = "${catalogBundle pkgs}/catalog.json";
          modulesJsonl = "${catalogBundle pkgs}/modules.jsonl";
          bundledJson = "${catalogBundle pkgs}/bundled.json";
        };
    in
    {
      registryFragment = {
        apt-rootfs = withPlatformVariants {
          android = null;
          ios = ./dependencies/wawona/apt-rootfs.nix;
          ipados = ./dependencies/wawona/apt-rootfs.nix;
          tvos = ./dependencies/wawona/apt-rootfs.nix;
          visionos = ./dependencies/wawona/apt-rootfs.nix;
          watchos = ./dependencies/wawona/apt-rootfs.nix;
          macos = null;
          wearos = null;
        };
      };

      packages = forAll (system:
        let pkgs = pkgsFor system;
        in {
          catalog-json = catalogBundle pkgs;
          apt-rootfs-ios = aptRootfsFor pkgs;
        });

      formatter = forAll (system: (pkgsFor system).nixfmt-rfc-style);
    };
}
