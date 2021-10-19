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


def main(argv: Union[List[str], None] = None) -> int:
    """Drive the translation."""
    # ['translate', source]
    if not argv or len(argv) < 1:
        warnings.warn('received wrong number of arguments')
        return 2

    if argv[0] not in ('translate'):
        warnings.warn('received unknown command')
        return 2

    command = argv[0]
    if len(argv) > 1:
        source = arv[1]
        if not pathlib.Path(str(source)).is_file():
            warnings.warn('source is no file')
            return 1

    return 0
