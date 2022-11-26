# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Fuzz a language by mixing up only few words. API."""
import difflib
import json
import pathlib
import sys
import typing
from json.decoder import JSONDecodeError
from typing import Iterator

import yaml

import afasi.tabel as tb
from afasi import ENCODING, log

STDIN, STDOUT = 'STDIN', 'STDOUT'
DISPATCH = {
    STDIN: sys.stdin,
    STDOUT: sys.stdout,
}


def filter_table(pairs: list[tuple[str, str]]) -> tuple[tuple[str, str], ...]:
    """Filter same -> same and redundant repl -> ace from redundant table of pairs."""
    table = []
    for repl, ace in pairs:
        s_repl, s_ace = str(repl), str(ace)
        if s_repl != s_ace:
            pair = (s_repl, s_ace)
            if pair not in table:
                table.append(pair)

    return tuple(table)


def load_translation_table(path: pathlib.Path) -> tuple[tuple[str, str], ...]:
    """Load the translation table into a tuple of unique non-idempotent pairs."""
    if not path:
        raise ValueError('translation table path not given')

    if not path.is_file():
        raise ValueError('translation table path must lead to a file')

    suffix = path.suffix.lower()
    if suffix not in ('.json', '.yaml', '.yml'):
        raise ValueError('translation table path must have a .json, yaml, or .yml suffix')
    elif suffix == '.json':
        with open(path, 'r', encoding=ENCODING) as handle:
            try:
                table = json.load(handle)
            except JSONDecodeError:
                raise ValueError('translation table path must lead to a JSON file')
    else:
        with open(path, 'r', encoding=ENCODING) as handle:
            try:
                table = yaml.safe_load(handle)
            except yaml.YAMLError:
                raise ValueError('translation table path must lead to a YAML file')

    if not table:
        raise ValueError('translation table is empty')

    if any(len(entry) != 2 for entry in table):
        raise ValueError('translation table is not array of two element arrays')

    return filter_table([(repl, ace) for repl, ace in table])


def report_request(trans: tuple[tuple[str, str], ...]) -> list[str]:
    """Generate report of request per list of lines."""
    report = ['* translations (in order):']
    repl_col_width = max(len(repl) for repl, _ in trans) + 1
    for rank, (repl, ace) in enumerate(trans, start=1):
        lim_repl = "'" if "'" not in repl else ''
        lim_ace = "'" if "'" not in ace else ''
        repl_cell = f'{lim_repl}{repl}{lim_repl}'.ljust(repl_col_width)
        report.append(f' {rank:>2d}. {repl_cell} -> {lim_ace}{ace}{lim_ace}')

    return report + ['']


def replace(trans: tuple[tuple[str, str], ...], text: str) -> str:
    """Naive replacer."""
    for repl, ace in trans:
        text = text.replace(repl, ace)
    return text


def reader(path: str) -> Iterator[str]:
    """Context wrapper / generator to read the lines."""
    with open(pathlib.Path(path), 'rt', encoding=ENCODING) as handle:
        for line in handle:
            yield line


def verify_request(argv: list[str] | None) -> tuple[int, str, list[str]]:
    """Gail with grace."""
    if not argv or len(argv) != 5:
        return 2, 'received wrong number of arguments', ['']

    command, inp, out, translation_table_path, dryrun = argv

    if command not in ('translate',):
        return 2, 'received unknown command', ['']

    if inp:
        if not pathlib.Path(str(inp)).is_file():
            return 1, 'source is no file', ['']

    if out:
        if pathlib.Path(str(out)).is_file():
            return 1, 'target file exists', ['']

    return 0, '', argv


@typing.no_type_check
def speculative_table_loader(path: pathlib.Path):
    """Try loading table data as pod or as object."""
    try:
        return True, load_translation_table(path)
    except ValueError:
        pass

    try:
        return False, tb.load_table(path)
    except (IsADirectoryError, ValueError):
        pass

    log.warning('neither plain old parallel array nor object table data given')
    return True, (tuple(),)


def main(argv: list[str] | None = None) -> int:
    """Drive the translation."""
    error, message, strings = verify_request(argv)
    if error:
        log.error(message)
        return error

    command, inp, out, translation_table_path, dryrun = strings

    is_pod, meta = speculative_table_loader(pathlib.Path(translation_table_path))
    if is_pod and not meta[0]:
        return 1

    source = sys.stdin if not inp else reader(inp)
    if dryrun:
        log.info('dryrun requested\n# ---')
        log.info('* resources used:')
        inp_disp = 'STDIN' if not inp else f'"{inp}"'
        out_disp = 'STDOUT' if not out else f'"{out}"'
        log.info(f'  - input from:       {inp_disp}')
        log.info(f'  - output to:        {out_disp}')
        log.info(f'  - translation from: "{translation_table_path}"')
        if is_pod:
            log.info('\n'.join(report_request(meta)))
        else:
            log.info(f'* {meta}')
        src, tgt = [], []
        for line in source:
            src.append(line)
            if is_pod:
                tgt.append(replace(meta, line))
            else:
                tgt.append(meta.translate(line))
        log.info('* diff of source to target:')
        log.info(''.join(line for line in difflib.unified_diff(src, tgt, fromfile='SOURCE', tofile='TARGET')).strip())
        log.info('# ---')
    else:
        if out:
            with open(pathlib.Path(out), 'wt', encoding=ENCODING) as target:
                for line in source:
                    if is_pod:
                        target.write(replace(meta, line))
                    else:
                        target.write(meta.translate(line))
        else:
            for line in source:
                if is_pod:
                    sys.stdout.write(replace(meta, line))
                else:
                    sys.stdout.write(meta.translate(line))

    return 0
