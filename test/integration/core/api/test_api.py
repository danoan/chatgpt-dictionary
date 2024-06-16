from danoan.word_guru.core import api

import json
import pytest
import warnings


@pytest.fixture(scope="session")
def openai_key(pytestconfig):
    v = pytestconfig.getoption("openai_key")
    if v is None:
        warnings.warn("The openai_key is not specified. Tests won't be executed.")
    return pytestconfig.getoption("openai_key", skip=True)


@pytest.mark.api
@pytest.mark.parametrize(
    "word,language",
    [
        ("happiness", "eng"),
        ("pareil", "fra"),
        ("profumo", "ita"),
    ],
)
def test_get_definition(openai_key, word, language):
    response = api.get_definition(openai_key, None, word, language)
    assert response
    obj = json.loads(response)
    assert len(obj) > 0


@pytest.mark.api
@pytest.mark.parametrize(
    "word,language",
    [
        ("terrible", "eng"),
        ("travail", "fra"),
        ("facile", "ita"),
    ],
)
def test_get_synonym(openai_key, word, language):
    response = api.get_definition(openai_key, None, word, language)
    assert response
    obj = json.loads(response)
    assert len(obj) > 0


@pytest.mark.api
@pytest.mark.parametrize(
    "text,language,mandate_words",
    [
        ("that thing we put our plates on whenever we have a meal", "eng", ["table"]),
        ("ce vêtement qu'on utilise quand on a froid", "fra", ["manteau"]),
        ("una bevanda nera, aromatica ed energetica", "ita", ["caffè"]),
    ],
)
def test_get_reverse_definition(openai_key, text, language, mandate_words):
    response = api.get_reverse_definition(openai_key, None, text, language)
    assert response
    obj = json.loads(response)
    assert len(obj) > 0
    obj = json.loads(response)
    for word in mandate_words:
        assert word in obj


@pytest.mark.api
@pytest.mark.parametrize(
    "word,language",
    [
        ("notes", "eng"),
        ("manteau", "fra"),
        ("pragmatico", "ita"),
    ],
)
def test_get_usage_examples(openai_key, word, language):
    response = api.get_usage_examples(openai_key, None, word, language)
    assert response
    obj = json.loads(response)
    assert len(obj) > 0
