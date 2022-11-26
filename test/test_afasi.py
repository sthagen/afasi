# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import difflib
import logging
import pathlib

import pytest

import afasi.afasi as af

DIFF_FOR_MINIMAL = """\
--- test/fixtures/basic/minimal-in.xml
+++ minimal-out.xml
@@ -6,12 +6,12 @@
         <message id="SOME_TRACK">
             <source>Some Track</source>
             <extracomment>Does not matter.</extracomment>
-            <translation>Track</translation>
+            <translation>Rock</translation>
         </message>
         <message id="SOME_ROCK">
             <source>Some Rock</source>
             <extracomment>Does not matter.</extracomment>
-            <translation>Rock</translation>
+            <translation>Lounge</translation>
         </message>
     </context>
 </TS>
"""


def test_main_empty(caplog):
    message = 'received wrong number of arguments'
    assert af.main([]) == 2
    text = caplog.text
    assert message in text


def test_main_unknown_command(caplog):
    message = 'received unknown command'
    assert af.main(['fabulate', '', '', '', 'DRYRUN']) == 2
    text = caplog.text
    assert message in text


def test_main_source_is_no_file(caplog):
    message = 'source is no file'
    assert af.main(['translate', 'test/', '', '', 'DRYRUN']) == 1
    text = caplog.text
    assert message in text


def test_main_target_file_exists(caplog):
    message = 'target file exists'
    inp = 'test/fixtures/basic/language.xml'
    assert af.main(['translate', inp, 'test/fixtures/basic/existing_file.xml', '', 'DRYRUN']) == 1
    text = caplog.text
    assert message in text


def test_main_target_file_does_not_exist_no_table_path(caplog):
    message = 'neither plain old parallel array nor object table data given'
    inp = 'test/fixtures/basic/language.xml'
    assert af.main(['translate', inp, 'test/fixtures/basic/non_existing_file.xml', '', 'DRYRUN']) == 1
    text = caplog.text
    assert message in text


def test_main_translate_dryrun_only():
    inp = 'test/fixtures/basic/language.xml'
    assert af.main(['translate', inp, '', 'test/fixtures/basic/fuzz.json', 'DRYRUN']) == 0


def test_main_translate_augmented_dryrun_only():
    inp = 'test/fixtures/basic/language.xml'
    assert af.main(['translate', inp, '', 'test/fixtures/basic/translation.json', 'DRYRUN']) == 0


def test_main_translate_for_real():
    inp = 'test/fixtures/basic/language.xml'
    tab = 'test/fixtures/basic/fuzz.json'
    assert af.main(['translate', inp, '', tab, '']) == 0


def test_load_translation_table_empty_path_string():
    message = 'translation table path not given'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table('')


def test_load_translation_table_wrong_file_format():
    message = 'translation table path must have a .json, yaml, or .yml suffix'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table(pathlib.Path('test/fixtures/basic/fuzz.py'))


def test_load_translation_table_as_empty():
    message = 'translation table is empty'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table(pathlib.Path('test/fixtures/basic/empty.json'))


def test_load_translation_table_with_non_pairs():
    message = 'translation table is not array of two element arrays'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table(pathlib.Path('test/fixtures/basic/triads.json'))


def test_main_translate_minimal_for_real_stdout(capsys):
    inp = 'test/fixtures/basic/minimal-in.xml'
    tab = 'test/fixtures/basic/minimal.json'
    assert af.main(['translate', inp, '', tab, '']) == 0
    captured = capsys.readouterr()
    assert captured.err == ''


def test_main_translate_augmented_for_real_stdout(capsys):
    inp = 'test/fixtures/basic/language.xml'
    tab = 'test/fixtures/basic/translation.json'
    assert af.main(['translate', inp, '', tab, '']) == 0
    captured = capsys.readouterr()
    assert captured.err == ''


def test_main_translate_augmented_for_real_to_file_no_diff(capsys, tmp_path):
    inp = 'test/fixtures/basic/language.xml'
    out_fake = 'language-out.xml'
    out = tmp_path / out_fake
    tab = 'test/fixtures/basic/translation.json'
    assert af.main(['translate', inp, out, tab, '']) == 0
    captured = capsys.readouterr()
    assert captured.err == ''
    assert pathlib.Path(out).is_file()


def test_main_translate_minimal_for_real_to_file(capsys, tmp_path):
    inp = 'test/fixtures/basic/minimal-in.xml'
    out_fake = 'minimal-out.xml'
    out = tmp_path / out_fake
    tab = 'test/fixtures/basic/minimal.json'
    assert af.main(['translate', inp, out, tab, '']) == 0
    captured = capsys.readouterr()
    assert captured.err == ''
    assert pathlib.Path(out).is_file()

    with open(out, 'rt', encoding=af.ENCODING) as handle:
        assert any('            <translation>Lounge</translation>' in line for line in handle)

    with open(inp, 'rt', encoding=af.ENCODING) as handle:
        src = handle.readlines()
    with open(out, 'rt', encoding=af.ENCODING) as handle:
        tgt = handle.readlines()

    assert DIFF_FOR_MINIMAL == ''.join(line for line in difflib.unified_diff(src, tgt, fromfile=inp, tofile=out_fake))


def test_main_translate_minimal_dryrun_for_real_to_file(caplog, tmp_path):
    logging.root.setLevel(logging.INFO)
    inp = 'test/fixtures/basic/minimal-in.xml'
    out = tmp_path / 'minimal-out-dryrun-will-not-be-created.xml'
    tab = 'test/fixtures/basic/minimal.json'
    messages = (
        "  1. '>Rock' -> '>Lounge'",
        "  2. '>Track' -> '>Rock'",
    )
    assert af.main(['translate', inp, out, tab, 'DRYRUN']) == 0
    text = caplog.text
    for message in messages:
        assert message in text
    assert pathlib.Path(out).is_file() is False
