from danoan.word_guru.cli import cli


def test_cli():
    parser = cli.extend_parser()
    assert parser
