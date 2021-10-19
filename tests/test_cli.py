# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pytest
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
    result = runner.invoke(app, ['translate'])
    assert result.exit_code == 0
    assert not result.stdout


def test_cli_main():
    message = 'no input found'
    with pytest.raises(UserWarning) as ex:
        cli.main(['translate', 'no_file_there']) == 1
        assert message in str(ex.value)
