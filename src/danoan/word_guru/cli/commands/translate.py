from danoan.word_guru.logging_config import setup_logging
from danoan.word_guru.core import api, exception

import argparse
import logging
from typing import Optional

setup_logging()
logger = logging.getLogger(__name__)


def get_translation(
    openai_key: str,
    cache_path: Optional[str],
    word: str,
    from_language: str,
    to_language: str,
    *args,
    **kwargs,
):
    """
    Translate text.
    """
    try:
        print(
            api.get_translation(
                openai_key, cache_path, word, from_language, to_language
            )
        )
    except exception.OpenAIEmptyResponseError:
        logger.error("OpeanAI returned an empty response.")


def extend_parser(subcommand_action=None):
    command_name = "translate"
    description = get_translation.__doc__
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

    parser.add_argument("word", help="The word or expression you want to translate.")
    parser.add_argument(
        "from_language",
        metavar="from-language",
        help="The language of the original word. It should be the IETF 639-3 code of the language. E.g. eng",
    )
    parser.add_argument(
        "to_language",
        metavar="to-language",
        help="The language of the translation. It should be the IETF 639-3 code of the language. E.g. eng",
    )

    parser.set_defaults(func=get_translation, subcommand_help=parser.print_help)

    return parser
