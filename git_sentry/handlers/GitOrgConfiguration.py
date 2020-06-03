from git_sentry.logging.printer import section, pad


class GitOrgConfiguration:
    def __init__(self, members, admins):
        self.members = members
        self.admins = admins

    def differences(self, other):
        return GitOrgConfigurationDiff(self, other)


def _compute_removals(original, updated):
    return {'members': [m.login() for m in original.members if m not in updated.members],
            'admins': [m.login() for m in original.admins if m not in updated.admins]}


def _computer_user_access_changes(original, updated):
    changes = {'to add': {}, 'to change': {}}
    for member in updated.members:
        original_members = [m.login() for m in original.members]
        original_admins = [m.login() for m in original.admins]
        if member not in original_members:
            if member not in original_admins:
                changes['to add'][member] = 'member'
    for admin in updated.admins:
        if admin not in original_admins:
            if admin not in original_members:
                changes['to add'][admin] = 'admin'
            else:
                changes['to change'][admin] = 'admin'
    return changes


class GitOrgConfigurationDiff:
    def __init__(self, current, updated):
        self.changes = _computer_user_access_changes(current, updated)

    def __len__(self):
        changes_length = len(self.changes['to add']) + len(self.changes['to change'])
        return changes_length

    def __repr__(self):

        output = [('Sentry will perform the following changes\n', 1)]
        max_addition = self._compute_max_length_of_changes()

        if self.changes['to add'].items():
            output += [(section('New entries'), 0)]

        for member, role in self.changes['to add'].items():
            output += [(f'{member}{" " * (max_addition - len(member))} : None ==> {role}\n', 1)]

        if self.changes['to change'].items():
            output += [(section('Updates'), 0)]
        for member, role in self.changes['to change'].items():
            output += [(f'{member}{" " * (max_addition - len(member))} : member ==> {role}\n', 1)]

        number_of_new_additions = len(self.changes['to add'])
        number_of_changes = len(self.changes['to change'])

        output += [(f'Apply: {number_of_new_additions} users to add, {number_of_changes} users to change\n', 0)]
        padded_outputs = [pad(text, indent) for text, indent in output]
        return ''.join(padded_outputs)

    def _compute_max_length_of_changes(self):
        max_addition = 0
        for member_add in self.changes['to add']:
            if len(member_add) > max_addition:
                max_addition = len(member_add)
        for member_add in self.changes['to change']:
            if len(member_add) > max_addition:
                max_addition = len(member_add)
        return max_addition
