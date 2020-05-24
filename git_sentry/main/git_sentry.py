import os

import click

from git_sentry.logging.printer import write, focus_out
from git_sentry.main.connectivity.git import GitClient
from git_sentry.parsing.toml_parser import parse_toml_configuration


@click.group()
def cli():
    pass


@cli.command()
# @click.argument('toml_path', type=click.Path(exists=True, resolve_path=True))
# def apply(toml_path):
@click.argument('query')
def apply(query):
    toml_path = os.path.expanduser('/test/valid_toml')

    git_client = GitClient()
    write(f'Hello {focus_out(git_client.me().login)}\n')

    org, teams = parse_toml_configuration(toml_path)

    for result in git_client.search_orgs(query):
        print(result)

    for result in git_client.search_repos(query):
        print(result)


def main():
    cli()


if __name__ == '__main__':
    main()
