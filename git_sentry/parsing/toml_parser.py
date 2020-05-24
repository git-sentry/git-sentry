import glob
from collections import OrderedDict

import toml

from git_sentry.logging.printer import write


def find_toml_files(path):
    return glob.glob(f'{path}/*.toml')


def parse_toml_configuration(path):
    groups = parse_groups(path)
    orgs = _parse_orgs(path, groups)
    teams = _parse_teams(path, groups)
    return orgs, teams


def parse_groups(path):
    groups = {}
    files = find_toml_files(path)
    for f in files:
        toml_config = toml.load(f)
        groups.update(_extract_group_members(toml_config.get('group', [])))

    return groups


def _extract_group_members(groups):
    group_configs = OrderedDict()

    for group in groups:
        group_name = group['name']
        if group_name in group_configs.keys():
            write(f'Error: Duplicate group definition {group_name}')
            exit(1)

        group_configs[group_name] = group.get('usernames', [])

    new_elements_found = flatten_group(groups, group_configs)
    while new_elements_found:
        new_elements_found = flatten_group(groups, group_configs)

    return group_configs


def flatten_group(original_group_configs, flattened_group_configs):
    new_elements_found = False
    for group in original_group_configs:
        group_name = group['name']
        referenced_groups = group.get('groups', [])
        for referenced_group in referenced_groups:
            new_members = [m for m in flattened_group_configs[referenced_group] if
                           m not in flattened_group_configs[group_name]]
            if new_members:
                new_elements_found = True
                flattened_group_configs[group_name] += new_members
    return new_elements_found


def _parse_orgs(path, groups):
    orgs = {}
    files = find_toml_files(path)
    for f in files:
        toml_config = toml.load(f)
        orgs.update(_extract_org_configuration(toml_config.get('org', []), groups))
    return orgs


def _extract_org_configuration(orgs, groups):
    org_configs = {}
    for org in orgs:
        pattern = org['pattern']
        if pattern in org_configs.keys():
            write(f'Error: Duplicate pattern {pattern} for org configuration')
            exit(1)

        org_configs[pattern] = _extract_user_model(org, groups)

    return org_configs


def _extract_user_model(org, groups):
    org_configuration = {}

    for role in ['members', 'admins']:
        member_config = org.get(role, {})

        usernames = member_config.get('usernames', [])
        for group in member_config.get('groups', []):
            usernames += [m for m in groups[group] if m not in usernames]
        org_configuration[role] = usernames

    return org_configuration


def _parse_teams(path, groups):
    teams = {}
    files = find_toml_files(path)
    for f in files:
        toml_config = toml.load(f)
        teams.update(_extract_team_configuration(toml_config.get('team', []), groups))
    return teams


def _extract_team_configuration(teams, groups):
    team_configs = {}
    for team in teams:
        name = team['name']
        if name in team_configs.keys():
            write(f'Error: Duplicate team definition {name}')
            exit(1)
        team_configs[name] = _team_configuration(team, groups)

    return team_configs


def _team_configuration(team, groups):
    team_config = _extract_user_model(team, groups)
    repository_access_rules = team.get('repos', [])

    team_config['repos'] = {repo_access['pattern']: repo_access['permission'] for repo_access in
                            repository_access_rules}
    return team_config
