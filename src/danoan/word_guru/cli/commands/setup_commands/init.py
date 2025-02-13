from danoan.word_guru.cli import model
from danoan.word_guru.cli import config

import argparse
import os
from pathlib import Path
import toml


def init(*args, **kwargs):
    configuration_file = Path(os.getcwd()) / config.WORD_GURU_CONFIGURATION_FILENAME

    if configuration_file.exists():
        print(f"A configuration file exists already at: {configuration_file}")
        exit(1)

    wg_config = model.WordGuruConfiguration("openai-key", "word-guru.cache.db")
    with open(configuration_file, "w") as f:
        toml.dump(wg_config.__asdict__(), f)

    print(f"Configuration file created at: {configuration_file}")


def extend_parser(subcommand_action=None):
    command_name = "init"
    description = "Create configuration file"
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

    parser.set_defaults(func=init, subcommand_help=parser.print_help)
    return parser
