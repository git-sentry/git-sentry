import os

import click
from git_sentry.handlers.GitOrgConfiguration import GitOrgConfiguration
from git_sentry.logging.printer import write, focus_out
from git_sentry.main.connectivity.git import GitClient
from git_sentry.parsing.toml_parser import parse_toml_configuration


@click.group()
def cli():
    pass


@cli.command()
@click.argument('toml_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-n', '--dry-run', is_flag=True)
def apply(toml_path, dry_run):
    toml_path = os.path.expanduser(toml_path)

    git_client = GitClient()
    write(f'Welcome back, {focus_out(git_client.me().login)}!\n')
    orgs, teams = parse_toml_configuration(toml_path)

    for org_pattern, org_config in orgs.items():
        matching_orgs = git_client.search_orgs(org_pattern)

        for org in matching_orgs:
            current_configuration = GitOrgConfiguration(org.members('member'), org.members('admin'))
            new_config = GitOrgConfiguration(org_config['members'], org_config['admins'])

            difference = current_configuration.differences(new_config)

            if len(difference) != 0:
                write(f'Configuration analysis for {focus_out(org.login())} is complete.')
                write(difference)


def main():
    cli()


if __name__ == '__main__':
    main()
