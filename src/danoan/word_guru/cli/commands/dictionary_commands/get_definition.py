from danoan.word_guru.logging_config import setup_logging
from danoan.word_guru.core import api, exception

import argparse
import logging
from typing import Optional

setup_logging()
logger = logging.getLogger(__name__)


def get_definition(
    openai_key: str,
    cache_path: Optional[str],
    word: str,
    language: str,
    *args,
    **kwargs,
):
    """
    Get the definition of a word in the given language.
    """
    try:
        print(api.get_definition(openai_key, cache_path, word, language))
    except exception.OpenAIEmptyResponseError:
        logger.error("OpeanAI returned an empty response.")


def extend_parser(subcommand_action=None):
    command_name = "get-definition"
    description = get_definition.__doc__
    help = description.split(".")[0] if description else ""

    if subcommand_action:
        parser = subcommand_action.add_parser(
            command_name,
            help=help,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    else:
        parser = argparse.ArgumentParser(
            command_name,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    parser.add_argument("word", help="The word you ask for the definition.")
    parser.add_argument(
        "language", help="The IETF 639-3 code of the language. E.g. eng"
    )

    parser.set_defaults(func=get_definition, subcommand_help=parser.print_help)

    return parser
