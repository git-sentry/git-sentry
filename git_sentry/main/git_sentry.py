import os

import click

from git_sentry.logging.printer import write, focus_out
from git_sentry.main.connectivity.git import connect
from git_sentry.parsing.toml_parser import parse_toml_configuration


@click.group()
def cli():
    pass


@cli.command()
# @click.argument('toml_path', type=click.Path(exists=True, resolve_path=True))
# def apply(toml_path):
def apply():
    toml_path = os.path.expanduser('~/workspace/git-sentry/git_sentry/parsing/test/valid_toml')

    git_client = connect()
    write(f'Hello {focus_out(git_client.me().login)}\n')

    parse_toml_configuration(toml_path)


def main():
    cli()


if __name__ == '__main__':
    main()
