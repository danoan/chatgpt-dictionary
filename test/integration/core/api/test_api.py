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
        ("hapiness", "eng"),
        ("state", "eng"),
        ("clafoutis", "fra"),
        ("pareil", "fra"),
        ("magari", "ita"),
        ("profumo", "ita"),
    ],
)
def test_get_definition(openai_key, word, language):
    response = api.get_definition(openai_key, word, language)
    assert response
    assert len(response) > 10


@pytest.mark.api
@pytest.mark.parametrize(
    "word,language",
    [
        ("terrible", "eng"),
        ("passion", "eng"),
        ("ensemble", "fra"),
        ("travail", "fra"),
        ("cibo", "ita"),
        ("facile", "ita"),
    ],
)
def test_get_synonyme(openai_key, word, language):
    response = api.get_definition(openai_key, word, language)
    assert response
    assert len(response) > 10


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
    response = api.get_reverse_definition(openai_key, text, language)
    assert response
    assert len(response) > 10
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
    response = api.get_usage_examples(openai_key, word, language)
    assert response
    obj = json.loads(response)
    assert len(obj) > 0
