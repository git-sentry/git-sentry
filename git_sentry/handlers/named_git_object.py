from __future__ import annotations


class NamedGitObject:
    def __init__(self, git_object):
        self._git_object = git_object

    def name(self):
        pass

    def full_name(self):
        pass

    def login(self):
        pass

    def raw_object(self):
        return self._git_object

    def __eq__(self, other: NamedGitObject) -> bool:
        return self.login() == other.login()