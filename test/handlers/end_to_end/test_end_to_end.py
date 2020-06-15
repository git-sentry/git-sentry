import os
from unittest import mock

import pytest
from github3 import GitHub

from constants import ROOT_DIR
from git_sentry.handlers.git_config import apply_configuration
from git_sentry.main.connectivity.git import GitClient
from git_sentry.parsing import toml_parser
from test.handlers.mock_helpers.mock_helpers import mock_user, mock_org


@pytest.fixture(scope="module")
def git_client():
    mocked_client = mock.Mock(spec=GitHub)
    iron_man = mock_user('Iron Man')
    professor_hulk = mock_user('Professor Hulk')

    mocked_client.me.return_value = iron_man.raw_object()

    training_org = mock_org('training', 3, owner=iron_man.login(), team_names=['read'])
    tools_org = mock_org('tools', 5, owner=iron_man.login(), team_names=['read', 'write'])
    lab_org = mock_org('lab', 2, owner=professor_hulk.login(), team_names=['doctors', 'not-doctors'])

    all_orgs = {org.login(): org for org in [training_org, tools_org, lab_org]}
    mocked_client.organizations.return_value = [mocked_org.raw_object() for mocked_org in all_orgs.values()]

    all_repositories = []
    for org in [training_org, tools_org, lab_org]:
        all_repositories += org.repositories()

    mocked_client.repositories.return_value = [repo.raw_object() for repo in all_repositories]

    mocked_client.organization.side_effect = lambda org_login: all_orgs.get(org_login,
                                                                            mock_org('Not an org')).raw_object()

    return GitClient(mocked_client)


class TestEndToEnd:
    def test_git_object(self, git_client):
        assert git_client.me().login() == 'Iron Man'

        assert [org.login() for org in git_client.search_orgs('.*')] == ['training', 'tools', 'lab']
        assert [repo.login() for repo in git_client.search_repos('tools/.*')] == ['repo0', 'repo1', 'repo2', 'repo3',
                                                                                  'repo4']
        assert git_client.organization('tools').login() == 'tools'
        assert git_client.organization('random').login() == 'Not an org'

    def test_config(self):
        org_configurations = toml_parser.parse_toml_configuration(
            os.path.expanduser(f'{ROOT_DIR}/test/handlers/end_to_end/toml_config'))
        assert len(org_configurations) == 3

    def test_end_to_end(self, git_client):
        org_configurations = toml_parser.parse_toml_configuration(os.path.expanduser(f'{ROOT_DIR}/test/handlers/end_to_end/toml_config'))
        print()
        apply_configuration(git_client, org_configurations, False)
        training_org = git_client.organization('training')
        tools_org = git_client.organization('tools')
        lab_org = git_client.organization('lab')

        check_training_org(training_org)
        check_tools_org(tools_org)
        check_lab_org(lab_org)


def check_training_org(training_org):
    assert {team.name() for team in training_org.teams()} == {'read', 'write'}

    check_members(training_org.members(role='member'), {'Bruce Banner', 'Black Widow', 'Hawkeye'})
    check_members(training_org.members(role='admin'), {'Iron Man', 'Captain America', 'Thor'})

    training_org_read = training_org.team('read')

    check_members(training_org_read.members(role='member'), {'Bruce Banner', 'Black Widow', 'Hawkeye'})
    check_members(training_org_read.members(role='maintainer'), {'Iron Man', 'Captain America', 'Thor'})

    for repository in training_org_read.repositories():
        assert repository.permission_for_team(training_org_read.login()) == 'pull'

    training_org_write = training_org.team('write')

    check_members(training_org_write.members(role='member'), {})
    check_members(training_org_write.members(role='maintainer'), {'Captain America'})

    for repository in training_org_write.repositories():
        assert repository.permission_for_team(training_org_write.login()) == 'push'


def check_tools_org(tools_org):
    assert {team.name() for team in tools_org.teams()} == {'read', 'write'}

    check_members(tools_org.members(role='member'), {'Bruce Banner', 'Black Widow', 'Hawkeye'})
    check_members(tools_org.members(role='admin'), {'Iron Man', 'Captain America', 'Thor'})

    tools_org_read = tools_org.team('read')

    check_members(tools_org_read.members(role='member'), {'Bruce Banner', 'Black Widow', 'Hawkeye'})
    check_members(tools_org_read.members(role='maintainer'), {'Iron Man', 'Captain America', 'Thor'})

    for repository in tools_org_read.repositories():
        assert repository.permission_for_team(tools_org_read.login()) == 'pull'

    tools_org_write = tools_org.team('write')

    check_members(tools_org_write.members(role='member'), {})
    check_members(tools_org_write.members(role='maintainer'), {'Captain America'})

    for repository in tools_org_write.repositories():
        assert repository.permission_for_team(tools_org_write.login()) == 'push'


def check_lab_org(lab_org):
    assert {team.name() for team in lab_org.teams()} == {'read', 'doctors', 'not-doctors'}

    check_members(lab_org.members(role='member'), {'Thor', 'Black Widow', 'Hawkeye'})
    check_members(lab_org.members(role='admin'), {'Iron Man', 'Captain America', 'Bruce Banner', 'Professor Hulk'})

    lab_org_read = lab_org.team('read')
    check_members(lab_org_read.members(role='member'), {'Bruce Banner', 'Black Widow', 'Hawkeye'})
    check_members(lab_org_read.members(role='maintainer'), {'Iron Man', 'Captain America', 'Thor'})
    for repository in lab_org_read.repositories():
        assert repository.permission_for_team(lab_org_read.login()) == 'pull'

    lab_org_doctors = lab_org.team('doctors')
    check_members(lab_org_doctors.members(role='member'), {'Iron Man', 'Bruce Banner'})
    check_members(lab_org_doctors.members(role='maintainer'), {})
    for repository in lab_org_doctors.repositories():
        assert repository.permission_for_team(lab_org_doctors.login()) == 'admin'

    lab_org_not_doctors = lab_org.team('not-doctors')
    check_members(lab_org_not_doctors.members(role='member'), {'Thor', 'Captain America', 'Black Widow', 'Hawkeye'})
    check_members(lab_org_not_doctors.members(role='maintainer'), {})
    for repository in lab_org_not_doctors.repositories():
        assert repository.permission_for_team(lab_org_not_doctors.login()) == 'pull'


def check_members(member_list, expected):
    assert {member.login() for member in member_list} == set(expected)
