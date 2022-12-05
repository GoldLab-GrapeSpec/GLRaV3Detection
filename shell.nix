# with import <nixpkgs> { config = {
#   packageOverrides = pkgs: {
#     uwsgi = pkgs.uwsgi.override { xlibs = null; }; # how to make this enable pcre?
#   };
# };};
with import <nixpkgs> {};
with pkgs.python37Packages;
stdenv.mkDerivation {
  name = "impurePythonEnv";
  buildInputs = [
    # protobuf  # remove protobuf from shell.nix due to version conflicts

    # these packages are required for virtualenv and pip to work:
    #
    mypy
    python37Full
    python37Packages.virtualenv
    
    python37Packages.numpy

    # for running tests
    python37Packages.nose2
  ];
  src = null;
  # TODO: convert to full nix expression so as to not rely on pip
  shellHook = ''
    # set SOURCE_DATE_EPOCH so that we can use python wheels
    SOURCE_DATE_EPOCH=$(date +%s)
    export LANG=en_US.UTF-8
    virtualenv venv
    source venv/bin/activate
    export PATH=$PWD/venv/bin:$PATH
    export PYTHONPATH=$PWD:$PYTHONPATH
    pip install openpyxl xlrd
    pip install -e .
  '';
}
