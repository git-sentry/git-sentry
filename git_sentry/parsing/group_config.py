from __future__ import annotations

from git_sentry.logging.printer import section


class GroupConfig:
    def __init__(self, name, usernames, groups):
        self._name = name
        self._usernames = usernames
        self._groups = groups

    def flattened(self, all_groups_configs):
        for referenced_group in self._groups:
            referenced_group_config = all_groups_configs[referenced_group]
            flattened_referenced_group_config = referenced_group_config.flattened(all_groups_configs)
            while flattened_referenced_group_config.usernames() != referenced_group_config.usernames():
                flattened_referenced_group_config = referenced_group_config.flattened(all_groups_configs)
            all_groups_configs[referenced_group] = flattened_referenced_group_config

        for referenced_group in self._groups:
            self._usernames += [user for user in all_groups_configs[referenced_group].usernames() if
                                user not in self.usernames()]

        return self

    def diff(self, older_group: GroupConfig):
        username_additions = [user for user in self.usernames() if user not in older_group.usernames()]
        group_additions = [group for group in self.groups() if group not in older_group.groups()]
        return GroupConfig(self.name(), username_additions, group_additions)

    def name(self):
        return self._name

    def usernames(self):
        return self._usernames

    def groups(self):
        return self._groups

    def __repr__(self):
        output = []
        output += [section(f'Group configuration for {self.name()}')]
        for username in self.usernames():
            output += [username]
        return '\n'.join(output)

    def __eq__(self, other):
        if isinstance(other, GroupConfig):
            return self.usernames() == other.usernames()
        if isinstance(other, list):
            return self.usernames() == other
