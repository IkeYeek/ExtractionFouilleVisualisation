{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
          python313
          python313Packages.pandas
          python313Packages.matplotlib
          python313Packages.plotly
          python313Packages.dash
          python313Packages.numpy
          python313Packages.shapely

          python313Packages.openpyxl

          libreoffice
        ];
      };
    }
  );
}
