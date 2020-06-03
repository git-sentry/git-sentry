from git_sentry.handlers.access_controlled_git_object import AccessControlledGitObject


class GitRepo(AccessControlledGitObject):
    def __init__(self, git_object):
        super().__init__(git_object)

    def owner(self):
        return self._git_object.owner()

    def __eq__(self, other):
        return self.login() == other.login()