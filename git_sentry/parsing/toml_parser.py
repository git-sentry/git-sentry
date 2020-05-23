import glob
import pprint
from collections import OrderedDict

import toml

from git_sentry.logging.printer import write


def find_toml_files(path):
    return glob.glob(f'{path}/*.toml')


def read_toml_configuration(path):
    files = find_toml_files(path)
    groups = {}

    for f in files:
        write(f'Reading toml config from {f}', indent=1)
        toml_config = toml.load(f)
        if 'group' in toml_config:
            groups.update(compute_members(toml_config['group']))

    pprint.pprint(groups)


def compute_members(groups):
    group_map = OrderedDict()

    for group in groups:
        group_name = group['name']
        if group_name in group_map.keys():
            write(f'Error: Duplicate group definition {group_name}')
            exit(1)

        group_map[group_name] = []

        if 'usernames' in group:
            group_map[group_name] += group['usernames']

    new_elements = flatten_groups(groups, group_map)
    while new_elements:
        new_elements = flatten_groups(groups, group_map)

    return group_map


def flatten_groups(groups, group_map):
    added = False
    for group in groups:
        group_name = group['name']
        if 'groups' in group:
            for referenced_group in group['groups']:
                new_members = [m for m in group_map[referenced_group] if m not in group_map[group_name]]
                if new_members:
                    added = True
                    group_map[group_name] += new_members
    return added
