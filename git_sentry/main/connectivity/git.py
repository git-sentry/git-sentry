import re

from git_sentry.configuration.config_reader import read_config
from git_sentry.handlers.git_org import GitOrg
from git_sentry.handlers.git_repo import GitRepo
from github3 import login, enterprise_login

git_client = None


class GitClient:
    def __init__(self):
        self._git_client = _connect()
        self._orgs = None
        self._repos = None

    def me(self):
        return self._git_client.me()

    def search_orgs(self, query):
        if self._orgs is None:
            self._orgs = self._git_client.organizations()

        regex = re.compile(query)
        matching_orgs = [GitOrg(org) for org in self._orgs if regex.match(org.login)]
        return matching_orgs

    def search_repos(self, query):
        if self._repos is None:
            self._repos = self._git_client.repositories()

        regex = re.compile(query)

        matching_repos = [GitRepo(repo) for repo in self._repos if regex.match(repo.full_name)]

        return matching_repos

    def organization(self, org_login):
        org = self._git_client.organization(org_login)
        if org is not None:
            return GitOrg(org)
        return None


def _connect():
    global git_client
    if not git_client:
        git_credentials = read_config()
        github_url, github_token = git_credentials[0]
        if github_url == 'github.com':
            git_client = login(token=github_token)
        else:
            git_client = enterprise_login(url=f'https://{github_url}', token=github_token)
    return git_client
