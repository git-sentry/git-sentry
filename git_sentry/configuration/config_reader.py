import configparser
import os

import click

CONFIG_FILE_PATH = os.path.expanduser('~/.config/sentry/sentry.ini')


def read_config():
    config_parser = configparser.ConfigParser()
    if not os.path.isfile(CONFIG_FILE_PATH):
        os.makedirs(os.path.dirname(CONFIG_FILE_PATH))
        github_instance = click.prompt('Github instance URL', default='github.com')
        token = click.prompt('Token', hide_input=True)
        config_parser[github_instance] = {'token': token}
        with open(CONFIG_FILE_PATH, 'w') as config_file:
            config_parser.write(config_file)

    config_parser.read(CONFIG_FILE_PATH, encoding='utf-8')

    return [(section, config_parser[section]['token']) for section in config_parser.sections()]
