from danoan.dictionaries.chatgpt.cli.commands import (
    get_definition,
    get_synonyme,
    get_reverse_definition,
)

import argparse


def extend_parser(subcommand_action=None):
    command_name = "chatgpt-dictionary"
    description = "ChatGPT dictionary"
    help = description

    if subcommand_action:
        parser = subcommand_action.add_parser(
            command_name,
            help=help,
            description=description,
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )
    else:
        parser = argparse.ArgumentParser(description)

    parser.add_argument(
        "openai_key",
        help="The organization id used to authenticate requests to OpeanAI API.",
    )
    subparser_action = parser.add_subparsers()

    list_of_commands = [get_definition, get_synonyme, get_reverse_definition]
    for command in list_of_commands:
        command.extend_parser(subparser_action)

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
