from github3 import login

from git_sentry.configuration.config_reader import read_config


def connect():
    git_credentials = read_config()
    public_github_url, public_github_token = git_credentials[0]
    git_client = login(token=public_github_token)
    return git_client