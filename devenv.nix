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
    shipany-bot-worker
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
