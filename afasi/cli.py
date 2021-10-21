#! /usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""Commandline API gateway for afasi."""
import sys
from typing import List, Union

import typer

import afasi
import afasi.afasi as af

APP_NAME = 'Fuzz a language by mixing up only few words.'
APP_ALIAS = 'afasi'
app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)

TEMPLATE_EXAMPLE = """\
{
  "table": {
    "description": "table level default constraints, row attributes do replace those if present.",
    "contra": [
      "extracomment",
      "source"
    ],
    "count": 0,
    "flip_is_stop": true,
    "flip_flop": [
      "<message id=\\"SOME_TRACK\\">",
      "</message>"
    ],
    "pro": [
      "translation"
    ]
  },
  "foo": "bar",
  "translations": [
    {
      "repl": ">Lock",
      "ace": ">Launch"
    },
    {
      "repl": ">Track",
      "ace": ">Lock"
    },
    {
      "repl": ">Autotrack",
      "ace": ">Autolock"
    },
    {
      "repl": "lock r",
      "ace": "launch r"
    },
    {
      "repl": "track r",
      "ace": "lock r"
    }
  ]
}
"""


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

    The translation table entries are applied in order per line of input.
    So, with large translation tables the performance will obviously degrade with a power of two.
    The latter should be taken as a hint to maintain both language files in separate entities not as a patch task.

    The translation table is either an array of two element arrays provided as JSON and thus shall be in a shape like:

    \b
      [
        ["repl", "ace"],
        ["als", "othis"]
      ]

    Or the table is given as an object providing more detailed instructions constraining the translation rules like:

    \b
    * contra indicators - when given exempting a line from translation
    * pro indicators - when given marking a line for translation
    * flip_flop indicators - providing either stop-start (default) or start-stop state switching

    The JSON object format is best understood when executing the template command and adapting the resulting JSON
    object written to standard out.

    Default for input source is standard in and out per default is sent to standard out.
    """
    if version:
        typer.echo(f'{APP_NAME} version {afasi.__version__}')
        raise typer.Exit()


@app.command('template')
def app_template() -> int:
    """
    Write a template of a translation table JSON structure to standard out and exit
    """
    sys.stdout.write(TEMPLATE_EXAMPLE)
    return sys.exit(0)


@app.command('translate')
def translate(
    source: str = typer.Argument(af.STDIN),
    target: str = typer.Argument(af.STDOUT),
    inp: str = typer.Option(
        '',
        '-i',
        '--input',
        help='Path to input file (default is reading from standard in)',
        metavar='<sourcepath>',
    ),
    out: str = typer.Option(
        '',
        '-o',
        '--output',
        help='Path to non-existing output file (default is writing to standard out)',
        metavar='<targetpath>',
    ),
    translation_table_path: str = typer.Option(
        '',
        '-t',
        '--table',
        help=(
            'Path to translation table file in JSON format.'
            '\nStructure of table data is [["repl", "ace"], ["als", "othis"]]'
        ),
        metavar='<translation table path>',
    ),
    dry: bool = typer.Option(
        False,
        '-n',
        '--dryrun',
        help='Flag to execute without writing the translation but a diff instead (default is False)',
        metavar='bool',
    ),
) -> int:
    """
    Translate from a language to a 'langauge'.
    """
    command = 'translate'
    incoming = inp if inp else (source if source != af.STDIN else '')
    outgoing = out if out else (target if target != af.STDOUT else '')
    dryrun = 'DRYRUN' if dry else ''
    action = [command, incoming, outgoing, translation_table_path, dryrun]
    return sys.exit(af.main(action))


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
    return af.main(argv)
