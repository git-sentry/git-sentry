from git_sentry.logging.printer import write, focus_out
from git_sentry.main.connectivity.git import GitClient


def apply_configuration(git_client, org_configurations, dry_run):
    for org_pattern, org_config in org_configurations.items():
        matching_orgs = git_client.search_orgs(org_pattern)

        for org in matching_orgs:
            org_config = org_config.resolve(org)
            current_configuration = org.configuration()

            difference = org_config.diff(current_configuration)

            if difference.length() != 0:
                write(f'Configuration analysis for {focus_out(org.login())} is complete.')
                write(difference)

            if not dry_run:
                for m in difference.members():
                    org.grant_access(m)

                for m in difference.admins():
                    org.grant_access(m, role='admin')

                for team_name, team_config in difference.teams().items():
                    existing_team = org.team(team_name)
                    if existing_team is None:
                        existing_team = org.create_team(team_name)

                    for repo, permission in team_config.repos().items():
                        existing_team.add_to_repo(repo, permission)

                    for member in team_config.members():
                        existing_team.grant_access(member)
                    for admin in team_config.admins():
                        existing_team.grant_access(admin, role='maintainer')
