from danoan.word_guru.core import api, exception

import pytest


def test_get_language():
    language = api._get_language("eng")
    assert language
    with pytest.raises(exception.LanguageCodeNotRecognizedError):
        language = api._get_language("en")
