from danoan.word_guru.core import exception

import pycountry
from typing import Dict, Optional, Any
from pathlib import Path
import toml

import importlib.resources as pgk_resources
from danoan.word_guru import prompts
from danoan.llm_assistant.runner.core import api as llma
from danoan.llm_assistant.common.model import RunnerConfiguration, PromptConfiguration


def _call_llm(
    openai_key: str,
    cache_path: Optional[Path],
    prompt_filename: str,
    prompt_data: Dict[str, Any],
):
    use_cache = cache_path is not None

    runner_config = RunnerConfiguration(
        openai_key, "gpt-4o-mini", use_cache, cache_path
    )
    llma.LLMAssistant().setup(runner_config)

    with pgk_resources.open_text(prompts, prompt_filename) as f:
        prompt_config = PromptConfiguration(**toml.load(f))

    return llma.custom(prompt_config, **prompt_data)


def _get_language(language_alpha3: str):
    language = pycountry.languages.get(alpha_3=language_alpha3)
    if not language:
        raise exception.LanguageCodeNotRecognizedError(language_alpha3)
    return language


def get_definition(
    openai_key: str, cache_path: Optional[Path], word: str, language_alpha3
) -> str:
    """
    Get the definition of a word.

    The response is a string containing the definition of the word.

    Raises:
        OpenAIEmptyResponseError: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "word-definition.toml"
    language = _get_language(language_alpha3)
    data = {"language": language.name, "message": word}
    response = _call_llm(openai_key, cache_path, prompt_filename, data)
    if not response:
        raise exception.OpenAIEmptyResponseError()

    return response.content


def get_synonym(
    openai_key: str, cache_path: Optional[Path], word: str, language_alpha3
) -> str:
    """
    Get the synonyms of a word.

    The response is string which content is a json list with strings, each one representing a synonym.

    Raises:
        OpenAIEmptyResponseError: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "alternative-expression.toml"
    language = _get_language(language_alpha3)
    data = {"language": language.name, "message": word}
    response = _call_llm(openai_key, cache_path, prompt_filename, data)
    if not response:
        raise exception.OpenAIEmptyResponseError()

    return response.content


def get_reverse_definition(
    openai_key: str, cache_path: Optional[Path], text: str, language_alpha3: str
) -> str:
    """
    Get a list of words that best encode the intention of a text.

    The response is a string which the content is a json list with strings, each one representing a word.

    Raises:
        OpenAIEmptyResponseError: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "reverse-definition.toml"
    language = _get_language(language_alpha3)
    data = {"language": language.name, "message": text}
    response = _call_llm(openai_key, cache_path, prompt_filename, data)
    if not response:
        raise exception.OpenAIEmptyResponseError()

    return response.content


def get_usage_examples(
    openai_key: str, cache_path: Optional[Path], word: str, language_alpha3: str
) -> str:
    """
    Get a list of sentences in which the word is used with their different meanings.

    The response is a string which the content is a json list with strings, each one representing a word.

    Raises:
        OpenAIEmptyResponseError: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "usage-examples.toml"
    language = _get_language(language_alpha3)
    data = {"language": language.name, "message": word}
    response = _call_llm(openai_key, cache_path, prompt_filename, data)
    if not response:
        raise exception.OpenAIEmptyResponseError()

    return response.content


def get_pos_tag(
    openai_key: str, cache_path: Optional[Path], word: str, language_alpha3: str
) -> str:
    """
    Get the part-of-speech tag of the most common uses of the word.

    The response is a string which the content is a json list with strings, each one representing a pos tag.

    Raises:
        OpenAIEmptyResponseError: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "classify-pos.toml"
    language = _get_language(language_alpha3)
    data = {"language": language.name, "message": word}
    response = _call_llm(openai_key, cache_path, prompt_filename, data)
    if not response:
        raise exception.OpenAIEmptyResponseError()

    return response.content


def get_translation(
    openai_key: str,
    cache_path: Optional[Path],
    word: str,
    from_language_alpha3: str,
    to_language_alpha3: str,
) -> str:
    """
    Get the translation of a word or expression.

    Raises:
        OpenAIEmptyResponseError: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "translate.toml"
    from_language = _get_language(from_language_alpha3)
    to_language = _get_language(to_language_alpha3)
    data = {
        "from_language": from_language.name,
        "to_language": to_language.name,
        "message": word,
    }
    response = _call_llm(openai_key, cache_path, prompt_filename, data)
    if not response:
        raise exception.OpenAIEmptyResponseError()

    return response.content


def get_correction(
    openai_key: str, cache_path: Optional[Path], word: str, language_alpha3: str
) -> str:
    """
    Get the corrected version of a text.

    Raises:
        OpenAIEmptyResponseError: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "correct-text.toml"
    language = _get_language(language_alpha3)
    data = {"language": language.name, "message": word}
    response = _call_llm(openai_key, cache_path, prompt_filename, data)
    if not response:
        raise exception.OpenAIEmptyResponseError()

    return response.content
