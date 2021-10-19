# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Fuzz a language by mixing up only few words. API."""
import os
import pathlib
import warnings
from typing import List, Union

DEBUG_VAR = 'AFASI_DEBUG'
DEBUG = os.getenv(DEBUG_VAR)

ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'

STDIN, STDOUT = 'STDIN', 'STDOUT'
DISPATCH = {
  STDIN: sys.stdin,
  STDOUT: sys.stdout,
}


def main(argv: Union[List[str], None] = None) -> int:
    """Drive the translation."""
    # ['translate', inp, out]
    if not argv or len(argv) != 3:
        warnings.warn('received wrong number of arguments')
        return 2

    if argv[0] not in ('translate'):
        warnings.warn('received unknown command')
        return 2

    command, inp, out = argv[0]
    if inp:
        if not pathlib.Path(str(inp)).is_file():
            warnings.warn('source is no file')
            return 1

    if out:
        if pathlib.Path(str(out)).is_file():
            warnings.warn('target file exists')
            return 1

    return 0
