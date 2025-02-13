from danoan.word_guru.cli import config
from danoan.word_guru.cli.commands.setup_commands import init

import argparse


def print_config(*args, **kwargs):
    try:
        config.get_configuration()
    except:
        print(
            f"No configuration file found. Create one by calling word-guru setup init or set up the environment variable {config.WORD_GURU_ENV_VARIABLE} to point to a directory where configuration will be stored."
        )
        exit(1)

    configuration_filepath = config.get_configuration_filepath()
    with open(configuration_filepath, "r") as f:
        print(f"Using configuration file: {configuration_filepath}:\n")
        print(f.read())


def extend_parser(subcommand_action=None):
    command_name = "setup"
    description = "Initialize or list the current configuration file"
    help = description

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

    commands = [init]
    subparser_action = parser.add_subparsers()
    for cmd in commands:
        cmd.extend_parser(subparser_action)

    parser.set_defaults(func=print_config, subcommand_help=parser.print_help)
    return parser
