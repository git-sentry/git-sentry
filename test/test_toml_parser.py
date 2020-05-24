import pprint

import pytest

from constants import ROOT_DIR
from git_sentry.parsing.toml_parser import parse_groups, parse_toml_configuration


class TestTomlParser:

    def test_valid_toml_groups(self):
        groups = parse_groups(f'{ROOT_DIR}/test/valid_toml')
        assert groups == {
            'Musicians': ['Jimmy Hendrix', 'Bob Dylan', 'Keith Richards', 'Eminem'],
            'Rolling Stones': ['Mick Jagger', 'Keith Richards', 'Ronnie Woods', 'Charlie Watts'],
            'Seen Live': ['Keith Richards', 'Mick Jagger', 'Ronnie Woods', 'Charlie Watts'],
            'Friends': ['Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe']
        }

    def test_valid_toml_orgs(self):
        orgs, _ = parse_toml_configuration(f'{ROOT_DIR}/test/valid_toml')
        assert orgs == {
            'Artists': {
                'members': ['Adele',
                            'Mick Jagger', 'Keith Richards', 'Ronnie Woods', 'Charlie Watts',  # Rolling Stones
                            # Musicians - Richards, as already mentioned with Rolling Stones above
                            'Jimmy Hendrix', 'Bob Dylan', 'Eminem',
                            'Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe'],  # Friends
                'admins': ['Jimmy Hendrix', 'Bob Dylan', 'Keith Richards', 'Eminem']  # Musicians]
            },
            'Friends Forever': {
                'members': ['Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe'],
                'admins': ['Chandler', 'Joey', 'Ross', 'Monica', 'Rachel', 'Phoebe']
            }
        }

    def test_valid_toml_teams(self):
        _, teams = parse_toml_configuration(f'{ROOT_DIR}/test/valid_toml')
        assert teams == {
            "Chandler's": {
                'members': ['Joey', 'Rachel'],
                'admins': ['Chandler'],
                'repos': {'turkey/sandwich': 'push', 'dinner/pizza': 'admin'}
            },
            "Monica's": {
                'admins': [],
                'members': ['Joey', 'Ross', 'Chandler', 'Monica', 'Rachel', 'Phoebe'],
                'repos': {},
            }
        }

    def test_invalid_groups_toml(self):
        with pytest.raises(SystemExit):
            parse_groups(f'{ROOT_DIR}/test/invalid_groups_toml')

    def test_invalid_orgs_toml(self):
        with pytest.raises(SystemExit):
            parse_toml_configuration(f'{ROOT_DIR}/test/invalid_orgs_toml')

    # def test_invalid_team_toml(self):
    #     # with pytest.raises(SystemExit):
    #     _, teams = parse_toml_configuration(f'{ROOT_DIR}/test/invalid_team_toml')
    #     pprint.pprint(teams)
