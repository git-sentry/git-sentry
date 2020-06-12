from test.handlers.mock_helpers.mock_helpers import mock_org, mock_team, mock_user


class TestOrgTeams:

    def test_initial_org_has_no_teams(self):
        target_org = mock_org('target-org')

        assert target_org.teams() == []
        assert target_org.team('Any Name') is None

    def test_team_with_initial_teams_has_them(self):
        target_org = mock_org('target-org', team_names=['Read', 'Write', 'Admin'])

        read = mock_team('Read', target_org.raw_object())
        write = mock_team('Write', target_org.raw_object())
        admin = mock_team('Admin', target_org.raw_object())

        org_teams = target_org.teams()
        assert org_teams == [read, write, admin]

        for actual_team in org_teams:
            assert actual_team.repositories() == []
        assert read.members() == []

    def test_adding_team_to_org(self):
        target_org = mock_org('target-org', team_names=['Read', 'Write'])

        read = mock_team('Read', target_org.raw_object())
        write = mock_team('Write', target_org.raw_object())

        assert target_org.teams() == [read, write]

        target_org.create_team('Admin')

        admin = mock_team('Admin', target_org.raw_object())
        assert target_org.teams() == [read, write, admin]

    def test_adding_existing_team_to_org(self):
        target_org = mock_org('target-org', team_names=['Read', 'Write'])

        read = mock_team('Read', target_org.raw_object())
        write = mock_team('Write', target_org.raw_object())

        assert target_org.teams() == [read, write]

        target_org.create_team('Read')

        assert target_org.teams() == [read, write]

    def test_team_not_in_repos_until_added(self):
        target_org = mock_org('target_org', number_of_repos=2, team_names=['Team1'])
        team1 = target_org.team('Team1')

        assert team1.name() == 'Team1'
        assert team1.repositories() == []

        repo1, repo2 = target_org.repositories()

        team1.add_to_repo(repo1, 'maintainer')
        assert team1.repositories() == [repo1]

    def test_adding_new_members(self):
        target_org = mock_org('target_org', team_names=['Team1'])
        team1 = target_org.team('Team1')

        me = mock_user('me')
        assert team1.members() == []

        team1.grant_access(me.login())
        assert team1.members() == [me]
        assert team1.members('member') == [me]
        assert team1.members('maintainer') == []

    def test_adding_existing_member(self):
        team1 = mock_team('Team1', mock_org('target_org', team_names=['Team1']))
        assert team1.members() == []
        me = mock_user('me')

        team1.grant_access(me.login())
        assert team1.members() == [me]

        team1.grant_access(me.login())
        assert team1.members() == [me]

    def test_promote_existing_member(self):
        team1 = mock_team('Team1', mock_org('target_org', team_names=['Team1']))
        assert team1.members() == []
        me = mock_user('me')

        team1.grant_access(me.login())
        assert team1.members() == [me]

        team1.grant_access(me.login(), 'maintainer')
        assert team1.members() == [me]
        assert team1.members(role='member') == []
        assert team1.members(role='maintainer') == [me]

    def test_demote_existing_member_does_nothing(self):
        team1 = mock_team('Team1', mock_org('target_org', team_names=['Team1']))
        assert team1.members() == []
        me = mock_user('me')

        team1.grant_access(me.login(), 'maintainer')
        assert team1.members(role='maintainer') == [me]
        assert team1.members(role='member') == []

        team1.grant_access(me.login())
        assert team1.members(role='member') == []
        assert team1.members(role='maintainer') == [me]
