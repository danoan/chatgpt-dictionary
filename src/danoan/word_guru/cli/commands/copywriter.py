from danoan.word_guru.cli.commands.copywriter_commands import (
    get_correction,
)

import argparse


def extend_parser(subcommand_action=None):
    command_name = "copywriter"
    description = "Your multilanguage copywriter specialist."
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
        get_correction,
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
