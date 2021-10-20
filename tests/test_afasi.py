# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pathlib

import pytest

import afasi.afasi as af


def test_main_empty():
    message = 'received wrong number of arguments'
    with pytest.raises(UserWarning) as ex:
        af.main([]) == 2
        assert message in str(ex.value)


def test_main_unknown_command():
    message = 'received wrong number of arguments'
    with pytest.raises(UserWarning) as ex:
        af.main(['fabulate', '', '', '', 'DRYRUN']) == 2
        assert message in str(ex.value)


def test_main_source_is_no_file():
    message = 'source is no file'
    with pytest.raises(UserWarning) as ex:
        af.main(['translate', 'tests/', '', '', 'DRYRUN']) == 2
        assert message in str(ex.value)


def test_main_target_file_exists():
    message = 'target file exists'
    inp = 'tests/fixtures/basic/language.xml'
    with pytest.raises(UserWarning) as ex:
        af.main(['translate', inp, 'tests/fixtures/basic/existing_file.xml', '', 'DRYRUN']) == 2
        assert message in str(ex.value)


def test_main_translate_dryrun_only():
    af.main(['translate', '', '', 'tests/fixtures/basic/fuzz.json', 'DRYRUN']) == 0


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
