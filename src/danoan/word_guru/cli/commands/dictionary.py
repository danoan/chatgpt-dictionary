from danoan.word_guru.cli.commands.dictionary_commands import (
    get_definition,
    get_synonyme,
    get_reverse_definition,
    get_usage_examples,
    get_pos_tag,
)

import argparse


def extend_parser(subcommand_action=None):
    command_name = "dictionary"
    description = "Multilanguage dictionary powered by ChatGPT"
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

    subparser_action = parser.add_subparsers()

    list_of_commands = [
        get_definition,
        get_synonyme,
        get_reverse_definition,
        get_usage_examples,
        get_pos_tag,
    ]
    for command in list_of_commands:
        command.extend_parser(subparser_action)

    parser.set_defaults(subcommand_help=parser.print_help)

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
