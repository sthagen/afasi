# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
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


def test_main_translate():
    af.main(['translate', '', '', 'tests/fixtures/basic/fuzz.json', 'DRYRUN']) == 0
