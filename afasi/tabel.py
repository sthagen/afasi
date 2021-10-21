# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Tabel (Danish for Table). Class API."""
import json
import pathlib
import typing

ENCODING = 'utf-8'


class Table:
    """Translation table."""

    __slots__ = ['description', 'contra', 'count', 'flip_is_stop', 'flip_flop', 'pro', 'translations']

    @typing.no_type_check
    def __init__(self, **kwargs):
        """Instance created from dictionary usually stored in a JSON file."""
        for key, value in kwargs.items():
            if key == 'table':
                for me, ta in value.items():
                    setattr(self, me, ta)
            elif key == 'translations':
                setattr(self, key, [])
                for entry in value:
                    self.translations.append(Translation(**entry))
            else:
                print(f'table ignored ({key=} -> {value=})')

    @typing.no_type_check
    def translate(self, text: str) -> str:
        """Sequenced replacer (WIP)."""
        for rule in self.translations:
            text = text.replace(rule.repl, rule.ace)
        return text

    @typing.no_type_check
    def __str__(self):
        """Human readable rendition esp. for debugging."""
        ff = "'" + "'\n    '".join(switch for switch in self.flip_flop) + "'"
        return (
            f'table:\n  {self.description=}\n'
            f'  {self.contra=}\n'
            f'  {self.count=}\n'
            f'  {self.flip_is_stop=}\n'
            f'  flip_flop:\n    {ff}\n'
            f'  {self.count=}\n'
            f'  {self.pro=}\n'
            f'  translations:\n    {"    ".join(str(translation) for translation in self.translations)}\n'
        )


class Translation:
    """Translation task."""

    __slots__ = ['repl', 'ace']

    @typing.no_type_check
    def __init__(self, **kwargs):
        """Instance created from dictionary."""
        for key, value in kwargs.items():
            setattr(self, key, value)

    @typing.no_type_check
    def __str__(self):
        """Human readable rendition esp. for debugging."""
        return f'{self.repl=} -> {self.ace=}\n'


def load_table(path: pathlib.Path) -> typing.Any:
    """Generate Table instance from JSON file."""
    with open(path, 'rt', encoding=ENCODING) as dump:
        return Table(**json.load(dump))
