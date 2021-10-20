# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
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


def test_app_translate():
    result = runner.invoke(app, ['translate'])
    assert result.exit_code == 1


def test_cli_main(capsys):
    message = 'received wrong number of arguments'
    cli.main(['translate', 'no_file_there']) == 1
    captured = capsys.readouterr()
    assert message in captured.err
