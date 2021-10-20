# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Fuzz a language by mixing up only few words. API."""
import json
import os
import pathlib
import sys
from json.decoder import JSONDecodeError
from typing import List, Tuple, Union

DEBUG_VAR = 'AFASI_DEBUG'
DEBUG = os.getenv(DEBUG_VAR)

ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'

STDIN, STDOUT = 'STDIN', 'STDOUT'
DISPATCH = {
    STDIN: sys.stdin,
    STDOUT: sys.stdout,
}


def filter_table(pairs: List[Tuple[str, str]]) -> Tuple[Tuple[str, str], ...]:
    """Filter same -> same and redundant repl -> ace from redundant table of pairs."""
    table = []
    for repl, ace in pairs:
        s_repl, s_ace = str(repl), str(ace)
        if s_repl != s_ace:
            pair = (s_repl, s_ace)
            if pair not in table:
                table.append(pair)

    return tuple(table)


def load_translation_table(path: pathlib.Path) -> Tuple[Tuple[str, str], ...]:
    """Load the translation table into a tuple of unique non-idempotent pairs."""
    if not path:
        raise ValueError('translation table path not given')

    if not path.is_file():
        raise ValueError('translation table path must lead to a file')

    with open(path, 'r', encoding=ENCODING) as handle:
        try:
            table = json.load(handle)
        except JSONDecodeError:
            raise ValueError('translation table path must lead to a JSON file')

    if not table:
        raise ValueError('translation table is empty')

    if any(len(entry) != 2 for entry in table):
        raise ValueError('translation table is not array of two element arrays')

    return filter_table([(repl, ace) for repl, ace in table])


def report_request(trans: Tuple[Tuple[str, str], ...]) -> List[str]:
    """Generate report of request per list of lines."""
    report = ['using these translations (in order):']
    repl_col_width = max(len(repl) for repl, _ in trans) + 2
    for rank, (repl, ace) in enumerate(trans, start=1):
        lim_repl = "'" if "'" not in repl else ''
        lim_ace = "'" if "'" not in ace else ''
        repl_cell = f'{lim_repl}{repl}{lim_repl}'.ljust(repl_col_width)
        report.append(f' {rank:>2d}. {repl_cell} -> {lim_ace}{ace}{lim_ace}')

    return report + ['']


def main(argv: Union[List[str], None] = None) -> int:
    """Drive the translation."""
    # ['translate', inp, out]
    if not argv or len(argv) != 5:
        print('received wrong number of arguments')
        return 2

    command, inp, out, translation_table_path, dryrun = argv

    if command not in ('translate'):
        print('received unknown command')
        return 2

    if inp:
        if not pathlib.Path(str(inp)).is_file():
            print('source is no file')
            return 1

    if out:
        if pathlib.Path(str(out)).is_file():
            print('target file exists')
            return 1

    try:
        trans = load_translation_table(pathlib.Path(translation_table_path))
    except ValueError as err:
        print(err)
        return 1

    if dryrun:
        print('dryrun requested')
        return 0

    print('\n'.join(report_request(trans)))
    print(' ... later')

    return 0
