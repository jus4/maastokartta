# # shell.nix
# let
#   # We pin to a specific nixpkgs commit for reproducibility.
#   # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
#   pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/cf8cc1201be8bc71b7cbbbdaf349b22f4f99c7ae.tar.gz") {};
# in pkgs.mkShell {
#   packages = [
#     (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
#       flask
#       gunicorn
#       pyproj
#       requests
#       pip
#     ]))
#
#   ];
#
#   # Set environment variables to help the build process
#   C_INCLUDE_PATH = pkgs.lib.makeSearchPathOutput "dev" "include" [ pkgs.libxml2 pkgs.libxslt ];
#   LIBRARY_PATH = pkgs.lib.makeLibraryPath [ pkgs.libxml2 pkgs.libxslt pkgs.zlib ];
# }


{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShell {
  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.python3Packages.virtualenv
    pkgs.gcc
  ];
  shellHook = ''
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
  '';
}
