{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.gcc
    pkgs.uv
    pkgs.flutter
    
    # GTK dependencies for Flet on Linux
    pkgs.gtk3
    pkgs.pango
    pkgs.cairo
    pkgs.glib
    pkgs.gdk-pixbuf
    pkgs.harfbuzz
    pkgs.atk
    pkgs.libsecret
    pkgs.libepoxy
    pkgs.fontconfig
  ];
  
  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.gtk3}/lib:${pkgs.pango.out}/lib:${pkgs.cairo}/lib:${pkgs.glib.out}/lib:${pkgs.gdk-pixbuf}/lib:${pkgs.harfbuzz}/lib:${pkgs.atk}/lib:${pkgs.libsecret}/lib:${pkgs.libepoxy}/lib:${pkgs.fontconfig.lib}/lib:$LD_LIBRARY_PATH
    export FLUTTER_ROOT=${pkgs.flutter.out}
  '';
}
