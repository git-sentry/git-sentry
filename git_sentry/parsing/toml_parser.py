import glob
import pprint
from collections import OrderedDict

import toml

from git_sentry.logging.printer import write


def find_toml_files(path):
    return glob.glob(f'{path}/*.toml')


def parse_toml_configuration(path):
    files = find_toml_files(path)
    groups = _parse_groups(files)
    orgs = _parse_orgs(files, groups)
    pprint.pprint(orgs)


def _parse_groups(files):
    groups = {}
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

def _parse_orgs(files, groups):
    orgs = {}
    for f in files:
        toml_config = toml.load(f)
        orgs.update(_extract_org_configuration(toml_config.get('org', []), groups))
    return orgs

def _extract_org_configuration(orgs, groups):
    org_configs = {}
    for org in orgs:
        pattern = org['pattern']
        if pattern in org_configs.keys():
            write(f'Error: Duplicate pattern {pattern}')
            exit(1)
        org_configs[pattern] = {}
        org_configs[pattern]['members'] = _org_membership_config(org, 'members', groups)
        org_configs[pattern]['admins'] = _org_membership_config(org, 'admins', groups)

    return org_configs


def _org_membership_config(org, role, groups):
    member_config = org.get(role, {})

    usernames = member_config.get('usernames', [])
    for group in member_config.get('groups', []):
        usernames += groups[group]
    return usernames