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


def test_app_template():
    result = runner.invoke(app, ['template'])
    assert result.exit_code == 0
    assert result.stdout == cli.TEMPLATE_EXAMPLE


def test_app_translate():
    result = runner.invoke(app, ['translate'])
    assert result.exit_code == 1
