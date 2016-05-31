from tests import config


def setup_user_if_not_exists(user_email):
    if config.SETUP_ENVIRONMENT:
        from mist.core.user.models import User, Owner
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            user = User()
            user.email = user_email
            user.set_password(config.PASSWORD1)
            user.status = 'confirmed'
            user.save()
        return user


def remove_user_if_exists(context, user_email):
    if config.SETUP_ENVIRONMENT:
        from mist.core.user.models import Owner
        if context.mist_config.get(user_email):
            user_email = context.mist_config.get(user_email)
        try:
            Owner.objects.get(email=user_email).delete()
        except Owner.DoesNotExist:
            pass


def setup_org_if_not_exists(org_name, owner_email, clean_org=True):
    # If clean_org is set to True then all the teams of the organization
    # will be deleted and all the members except the owner.
    if config.SETUP_ENVIRONMENT:
        owner = setup_user_if_not_exists(owner_email)
        from mist.core.user.models import Organization
        try:
            org = Organization.objects.get(name=org_name)
        except Organization.DoesNotExist:
            org = Organization()
        if clean_org:
            i = 0
            while len(org.teams) > 1:
                if org.teams[i].name != 'Owners':
                    team = org.teams.pop(i)
                    team.delete()
                else:
                    while len(team.members) > 0:
                        team.members.pop()
                    i += 1
            while len(org.members) > 0:
                org.members.pop()
        org.add_member_to_team('Owners', owner)
        org.save()
        return org, owner


def setup_team(org_name, team_name, team_members=[], clean_policy=True):
    if config.SETUP_ENVIRONMENT:
        from mist.core.user.models import Team
        from mist.core.user.models import Organization
        org = Organization.objects(name=org_name).get()
        team_found = False
        for team in org.teams:
            if team.name == team_name:
                team_found = True
                if clean_policy:
                    while len(team.policy.rules) > 0:
                        team.policy.rules.pop()
                break

        if not team_found:
            team = Team()
            team.name = team_name
            org.teams.append(team)

        for team_member in team_members:
            org.add_member_to_team(team_name, team_member)

        org.save()
        return org


def setup_team_members(org_name, team_name, team_members=[]):
    if config.SETUP_ENVIRONMENT:
        from mist.core.user.models import Team
        from mist.core.user.models import Organization
        org = Organization.objects(name=org_name).get()
        for team_member in team_members:
            org.add_member_to_team(team_name, team_member)
        org.save()

