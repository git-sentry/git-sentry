import click

from git_sentry.logging.printer import write, focus_out
from git_sentry.main.connectivity.git import connect


@click.group()
def cli():
    pass


@cli.command()
def apply():
    git_client = connect()
    write(f'Hello {focus_out(git_client.me().login)}')


def main():
    cli()


if __name__ == '__main__':
    main()
