{ pkgs ? import <nixpkgs> { } }:
with pkgs;
mkShell {
  buildInputs = with python311Packages;[
    python3
    astroid
    black
    click
    dill
    isort
    mccabe
    mypy-extensions
    packaging
    pathspec
    platformdirs
    pylint
    tkinter
    tomlkit
    imageio
  ];
}

