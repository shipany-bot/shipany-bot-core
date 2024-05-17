{ pkgs, lib, config, inputs, ... }:

{
  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  enterShell = ''
    uv pip install -r requirements.txt -r dev-requirements.txt -e .
  '';

  scripts.compile.exec = ''
    uv pip compile $1.in -o $1.txt -q
  '';

  scripts.install.exec = ''
    uv pip install -r $1.txt
  '';

  scripts.run-tests.exec = ''
    coverage run -m pytest
    coverage xml
  '';

  scripts.print-report.exec = ''
    coverage report
  '';

  scripts.run-bot.exec = ''
    shipany-bot-cli run $1
  '';

  scripts.tag-build.exec = ''
    git tag $1
    version=$(shipany-bot-cli version)
    if [ "$version" != "$1" ]; then
      echo Commit changes first
      git tag --delete $1
      exit 1
    fi
    mkdir -p schemata/$version
    shipany-bot-cli schema > schemata/$version/schema.json
  '';

  enterTest = ''
  '';

  dotenv.enable = true;
  languages.python = {
    enable = true;
    version = "3.11.4";
    venv = {
      enable = true;
    };
    uv = {
      enable = true;
    };
  };
}
