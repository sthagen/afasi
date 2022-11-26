from typer.testing import CliRunner

import afasi
import afasi.cli as cli
from afasi.cli import app

runner = CliRunner()


def test_app_version():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert cli.APP_NAME in result.stdout
    assert afasi.__version__ in result.stdout


def test_app_template():
    result = runner.invoke(app, ['template'])
    assert result.exit_code == 0
    assert result.stdout == cli.TEMPLATE_EXAMPLE_YAML


def test_app_template_json():
    result = runner.invoke(app, ['template', '-f', 'jSoN'])
    assert result.exit_code == 0
    assert result.stdout == cli.TEMPLATE_EXAMPLE_JSON


def test_app_translate():
    result = runner.invoke(app, ['translate'])
    assert result.exit_code == 1
