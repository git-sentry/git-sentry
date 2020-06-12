import os

import click

from git_sentry.logging.printer import write, focus_out
from git_sentry.main.connectivity.git import GitClient
from git_sentry.parsing.toml_parser import parse_toml_configuration


@click.group()
def cli():
    pass


@cli.command()
@click.argument('toml_path', type=click.Path(exists=True, resolve_path=True))
@click.option('-n', '--dry-run', is_flag=True, default=True)
def apply(toml_path, dry_run):
    toml_path = os.path.expanduser(toml_path)

    git_client = GitClient()
    write(f'Welcome back, {focus_out(git_client.me().login)}!\n')
    orgs = parse_toml_configuration(toml_path)

    for org_pattern, org_config in orgs.items():
        matching_orgs = git_client.search_orgs(org_pattern)

        for org in matching_orgs:
            org_config = org_config.resolve(org)
            current_configuration = org.configuration()

            difference = org_config.diff(current_configuration)

            if difference.length() != 0:
                write(f'Configuration analysis for {focus_out(org.login())} is complete.')
                write(difference)

            # if not dry_run:
            #     for m in difference.members():
            #         org.grant_access(m)
            #
            #     for m in difference.admins():
            #         org.grant_access(m, role='admin')
            #
            #     for team in difference.teams():
            #

    # for team_name, team_config in teams.items():
    #     repo_configs = team_config.get('repos', [])
    #
    #     for repo_pattern, permission in repo_configs.items():
    #         repositories = git_client.search_repos(repo_pattern)
    #         for matching_repo in repositories:
    #             matching_org = git_client.organization(matching_repo.owner().login)
    #             existing_team = matching_org.team(team_name)
    #             diff = TeamConfigurationDifference(team_name, existing_team, team_config, repositories, permission)
    #             diff.difference()
    #
    #
    #             # write(matching_repo.owner().login)
    #
    #         # print(retrieve_orgs)
    #     #     git_client.search_repos(repo_pattern)
    #         # print(repo, repo_config['permission'])
    #         # pattern = repo['pattern']
    #         # print(pattern)
    #         # all_orgs_patterns = [['pattern']]
    #     # print(team_name)
    #     # print(team_config)




def main():
    cli()


if __name__ == '__main__':
    main()
