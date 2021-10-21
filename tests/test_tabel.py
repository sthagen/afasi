# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import json

import afasi.tabel as tb

TABLE_DATA = """\
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


def test_translation_init_from_dict():
    data = {'repl': '>Autotrack', 'ace': '>Autolock'}
    translation = tb.Translation(**data)
    assert translation.repl == data['repl']
    assert translation.ace == data['ace']


def test_table_init_from_json_string():
    table = tb.Table(**json.loads(TABLE_DATA))
    assert table.flip_is_stop is True
    assert table.pro == ['translation']


def test_table_init_from_json_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "tr.json"
    p.write_text(TABLE_DATA)
    with open(p, 'rt', encoding=tb.ENCODING) as dump:
        table = tb.Table(**json.load(dump))
    assert table.flip_is_stop is True
    assert table.pro == ['translation']
