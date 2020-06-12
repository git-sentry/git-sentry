from unittest import mock

from github3.orgs import ShortOrganization, ShortTeam
from github3.repos import ShortRepository
from github3.users import ShortUser

from git_sentry.handlers.git_org import GitOrg
from git_sentry.handlers.git_repo import GitRepo
from git_sentry.handlers.git_team import GitTeam
from git_sentry.handlers.git_user import GitUser


def mock_org(org_name, number_of_repos=0, owner=None, team_names=None):
    if not team_names:
        team_names = []

    mocked_org = mock.Mock(spec=ShortOrganization)
    mocked_org.login = org_name
    mocked_org.name = org_name

    existing_members = []
    existing_admins = []
    repositories = []
    teams = [mock_team(team_name, org_name) for team_name in team_names]

    for i in range(number_of_repos):
        repo = mock_repo(org_name, f'repo{i}')
        repo.archived = False
        repositories.append(repo.raw_object())

    mocked_org.repositories.return_value = repositories
    if owner:
        existing_admins += [owner]

    def members(role=None):
        final_members = existing_admins + existing_members

        if role == 'admin':
            final_members = existing_admins
        if role == 'members':
            final_members = existing_members

        return [mock_user(m).raw_object() for m in final_members]

    def add_member(raw_mock_member, role=None):
        if not role:
            role = 'member'

        if role == 'member':
            if raw_mock_member not in existing_admins:
                existing_members.append(raw_mock_member)
        else:
            existing_admins.append(raw_mock_member)
            if raw_mock_member in existing_members:
                existing_members.remove(raw_mock_member)

    def new_team(team_name, repo_names=None, permission=None, privacy=None, description=None):
        mocked_team = mock_team(team_name, mocked_org.login)
        if mocked_team not in teams:
            teams.append(mocked_team)

    def get_teams():
        return [t.raw_object() for t in teams]

    def retrieve_membership(raw_mock_member):
        if raw_mock_member in existing_admins:
            return {'role': 'admin'}
        if raw_mock_member in existing_members:
            return {'role': 'member'}
        return {'role': 'None'}

    mocked_org.members.side_effect = members
    mocked_org.add_or_update_membership.side_effect = add_member
    mocked_org.teams.side_effect = get_teams
    mocked_org.create_team.side_effect = new_team
    mocked_org.membership_for.side_effect = retrieve_membership
    return GitOrg(mocked_org)


def mock_repo(parent, repo_name):
    mocked_repo = mock.MagicMock(spec=ShortRepository)
    mocked_repo.name = repo_name
    mocked_repo.login = repo_name
    mocked_repo.full_name = f'{parent}/{repo_name}'

    return GitRepo(mocked_repo)


def mock_user(login):
    mocked_user = mock.MagicMock(spec=ShortUser)
    mocked_user.login = login
    mocked_user.name = login

    return GitUser(mocked_user)


def mock_team(team_name, organization):
    mocked_team = mock.Mock(spec=ShortTeam)

    mocked_team.login = team_name
    mocked_team.name = team_name
    mocked_team.organization = organization
    members = []
    maintainers = []
    repos = {}

    def add_member(raw_mock_member, role=None):
        if not role:
            role = 'member'
        if role == 'member':
            if raw_mock_member not in maintainers and raw_mock_member not in members:
                members.append(raw_mock_member)
        else:
            if raw_mock_member not in maintainers:
                maintainers.append(raw_mock_member)
            if raw_mock_member in members:
                members.remove(raw_mock_member)

    def get_members(role=None):
        final_members = maintainers + members

        if role == 'maintainer':
            final_members = maintainers
        if role == 'member':
            final_members = members

        return [mock_user(m).raw_object() for m in final_members]

    def add_to_repo(mock_repo, permission):
        # TODO: This needs to match the API call
        repos[mock_repo] = permission

    def get_repos():
        return [mock_repo(organization, repo).raw_object() for repo in repos.keys()]

    mocked_team.add_or_update_membership.side_effect = add_member
    mocked_team.add_repository.side_effect = add_to_repo
    mocked_team.members.side_effect = get_members
    mocked_team.repositories.side_effect = get_repos

    return GitTeam(mocked_team)
