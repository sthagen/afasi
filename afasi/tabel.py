# -*- coding: utf-8 -*-
# pylint: disable=expression-not-assigned,line-too-long
"""Tabel (Danish for Table). Class API."""
import json
import pathlib


class Table:
    __slots__ = ['description', 'contra', 'count', 'pro', 'translations']
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'table':
                for me, ta in value.items():
                    setattr(self, me, ta)
            elif key == 'translations':
                setattr(self, key, [])
                for entry in value:
                    self.translations.append(Translation(**entry))
            else:
                print(f'ignored ({key} -> {value}')


class Translation:
    __slots__ = ['repl', 'ace']
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


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

data = json.loads(DATA)
print(Table(**data).description)
