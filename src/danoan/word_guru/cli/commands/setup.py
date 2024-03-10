from danoan.word_guru.cli import utils

import argparse


def init():
    try:
        utils.ensure_environment_variable_exist()
        utils.ensure_configuration_file_exist()
    except utils.EnvironmentVariableIsNotSet as ex:
        print(
            f"The environment variable {ex.environment_variable} is not set. Please define this variable. It should point to a folder where configuration files will be stored."
        )
        exit(1)
    except utils.ConfigurationFileDoesNotExist as ex:
        print(f"Could not find {ex.configuration_filepath}. Creating an empty one.")
        ex.configuration_filepath.parent.mkdir(parents=True, exist_ok=True)
        ex.configuration_filepath.touch()

    return utils.get_configuration_file()


def print_config(*args, **kwargs):
    init()
    configuration_filepath = utils.ensure_configuration_file_exist()
    with open(configuration_filepath, "r") as f:
        print(f"Contents of: {configuration_filepath}:")
        print(f.read())


def extend_parser(subcommand_action=None):
    command_name = "setup"
    description = "Create or edit configuration file"
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

    subparser_action = parser.add_subparsers()
    # list_of_commands = [init]
    # for command in list_of_commands:
    #     command.extend_parser(subparser_action)

    parser.set_defaults(func=print_config, subcommand_help=parser.print_help)
    return parser


if __name__ == "__main__":
    parser = extend_parser()
    args = parser.parse_args()

    if "func" in args:
        args.func(**vars(args))
    elif "subcommand_help" in args:
        args.subcommand_help()
    else:
        parser.print_help()
