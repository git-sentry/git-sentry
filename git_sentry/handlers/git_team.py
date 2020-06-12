from git_sentry.handlers.access_controlled_git_object import AccessControlledGitObject
from git_sentry.handlers.git_repo import GitRepo
from git_sentry.handlers.git_user import GitUser


class GitTeam(AccessControlledGitObject):
    def __init__(self, git_object):
        super().__init__(git_object)

    def name(self):
        return self._git_object.name

    def login(self):
        return self.name()

    def as_dict(self):
        return self._git_object.as_json()

    def add_to_repo(self, repo, permission):
        self._git_object.add_repository(repo.login(), permission)

    def repositories(self):
        return [GitRepo(r) for r in self._git_object.repositories()]

    def grant_access(self, user, role='member'):
        if self.permission_for(user) != 'maintainer':
            self._git_object.add_or_update_membership(user, role)

    def revoke_access(self, username):
        super().revoke_access(username)

    def members(self, role=None):
        return [GitUser(u) for u in self._git_object.members(role)]

    def permission_for(self, username):
        if any(m.login() == username for m in self.members('maintainer')):
            return 'maintainer'
        if any(m.login() == username for m in self.members('member')):
            return 'member'
        return None

    def __eq__(self, other):
        return self.name() == other.name()

    def __repr__(self):
        return f'GitTeam[{self.name()}]'

    def __str__(self):
        return f'GitTeam[{self.name()}]'
