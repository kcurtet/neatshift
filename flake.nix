{
  description = "Organizador de Archivos - GUI multiplataforma para organizar archivos";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        # Development shell usando el shell.nix existente
        devShells.default = import ./shell.nix { inherit pkgs; };

        # Alias para compatibilidad
        devShell = self.devShells.${system}.default;

        # Metadata del proyecto
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "organizador-archivos";
          version = "1.0.0";
          src = ./.;
          
          meta = with pkgs.lib; {
            description = "Organizador de archivos con GUI multiplataforma usando Flet";
            homepage = "https://github.com/kcurtet/file-organizer";
            license = licenses.mit;
            platforms = platforms.all;
            maintainers = [ ];
          };
        };
      }
    );
}
