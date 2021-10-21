# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import difflib
import pathlib

import pytest

import afasi.afasi as af

DIFF_FOR_MINIMAL = """\
--- tests/fixtures/basic/minimal-in.xml
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


def test_main_empty(capsys):
    message = 'received wrong number of arguments'
    af.main([]) == 2
    captured = capsys.readouterr()
    assert message in captured.err


def test_main_unknown_command(capsys):
    message = 'received unknown command'
    af.main(['fabulate', '', '', '', 'DRYRUN']) == 2
    captured = capsys.readouterr()
    assert message in captured.err


def test_main_source_is_no_file(capsys):
    message = 'source is no file'
    af.main(['translate', 'tests/', '', '', 'DRYRUN']) == 2
    captured = capsys.readouterr()
    assert message in captured.err


def test_main_target_file_exists(capsys):
    message = 'target file exists'
    inp = 'tests/fixtures/basic/language.xml'
    af.main(['translate', inp, 'tests/fixtures/basic/existing_file.xml', '', 'DRYRUN']) == 2
    captured = capsys.readouterr()
    assert message in captured.err


def test_main_target_file_does_not_exist_no_table_path(capsys):
    message = 'neither plain old parallel array nor object table data given'
    inp = 'tests/fixtures/basic/language.xml'
    af.main(['translate', inp, 'tests/fixtures/basic/non_existing_file.xml', '', 'DRYRUN']) == 1
    captured = capsys.readouterr()
    assert message in captured.err


def test_main_translate_dryrun_only():
    inp = 'tests/fixtures/basic/language.xml'
    af.main(['translate', inp, '', 'tests/fixtures/basic/fuzz.json', 'DRYRUN']) == 0


def test_main_translate_augmented_dryrun_only():
    inp = 'tests/fixtures/basic/language.xml'
    af.main(['translate', inp, '', 'tests/fixtures/basic/translation.json', 'DRYRUN']) == 0


def test_main_translate_for_real():
    inp = 'tests/fixtures/basic/language.xml'
    tab = 'tests/fixtures/basic/fuzz.json'
    af.main(['translate', inp, '', tab, '']) == 0


def test_load_translation_table_empty_path_string():
    message = 'translation table path not given'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table('')


def test_load_translation_table_wrong_file_format():
    message = 'translation table path must lead to a JSON file'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table(pathlib.Path('tests/fixtures/basic/fuzz.py'))


def test_load_translation_table_as_empty():
    message = 'translation table is empty'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table(pathlib.Path('tests/fixtures/basic/empty.json'))


def test_load_translation_table_with_non_pairs():
    message = 'translation table is not array of two element arrays'
    with pytest.raises(ValueError, match=message):
        af.load_translation_table(pathlib.Path('tests/fixtures/basic/triads.json'))


def test_main_translate_minimal_for_real_stdout(capsys):
    inp = 'tests/fixtures/basic/minimal-in.xml'
    tab = 'tests/fixtures/basic/minimal.json'
    af.main(['translate', inp, '', tab, '']) == 0
    captured = capsys.readouterr()
    assert captured.err == ''


def test_main_translate_augmented_for_real_stdout(capsys):
    inp = 'tests/fixtures/basic/language.xml'
    tab = 'tests/fixtures/basic/translation.json'
    af.main(['translate', inp, '', tab, '']) == 0
    captured = capsys.readouterr()
    assert captured.err == ''


def test_main_translate_augmented_for_real_to_file_no_diff(capsys, tmp_path):
    inp = 'tests/fixtures/basic/language.xml'
    out_fake = 'language-out.xml'
    out = tmp_path / out_fake
    tab = 'tests/fixtures/basic/translation.json'
    af.main(['translate', inp, out, tab, '']) == 0
    captured = capsys.readouterr()
    assert captured.err == ''
    assert pathlib.Path(out).is_file()


def test_main_translate_minimal_for_real_to_file(capsys, tmp_path):
    inp = 'tests/fixtures/basic/minimal-in.xml'
    out_fake = 'minimal-out.xml'
    out = tmp_path / out_fake
    tab = 'tests/fixtures/basic/minimal.json'
    af.main(['translate', inp, out, tab, '']) == 0
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


def test_main_translate_minimal_dryrun_for_real_to_file(capsys, tmp_path):
    inp = 'tests/fixtures/basic/minimal-in.xml'
    out = tmp_path / 'minimal-out-dryrun-will-not-be-created.xml'
    tab = 'tests/fixtures/basic/minimal.json'
    messages = (
        "  1. '>Rock' -> '>Lounge'",
        "  2. '>Track' -> '>Rock'",
    )
    af.main(['translate', inp, out, tab, 'DRYRUN']) == 0
    captured = capsys.readouterr()
    for message in messages:
        assert message in captured.err
    assert pathlib.Path(out).is_file() is False
