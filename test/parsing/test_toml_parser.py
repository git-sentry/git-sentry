import pytest

from constants import ROOT_DIR
from git_sentry.parsing.team_config import TeamConfig
from git_sentry.parsing.toml_parser import parse_groups, parse_toml_configuration


class TestTomlParser:

    def test_valid_toml_groups(self):
        groups = parse_groups(f'{ROOT_DIR}/test/parsing/valid_toml')
        assert groups == {'Musicians': ['Jimmy Hendrix', 'Bob Dylan', 'Keith Richards', 'Eminem'],
                          'Rolling Stones': ['Mick Jagger', 'Keith Richards', 'Ronnie Woods', 'Charlie Watts'],
                          'Seen Live': ['Keith Richards', 'Mick Jagger', 'Ronnie Woods', 'Charlie Watts'],
                          'Friends': ['Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe']}

    def test_valid_toml_orgs(self):
        orgs = parse_toml_configuration(f'{ROOT_DIR}/test/parsing/valid_toml')
        assert orgs == {'Artists': {
            'members': ['Adele', 'Mick Jagger', 'Keith Richards', 'Ronnie Woods', 'Charlie Watts', 'Jimmy Hendrix',
                        'Bob Dylan', 'Eminem', 'Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe'],
            'admins': ['Jimmy Hendrix', 'Bob Dylan', 'Keith Richards', 'Eminem']},
            'Friends Forever': {'members': ['Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe'],
                                'admins': ['Chandler', 'Joey', 'Ross', 'Monica', 'Rachel', 'Phoebe']}}

    def test_valid_toml_teams(self):
        orgs = parse_toml_configuration(f'{ROOT_DIR}/test/parsing/valid_toml')

        assert orgs['Friends Forever'].teams() == {"Chandler's": TeamConfig(['Joey', 'Rachel'], ['Chandler'],
                                                                            {'turkey/sandwich': 'push',
                                                                             'dinner/pizza': 'admin'}),
                                                   "Monica's": TeamConfig(
                                                       ['Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe'], [],
                                                       {})}

    def test_invalid_groups_toml(self):
        with pytest.raises(SystemExit):
            parse_groups(f'{ROOT_DIR}/test/parsing/invalid_groups_toml')

    def test_invalid_orgs_toml(self):
        with pytest.raises(SystemExit):
            parse_toml_configuration(f'{ROOT_DIR}/test/parsing/invalid_orgs_toml')

    # def test_invalid_team_toml(self):
    #     with pytest.raises(SystemExit):
    #     parse_toml_configuration(f'{ROOT_DIR}/test/parsing/invalid_team_toml')
