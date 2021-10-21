# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Tabel (Danish for Table). Class API."""
import json
import pathlib
import typing

ENCODING = 'utf-8'


class Table:
    """Translation table."""

    __slots__ = ['description', 'contra', 'count', 'pro', 'translations']

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
    def __str__(self):
        """Human readable rendition esp. for debugging."""
        return (
            f'table:\n  {self.description=}\n'
            f'  {self.contra=}\n'
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


DATA = """\
{
  "table": {
    "description": "table level default constraints, row attributes do replace those if present.",
    "contra": [
      "extracomment",
      "source"
    ],
    "count": 0,
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

table = Table(**json.loads(DATA))
print('Table from string:')
print(table, end='')
other = load_table(pathlib.Path('tests/fixtures/basic/translation.json'))
print('Table from file:')
print(other, end='')
