from git_sentry.handlers.named_git_object import NamedGitObject


class GitUser(NamedGitObject):
    def __init__(self, git_object):
        super().__init__(git_object)

    def name(self):
        return self._git_object.name

    def full_name(self):
        return self._git_object.name

    def login(self):
        return self._git_object.login

    def get_organization_membership(self, organization):
        return organization.permission_for(self.login())

    def __str__(self):
        return f'GitUser[{self.login()}]'

    def __repr__(self):
        return f'GitUser[{self.login()}]'

    def __eq__(self, other):
        return self.login() == other.login()
