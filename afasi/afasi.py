# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Fuzz a language by mixing up only few words. API."""
import json
import os
import pathlib
import sys
import warnings
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


def load_translation_table(path: pathlib.Path) -> Tuple[Tuple[str, str], ...]:
    """Load the translation table into a tuple of pairs."""
    if not path:
        return (('', ''),)

    with open(path, 'r', encoding=ENCODING) as handle:
        table = json.load(handle)

    if len(table) != 1:
        raise ValueError('translation table is not array of two element arrays')

    return tuple((str(repl), str(ace)) for repl, ace in table)


def main(argv: Union[List[str], None] = None) -> int:
    """Drive the translation."""
    # ['translate', inp, out]
    if not argv or len(argv) != 4:
        warnings.warn('received wrong number of arguments')
        return 2

    command, inp, translation_table_path, out = argv

    if command not in ('translate'):
        warnings.warn('received unknown command')
        return 2

    if inp:
        if not pathlib.Path(str(inp)).is_file():
            warnings.warn('source is no file')
            return 1

    if not translation_table_path:
        warnings.warn('translation table needed')
        return 1

    if not pathlib.Path(str(translation_table_path)).is_file():
        warnings.warn('translation table path is no file')
        return 1

    if out:
        if pathlib.Path(str(out)).is_file():
            warnings.warn('target file exists')
            return 1

    trans = load_translation_table(pathlib.Path(translation_table_path))
    print(trans)

    return 0
