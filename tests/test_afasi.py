# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring,unused-import,reimported
import pathlib

import pytest

import afasi.kysy as af


def test_main_empty():
    message = 'received wrong number of arguments'
    with pytest.raises(UserWarning) as ex:
        af.main([]) == 2
        assert message in str(ex.value)
