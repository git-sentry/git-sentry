import configparser
import os

import click

CONFIG_FILE_PATH = os.path.expanduser('~/.config/sentry/sentry.ini')


def read_config():
    token = os.environ.get('GIT_TOKEN', default=None)
    git_instance = os.environ.get('GIT_URL', default=None)
    if token is None or git_instance is None:
        print(token, git_instance)
        config_parser = configparser.ConfigParser()
        if not os.path.isfile(CONFIG_FILE_PATH):
            if not os.path.isdir(os.path.dirname(CONFIG_FILE_PATH)):
                os.makedirs(os.path.dirname(CONFIG_FILE_PATH))
            github_instance = click.prompt('Github instance URL', default='github.com')
            token = click.prompt('Token', hide_input=True)
            config_parser[github_instance] = {'token': token}
            with open(CONFIG_FILE_PATH, 'w') as config_file:
                config_parser.write(config_file)

        config_parser.read(CONFIG_FILE_PATH, encoding='utf-8')
        config = [(section, config_parser[section]['token']) for section in config_parser.sections()]
        git_instance, token = config[0]

    return [(git_instance, token)]
