#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for afasi."""
import pathlib
import sys
from typing import List, Union

import typer

import afasi
import afasi.kysy as af

STDIN, STDOUT = 'STDIN', 'STDOUT'
DISPATCH = {
  STDIN: sys.stdin,
  STDOUT: sys.stdout,
}

APP_NAME = 'Fuzz a language by mixing up only few words.'
APP_ALIAS = 'afasi'
app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the afasi version and exit',
        is_eager=True,
    )
) -> None:
    """
    Fuzz a language by mixing up only few words.
    """
    if version:
        typer.echo(f'{APP_NAME} version {afasi.__version__}')
        raise typer.Exit()


@app.command('translate')
def translate(
    source: str = typer.Argument(STDIN),
    target: str = typer.Argument(STDOUT),
    inp: str = typer.Option('', '-i', '--input'),
    out: str = typer.Option('', '-o', '--output'),
) -> int:
    """
    Translate from a language to a 'langauge'.
    """
    incoming = inp if inp else (source if source != STDIN else '')
    outgoing = out if out else (target if target != STDOUT else '')
    action = ['translate', incoming, outgoing]
    return af.main(action)


@app.command('version')
def app_version() -> None:
    """
    Display the afasi version and exit
    """
    callback(True)


# pylint: disable=expression-not-assigned
# @app.command()
def main(argv: Union[List[str], None] = None) -> int:
    """Delegate processing to functional module."""
    argv = sys.argv[1:] if argv is None else argv
    return ky.main(argv)
