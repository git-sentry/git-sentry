import re

from github3 import login, enterprise_login

from git_sentry.configuration.config_reader import read_config

git_client = None


class GitClient:
    def __init__(self):
        self._git_client = _connect()

    def me(self):
        return self._git_client.me()

    def search_orgs(self, query):
        orgs = self._git_client.organizations()

        regex = re.compile(query)
        matching_orgs = [org for org in orgs if regex.match(org.login)]
        return matching_orgs

    def search_repos(self, query):
        orgs, *repos = query.split('/')

        matching_orgs = self.search_orgs(orgs)
        if repos:
            repos = repos[0]
            regex = re.compile(repos)
            matching_repos = [r for org in matching_orgs for r in org.repositories() if regex.match(r.name)]
            return matching_repos
        return []


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
