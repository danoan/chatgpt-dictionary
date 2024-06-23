from danoan.word_guru.core import exception

from hashlib import sha256
from jinja2 import Environment, PackageLoader
from openai import OpenAI
import pycountry
from typing import Dict, Optional, Any
from pathlib import Path

env = Environment(loader=PackageLoader("danoan.word_guru", package_path="prompts"))


def _singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@_singleton
class _Cache:
    def __init__(self, cache_folder: Path):
        if cache_folder.exists():
            self.cache_folder = cache_folder
            self.cache_folder.mkdir(parents=True, exist_ok=True)
        else:
            raise FileNotFoundError()

    def load(self, prompt: str):
        k = sha256(prompt.encode("utf-8")).hexdigest()
        cache_file = self.cache_folder / f"{k}.txt"
        if cache_file.exists():
            with open(cache_file, "r") as f:
                return f.read()
        else:
            return None

    def save(self, prompt: str, response: str):
        k = sha256(prompt.encode("utf-8")).hexdigest()
        cache_file = self.cache_folder / f"{k}.txt"
        with open(cache_file, "w") as f:
            f.write(response)


def _call_openai(
    openai_key: str,
    cache_folder: Optional[Path],
    prompt_filename: str,
    prompt_data: Dict[str, Any],
    content: str,
):
    client = OpenAI(api_key=openai_key)
    prompt = env.get_template(prompt_filename).render(data=prompt_data)

    cache = None
    if cache_folder:
        cache = _Cache(cache_folder)

    response = None
    cache_query = prompt + content
    if cache:
        response = cache.load(cache_query)

    if not response:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"<<{content}>>"},
            ],
            top_p=0.1,
        )

        if len(completion.choices) == 0:
            return None
        else:
            response = completion.choices[0].message.content

        if cache:
            cache.save(cache_query, response)

    return response


def _get_language(language_alpha3: str):
    language = pycountry.languages.get(alpha_3=language_alpha3)
    if not language:
        raise exception.LanguageCodeNotRecognizedError(language_alpha3)
    return language


def get_definition(
    openai_key: str, cache_folder: Optional[Path], word: str, language_alpha3
) -> str:
    """
    Get the definition of a word.

    The response is a string containing the definition of the word.

    Raises:
        OpenAIEmptyResponse: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "get-simple-definition.txt"
    language = _get_language(language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, cache_folder, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_synonym(
    openai_key: str, cache_folder: Optional[Path], word: str, language_alpha3
) -> str:
    """
    Get the synonyms of a word.

    The response is string which content is a json list with strings, each one representing a synonym.

    Raises:
        OpenAIEmptyResponse: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "get-synonym.txt"
    language = _get_language(language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, cache_folder, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_reverse_definition(
    openai_key: str, cache_folder: Optional[Path], text: str, language_alpha3: str
) -> str:
    """
    Get a list of words that best encode the intention of a text.

    The response is a string which the content is a json list with strings, each one representing a word.

    Raises:
        OpenAIEmptyResponse: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "get-reverse-definition.txt"
    language = _get_language(language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, cache_folder, prompt_filename, data, text)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_usage_examples(
    openai_key: str, cache_folder: Optional[Path], word: str, language_alpha3: str
) -> str:
    """
    Get a list of sentences in which the word is used with their different meanings.

    The response is a string which the content is a json list with strings, each one representing a word.

    Raises:
        OpenAIEmptyResponse: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "get-usage-examples.txt"
    language = _get_language(language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, cache_folder, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_pos_tag(
    openai_key: str, cache_folder: Optional[Path], word: str, language_alpha3: str
) -> str:
    """
    Get the part-of-speech tag of the most common uses of the word.

    The response is a string which the content is a json list with strings, each one representing a pos tag.

    Raises:
        OpenAIEmptyResponse: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "get-pos-tag.txt"
    language = _get_language(language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, cache_folder, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_translation(
    openai_key: str,
    cache_folder: Optional[Path],
    word: str,
    from_language_alpha3: str,
    to_language_alpha3: str,
) -> str:
    """
    Get the translation of a word or expression.

    Raises:
        OpenAIEmptyResponse: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "get-translation.txt"
    from_language = _get_language(from_language_alpha3)
    to_language = _get_language(to_language_alpha3)
    data = {
        "from_language_name": from_language.name,
        "to_language_name": to_language.name,
    }
    text_response = _call_openai(openai_key, cache_folder, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_correction(
    openai_key: str, cache_folder: Optional[Path], word: str, language_alpha3: str
) -> str:
    """
    Get the corrected version of a text.

    Raises:
        OpenAIEmptyResponse: If openai return an empty response.
        LanguageCodeNotRecognizedError: If language code is not recognized.
    """
    prompt_filename = "get-correction.txt"
    language = _get_language(language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, cache_folder, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response
