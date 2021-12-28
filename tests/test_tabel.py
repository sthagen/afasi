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

TABLE_DATA_FLOP_IS_STOP = TABLE_DATA.replace('true', 'false')

FLIP_FLOP_DATA = """\
        <message id="SOME_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Track</translation>
        </message>
        <message id="ANOTHER_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Track</translation>
        </message>
"""

FLIP_FLOP_TRANSLATED = """\
        <message id="SOME_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Track</translation>
        </message>
        <message id="ANOTHER_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Lock</translation>
        </message>
"""

FLOP_FLIP_TRANSLATED = """\
        <message id="SOME_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Lock</translation>
        </message>
        <message id="ANOTHER_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Track</translation>
        </message>
"""

FULLY_TRANSLATED = """\
        <message id="SOME_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Lock</translation>
        </message>
        <message id="ANOTHER_TRACK">
            <source>Some Track</source>
            <extracomment>Does not matter.</extracomment>
            <translation>Lock</translation>
        </message>
"""


def test_translation_init_from_dict():
    data = {'repl': '>Autotrack', 'ace': '>Autolock'}
    translation = tb.Translation(**data)
    assert translation.repl == data['repl']
    assert translation.ace == data['ace']
    assert str(translation).strip() == "self.repl='>Autotrack' -> self.ace='>Autolock'"


def test_table_init_from_json_string():
    table = tb.Table(**json.loads(TABLE_DATA))
    assert table.flip_is_stop is True
    assert table.pro == ['translation']
    assert "self.repl='>Autotrack' -> self.ace='>Autolock'" in str(table)


def test_table_init_from_json_file(tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'tr.json'
    p.write_text(TABLE_DATA)
    table = tb.load_table(p)
    assert table.flip_is_stop is True
    assert table.pro == ['translation']


def test_translate_apply_once():
    data = {'repl': '>Autotrack', 'ace': '>Autolock'}
    translation = tb.Translation(**data)
    assert translation.apply('<translation>Autotrack') == '<translation>Autolock'


def test_table_translate_once():
    table = tb.Table(**json.loads(TABLE_DATA))
    assert table.translate('<translation>Autotrack') == '<translation>Autolock'


def test_table_translate_twice_contra_once_pro_once_no():
    table = tb.Table(**json.loads(TABLE_DATA))
    assert table.translate('<source>Autotrack') == '<source>Autotrack'
    assert table.translate('<extracomment>Autotrack') == '<extracomment>Autotrack'
    assert table.translate('<translation>Autotrack') == '<translation>Autolock'
    assert table.translate('<noitalsnart>Autotrack') == '<noitalsnart>Autotrack'


def test_table_translate_flip_flop_some():
    table = tb.Table(**json.loads(TABLE_DATA))
    translation = []
    for line in FLIP_FLOP_DATA.split('\n'):
        translation.append(table.translate(line))
    for out, exp in zip(translation, FLIP_FLOP_TRANSLATED.split('\n')):
        assert out == exp


def test_table_translate_flop_flip_some():
    table = tb.Table(**json.loads(TABLE_DATA_FLOP_IS_STOP))
    translation = []
    for line in FLIP_FLOP_DATA.split('\n'):
        translation.append(table.translate(line))
    for out, exp in zip(translation, FLOP_FLIP_TRANSLATED.split('\n')):
        assert out == exp


def test_table_translate_no_flip_flop_some():
    no_ff_data = json.loads(TABLE_DATA)
    no_ff_data['table']['flip_flop'] = []
    table = tb.Table(**no_ff_data)
    translation = []
    for line in FLIP_FLOP_DATA.split('\n'):
        translation.append(table.translate(line))
    for out, exp in zip(translation, FULLY_TRANSLATED.split('\n')):
        assert out == exp
