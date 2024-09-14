{
  description = "Libgraphy for Nix";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
    let
      # Helper to provide system-specific attributes
      pkgs = import nixpkgs { inherit system; };

    in {
        devShells.default = pkgs.callPackage ./dev.nix {inherit pkgs; };
    }
  );
}


