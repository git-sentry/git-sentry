import glob
import os
import pprint
import typing
from collections import OrderedDict

import toml
from git_sentry.logging.printer import write
from git_sentry.parsing.group_config import GroupConfig
from git_sentry.parsing.org_config import OrgConfig
from git_sentry.parsing.team_config import TeamConfig


def find_toml_files(path):
    return glob.glob(f'{path}/*.toml')


OrgConfigurations = typing.Dict[str, OrgConfig]


def parse_toml_configuration(path) -> OrgConfigurations:
    groups = parse_groups(path)
    orgs = _parse_orgs(path, groups)
    return orgs


def parse_groups(path):
    groups = {}
    files = find_toml_files(path)
    for f in files:
        toml_config = toml.load(f)
        groups.update(_extract_group_members(toml_config.get('group', [])))

    flattened_group_configs = {group_name: group_config.flattened(groups) for (group_name, group_config) in
                               groups.items()}
    return flattened_group_configs


def _extract_group_members(groups):
    group_configs = OrderedDict()

    for group in groups:
        group_name = group['name']
        if group_name in group_configs.keys():
            write(f'Error: Duplicate group definition {group_name}')
            exit(1)

        group_conf = GroupConfig(group_name, group.get('usernames', []), group.get('groups', []))
        group_configs[group_name] = group_conf

    return group_configs


def _parse_orgs(path, groups):
    orgs = {}
    files = find_toml_files(path)
    for f in files:
        toml_config = toml.load(f)
        orgs.update(_extract_org_configuration(toml_config.get('org', []), groups))
    return orgs


def _flatten_members(original_config, groups):
    usernames = original_config.get('usernames', [])
    for group_name in original_config.get('groups', []):
        usernames += [user for user in groups[group_name].usernames() if user not in usernames]
    return usernames


def _extract_org_configuration(orgs, groups):
    org_configs = {}
    for org in orgs:
        pattern = org['pattern']

        if pattern in org_configs.keys():
            write(f'Error: Duplicate pattern {pattern} for org configuration')
            exit(1)

        members = _flatten_members(org.get('members', {}), groups)
        admins = _flatten_members(org.get('admins', {}), groups)

        teams = {}
        for team_config in org.get('team', []):
            flat_members = _flatten_members(team_config.get('members', {}), groups)
            flat_admins = _flatten_members(team_config.get('admins', {}), groups)
            repos = {repo_config['pattern']: repo_config['permission'] for repo_config in
                     team_config.get('repo', [])}
            configuration = TeamConfig(flat_members, flat_admins, repos)
            teams[team_config['name']] = configuration

        org_config = OrgConfig(pattern, members, admins, teams)

        org_configs[pattern] = org_config

    return org_configs


if __name__ == '__main__':
    config_path = os.path.expanduser('~/workspace/git-me-up')
    orgs = parse_toml_configuration(config_path)
    print(list(orgs.values())[0])
