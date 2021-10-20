# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Fuzz a language by mixing up only few words. API."""
import difflib
import json
import os
import pathlib
import sys
from json.decoder import JSONDecodeError
from typing import Iterator, List, Optional, Tuple, Union

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
    report = ['* translations (in order):']
    repl_col_width = max(len(repl) for repl, _ in trans) + 1
    for rank, (repl, ace) in enumerate(trans, start=1):
        lim_repl = "'" if "'" not in repl else ''
        lim_ace = "'" if "'" not in ace else ''
        repl_cell = f'{lim_repl}{repl}{lim_repl}'.ljust(repl_col_width)
        report.append(f' {rank:>2d}. {repl_cell} -> {lim_ace}{ace}{lim_ace}')

    return report + ['']


def replace(trans: Tuple[Tuple[str, str], ...], text: str) -> str:
    """Naive replacer."""
    for repl, ace in trans:
        text = text.replace(repl, ace)
    return text


def reader(path: str) -> Iterator[str]:
    """Context wrapper / generator to read the lines."""
    with open(pathlib.Path(path), 'rt', encoding=ENCODING) as handle:
        for line in handle:
            yield line


def verify_request(argv: Optional[List[str]]) -> Tuple[int, str, List[str]]:
    """Gail with grace."""
    if not argv or len(argv) != 5:
        return 2, 'received wrong number of arguments', ['']

    command, inp, out, translation_table_path, dryrun = argv

    if command not in ('translate'):
        return 2, 'received unknown command', ['']

    if inp:
        if not pathlib.Path(str(inp)).is_file():
            return 1, 'source is no file', ['']

    if out:
        if pathlib.Path(str(out)).is_file():
            return 1, 'target file exists', ['']

    return 0, '', argv


def main(argv: Union[List[str], None] = None) -> int:
    """Drive the translation."""
    error, message, strings = verify_request(argv)
    if error:
        print(message, file=sys.stderr)
        return error

    command, inp, out, translation_table_path, dryrun = strings

    try:
        trans = load_translation_table(pathlib.Path(translation_table_path))
    except ValueError as err:
        print(err, file=sys.stderr)
        return 1

    source = sys.stdin if not inp else reader(inp)
    if dryrun:
        print('dryrun requested\n# ---', file=sys.stderr)
        print('* resources used:', file=sys.stderr)
        inp_disp = "STDIN" if not inp else f'"{inp}"'
        out_disp = "STDOUT" if not out else f'"{out}"'
        print(f'  - input from:       {inp_disp}', file=sys.stderr)
        print(f'  - output to:        {out_disp}', file=sys.stderr)
        print(f'  - translation from: "{translation_table_path}"', file=sys.stderr)
        print('\n'.join(report_request(trans)), end='', file=sys.stderr)
        src, tgt = [], []
        for line in source:
            src.append(line)
            tgt.append(replace(trans, line))
        print('* diff of source to target:')
        print(''.join(line for line in difflib.unified_diff(src, tgt, fromfile='SOURCE', tofile='TARGET')).strip())
        print('# ---')
    else:
        if out:
            with open(pathlib.Path(out), 'wt', encoding=ENCODING) as target:
                for line in source:
                    target.write(replace(trans, line))
        else:
            for line in source:
                sys.stdout.write(replace(trans, line))

    return 0
