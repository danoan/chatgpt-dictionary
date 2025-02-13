from danoan.word_guru.core import api, exception

import argparse
import logging
from pathlib import Path
import sys
from typing import Optional

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setStream(sys.stderr)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def get_translation(
    openai_key: str,
    cache_folder: Optional[str],
    word: str,
    from_language: str,
    to_language: str,
    *args,
    **kwargs,
):
    """
    Get the translation of the word.
    """
    if cache_folder:
        cache_folder_path = Path(cache_folder)
        if not cache_folder_path.exists():
            logger.error(
                "The given cache folder does not exist. Create one before proceeding."
            )
            exit(1)

    try:
        print(
            api.get_translation(
                openai_key, cache_folder_path, word, from_language, to_language
            )
        )
    except exception.OpenAIEmptyResponse:
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


def main():
    parser = extend_parser()

    args = parser.parse_args()
    if "func" in args:
        args.func(**vars(args))
    elif "subcommand_help" in args:
        args.subcommand_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
