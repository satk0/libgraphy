{
    pkgs,
    ...
}:
let
  tex = pkgs.texlive.combine
    { inherit (pkgs.texlive) scheme-basic type1cm cm-super underscore
    babel-polish;
    };
  python = pkgs.python312;
  # https://github.com/NixOS/nixpkgs/blob/c339c066b893e5683830ba870b1ccd3bbea88ece/nixos/modules/programs/nix-ld.nix#L44
  # > We currently take all libraries from systemd and nix as the default.
  pythonldlibpath = pkgs.lib.makeLibraryPath (with pkgs; [
    zlib
    zstd
    stdenv.cc.cc
    curl
    openssl
    attr
    libssh
    bzip2
    libxml2
    acl
    libsodium
    util-linux
    xz
    systemd

# PyQT:
# https://stackoverflow.com/a/79242721
    glib
    libGL
    fontconfig
    xorg.libX11
    libxkbcommon
    freetype
    dbus
    xorg.libxcb
    xorg.xcbutilwm
    xorg.xcbutilimage
    xorg.xcbutilkeysyms
    xorg.xcbutilrenderutil
    xcb-util-cursor
  ]);

  patchedpython = (python.overrideAttrs (
    previousAttrs: {
      # Add the nix-ld libraries to the LD_LIBRARY_PATH.
      # creating a new library path from all desired libraries
      postInstall = previousAttrs.postInstall + ''
        mv  "$out/bin/python3.12" "$out/bin/unpatched_python3.12"
        cat << EOF >> "$out/bin/python3.12"
        #!/run/current-system/sw/bin/bash
        export LD_LIBRARY_PATH="${pythonldlibpath}"
        exec "$out/bin/unpatched_python3.12" "\$@"
        EOF
        chmod +x "$out/bin/python3.12"
      '';
    }
  ));
  # if you want poetry
  patchedpoetry =  (
  (pkgs.poetry.override { python3 = patchedpython; }).overrideAttrs (
    previousAttrs: {
      # same as above, but for poetry
      # not that if you dont keep the blank line bellow, it crashes :(
      postInstall = previousAttrs.postInstall + ''

        mv "$out/bin/poetry" "$out/bin/unpatched_poetry"
        cat << EOF >> "$out/bin/poetry"
        #!/run/current-system/sw/bin/bash
        export LD_LIBRARY_PATH="${pythonldlibpath}"
        exec "$out/bin/unpatched_poetry" "\$@"
        EOF
        chmod +x "$out/bin/poetry"
      '';
    }
  ));
in
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      makeWrapper
      bashInteractive
    ];

    #NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath ([
    #  patchedpython
    #  patchedpoetry
    #]);

    NIX_LD = pkgs.lib.fileContents "${pkgs.stdenv.cc}/nix-support/dynamic-linker";

    buildInputs = with pkgs; [
      tex
      patchedpython
      patchedpoetry

      graphviz

      pyright
    ];

    sourceRoot = ".";

    shellHook = ''
      echo "Hello from shell!"
    '';
  }
