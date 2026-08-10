{
  description = "Demonstrating the use of Docling to add semantic structure";

  inputs = {
    # Current nixpkgs for ordinary development tools
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    flake-utils.url = "github:numtide/flake-utils";

    # Historical nixpkgs containing the pdfcpu version you want
    nixpkgs-pdfcpu.url =
      "github:NixOS/nixpkgs/a0d7b28e3046186f34faf2c257603ddfb3be223a";

    # The commit that updated python311 to exactly Python 3.11.2
    nixpkgs-python3112.url =
      "github:NixOS/nixpkgs/f0b8e02958c5bec7aff2da38d62e9de7a673a49b";
  };

  outputs =
    {
      self,
      nixpkgs,
      nixpkgs-pdfcpu,
      nixpkgs-python3112,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        pdfcpuPkgs = nixpkgs-pdfcpu.legacyPackages.${system};

        python3112Pkgs =
          nixpkgs-python3112.legacyPackages.${system};

        python = python3112Pkgs.python311;
      in
      {
        devShells.default = pkgs.mkShell {
          packages = [
            python
            pkgs.uv
            pdfcpuPkgs.pdfcpu
            pkgs.git
          ];

          shellHook = ''
            # Force uv to use the Python supplied by Nix.
            export UV_PYTHON="${python}/bin/python3.11"

            # Don't let uv silently download another Python.
            export UV_PYTHON_DOWNLOADS=never

            echo "Development environment activated"
            echo "Python: $(python --version)"
            echo "pdfcpu: $(pdfcpu version 2>/dev/null | head -n 1)"
          '';
        };
      }
    );
}
