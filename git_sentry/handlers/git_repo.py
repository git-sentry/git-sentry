from git_sentry.handlers.access_controlled_git_object import AccessControlledGitObject


class GitRepo(AccessControlledGitObject):
    def __init__(self, git_object):
        super().__init__(git_object)

    def name(self):
        return self._git_object.name

    def full_name(self):
        return self._git_object.full_name

    def login(self):
        return self.name()

    def as_dict(self):
        return self._git_object.as_dict()

    def permission_for_team(self, team):
        permissions = self.as_dict().get('permissions', {})
        if permissions.get('admin', False):
            return 'admin'
        elif permissions.get('push', False):
            return 'push'
        elif permissions.get('pull', False):
            return 'pull'
        else:
            return None

    def raw_object(self):
        return self._git_object

    def owner(self):
        return self._git_object.owner

    def __eq__(self, other):
        return self.login() == other.login()

    def __repr__(self):
        return f'GitRepo[{self.full_name()}]'

    def __str__(self):
        return f'GitRepo[{self.full_name()}]'
