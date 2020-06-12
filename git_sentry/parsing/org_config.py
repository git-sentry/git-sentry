from __future__ import annotations

import re

from git_sentry.logging.printer import section, pad
from git_sentry.parsing.team_config import TeamConfig


class OrgConfig:
    def __init__(self, pattern, members, admins, teams):
        self._pattern = pattern
        self._members = members
        self._admins = admins

        self._teams = teams

    def members(self):
        return self._members

    def admins(self):
        return self._admins

    def teams(self):
        return self._teams

    def diff(self, older_config: OrgConfig):
        new_members = [m for m in self.members() if m not in older_config.members() and m not in older_config.admins()]
        new_admins = [m for m in self.admins() if m not in older_config.admins()]

        team_diff = {}
        for team_name, team_config in self.teams().items():
            if team_name not in older_config.teams().keys():
                team_diff[team_name] = team_config
            else:
                old_team_config = older_config.teams()[team_name]
                new_team_config = team_config.diff(old_team_config)
                if new_team_config.length() != 0:
                    team_diff[team_name] = new_team_config
        diff = OrgConfig(self._pattern, new_members, new_admins, team_diff)
        return diff

    def resolve(self, actual_org):
        teams_with_resolved_repositories = {}
        for team_name, team_config in self.teams().items():
            resolved_members = team_config.members()
            resolved_admins = team_config.admins()
            resolved_repos = {}
            repository_patterns = team_config.repos()

            for repo_pattern, permission in repository_patterns.items():
                regex = re.compile(repo_pattern)
                for repo in actual_org.repositories():
                    if regex.match(repo.login()):
                        resolved_repos[repo.full_name()] = permission
            teams_with_resolved_repositories[team_name] = TeamConfig(resolved_members, resolved_admins, resolved_repos)

        return OrgConfig(actual_org.login(), self._members, self._admins, teams_with_resolved_repositories)

    def length(self):
        return len(self._members) + len(self._admins) + len(self._teams)

    def __repr__(self):
        output = []
        output += [section(f'Org Config for {self._pattern}')]

        if self._members:
            output += [section('Org Members')]
            output += [pad(member, 2) for member in self._members]

        if self._admins:
            output += [section('Org Owners')]
            output += [pad(admin, 2) for admin in self._admins]

        for team, team_config in self.teams().items():
            output += [f'Team: {team}']
            output += [f'{team_config}']

        return '\n'.join(output)

    def __eq__(self, other):
        if isinstance(other, OrgConfig):
            return self.members() == other.members() and self.admins() == other.admins()

        if isinstance(other, dict):
            return self.members() == other.get('members', []) and self.admins() == other.get('admins', [])
