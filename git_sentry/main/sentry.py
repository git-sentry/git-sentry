import os

import click

from zen_core.handlers.git_config import apply_configuration
from zen_core.logging.printer import write, focus_out
from zen_core.handlers.git_client import GitClient
from zen_core.parsing.toml_parser import parse_toml_configuration


@click.group()
@click.version_option(version=None)
def cli():
    pass


@cli.command(help='Apply Git config from path')
@click.argument('toml_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-n', '--dry-run', is_flag=True, default=False)
def apply(toml_path, dry_run):
    toml_path = os.path.expanduser(toml_path)

    git_client = GitClient()
    write(f'Welcome back, {focus_out(git_client.me().login())}!\n')
    orgs = parse_toml_configuration(toml_path)

    apply_configuration(git_client, orgs, dry_run)

    write('Nothing left to do, see you soon!')


def run_cli():
    cli()


if __name__ == '__main__':
    run_cli()
