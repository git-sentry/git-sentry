from __future__ import annotations

from git_sentry.logging.printer import pad


class TeamConfig:
    def __init__(self, members, admins, repos):
        self._members = members
        self._admins = admins
        self._repos = repos

    def members(self):
        return self._members

    def admins(self):
        return self._admins

    def repos(self):
        return self._repos

    def diff(self, older_config: TeamConfig):
        new_members = [m for m in self.members() if m not in older_config.members()]
        new_admins = [m for m in self.admins() if m not in older_config.admins()]

        new_repos = {r: permission for r, permission in self.repos().items() if permission != older_config.repos().get(r, None)}

        return TeamConfig(new_members, new_admins, new_repos)

    def length(self):
        return len(self.members()) + len(self.admins()) + len(self.repos())

    def __repr__(self):
        output = []
        if self.members():
            output += [pad('Members:', 1)]
            output += [pad(member, 2) for member in self.members()]

        if self.admins():
            output += [pad('Admins:', 1)]
            output += [pad(admin, 2) for admin in self.admins()]

        repo_configs = self.repos()

        if repo_configs:
            output += [pad('Repositories:', 1)]
            output += [pad(f'{repo_name} : {permission}', 2) for repo_name, permission in repo_configs.items()]
        return '\n'.join(output)

    def __eq__(self, other):
        return self.members() == other.members() and self.admins() == other.admins() and self.repos() == other.repos()
