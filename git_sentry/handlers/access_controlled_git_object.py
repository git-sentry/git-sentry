from git_sentry.handlers.named_git_object import NamedGitObject


class AccessControlledGitObject(NamedGitObject):
    def __init__(self, git_object):
        super().__init__(git_object)

    def grant_access(self, username, role='member'):
        pass

    def revoke_access(self, username):
        pass

    def members(self, role=None):
        pass

    def permission_for(self, username):
        pass
