from test.handlers.mock_helpers.mock_helpers import mock_org, mock_user


class TestOrgMembership:

    def test_org_with_no_members(self):
        target_org = mock_org('target-org')

        assert target_org.members() == []

    def test_org_with_one_admin(self):
        target_org = mock_org('target-org', owner='me')

        me = mock_user('me')

        assert target_org.members() == [me]
        assert target_org.members(role='admin') == [me]

    def test_add_new_member(self):
        target_org = mock_org('target-org')
        me = mock_user('me')
        target_org.grant_access(me.login())

        assert target_org.members() == [me]

    def test_promote_new_members(self):
        target_org = mock_org('target-org')
        me = mock_user('me')

        target_org.grant_access(me.login(), role='admin')

        assert target_org.permission_for(me.login()) == 'admin'

    def test_promote_existing_members(self):
        target_org = mock_org('target-org')
        me = mock_user('me')

        target_org.grant_access(me.login())

        assert target_org.permission_for(me.login()) == 'member'

        target_org.grant_access(me.login(), role='admin')
        assert target_org.permission_for(me.login()) == 'admin'

    def test_demote_existing_admin(self):
        target_org = mock_org('target-org', owner='me')
        me = mock_user('me')

        target_org.grant_access(me.login())

        assert target_org.permission_for(me.login()) == 'admin'
