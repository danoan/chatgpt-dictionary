from danoan.word_guru.core import exception

from jinja2 import Environment, PackageLoader
from openai import OpenAI
import pycountry
from typing import Dict, Any

env = Environment(loader=PackageLoader("danoan.word_guru", package_path="prompts"))


def _call_openai(
    openai_key: str, prompt_filename: str, prompt_data: Dict[str, Any], content: str
):
    client = OpenAI(api_key=openai_key)
    prompt = env.get_template(prompt_filename).render(data=prompt_data)

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
        return completion.choices[0].message.content


def get_definition(openai_key: str, word: str, language_alpha3) -> str:
    """
    Get the definition of a word.

    The response is a string containing the definition of the word.
    """
    prompt_filename = "get-simple-definition.txt"
    language = pycountry.languages.get(alpha_3=language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_synonyme(openai_key: str, word: str, language_alpha3) -> str:
    """
    Get the synonymes of a word.

    The response is string which content is a json list with strings, each one representing a synonyme.
    """
    prompt_filename = "get-synonyme.txt"
    language = pycountry.languages.get(alpha_3=language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_reverse_definition(openai_key: str, text: str, language_alpha3: str) -> str:
    """
    Get a list of words that best encode the intention of a text.

    The response is a string which the content is a json list with strings, each one representing a word.
    """
    prompt_filename = "get-reverse-definition.txt"
    language = pycountry.languages.get(alpha_3=language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, prompt_filename, data, text)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response


def get_usage_examples(openai_key: str, word: str, language_alpha3: str) -> str:
    """
    Get a list of sentences in which the word is used with their different meanings.

    The response is a string which the content is a json list with strings, each one representing a word.
    """
    prompt_filename = "get-usage-examples.txt"
    language = pycountry.languages.get(alpha_3=language_alpha3)
    data = {"language_name": language.name}
    text_response = _call_openai(openai_key, prompt_filename, data, word)
    if not text_response:
        raise exception.OpenAIEmptyResponse()

    return text_response
