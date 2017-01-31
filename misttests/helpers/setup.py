import json
import requests
import logging

from misttests import config

from misttests.api.core.core import MistCoreApi

# def setup_user_if_not_exists(user_email, password=None):
#     if config.SETUP_ENVIRONMENT:
#         from mist.io.users.models import User, Owner
#         try:
#             user = User.objects.get(email=user_email)
#         except User.DoesNotExist:
#             user = User()
#             user.email = user_email
#         if not password:
#             password = config.PASSWORD1
#         user.set_password(password)
#         user.status = 'confirmed'
#         user.save()
#         return user


def setup_user_if_not_exists(email, password):

    #import ipdb;ipdb.set_trace()
    payload = {
        'email': config.OWNER_EMAIL,
        'password': config.OWNER_PASSWORD,
        'name': "Atheofovos Gkikas",
        'request_demo': False
    }

    print "The user used for API tests is " + config.OWNER_EMAIL
    print "The password used for API tests is " + config.OWNER_PASSWORD

    re = requests.post("%s/api/v1/dev/register" % config.MIST_URL, data=json.dumps(payload))
    return


def remove_user_if_exists(core_uri, user_email):
    url = "%s/api/v1/dev/users" % core_uri
    payload = {
        "email": user_email
    }

    re = requests.delete(url, data=json.dumps(payload))


def setup_org_if_not_exists(org_name, owner_email, clean_org=True, add_cloud=True):
    # If clean_org is set to True then all the teams of the organization
    # will be deleted and all the members except the owner.
    if config.SETUP_ENVIRONMENT:
        from mist.io.clouds.models import Cloud
        from mist.io.machines.models import Machine

        from mist.io.users.models import User
        from mist.io.users.models import Organization
        owner = User.objects.get(email=owner_email)
        try:
            org = Organization.objects.get(name=org_name)
        except Organization.DoesNotExist:
            org = Organization()
            org.name = org_name
        if clean_org:
            i = 0
            while len(org.teams) > 1:
                if org.teams[i].name != 'Owners':
                    org.teams.pop(i)
                else:
                    while len(org.teams[i].members) > 0:
                        org.teams[i].members.pop()
                    i += 1
            while len(org.members) > 0:
                org.members.pop()
        org.add_member_to_team('Owners', owner)
        org.save()

        if add_cloud:
            try:
                Cloud.objects.get(owner=org, title=config.API_TESTING_CLOUD)
            except Cloud.DoesNotExist:
                import mist.io.clouds.models as clouds_models
                kwargs = {'owner': org, 'title': config.API_TESTING_CLOUD}

                if config.API_TESTING_CLOUD_PROVIDER == 'EC2':
                    apikey = config.CREDENTIALS['EC2']['api_key']
                    apisecret = config.CREDENTIALS['EC2']['api_secret']
                    region = 'ec2_ap_northeast'
                    clouds_models.AmazonCloud(apikey=apikey,
                                              apisecret=apisecret,
                                              region=region, **kwargs).save()
                elif config.API_TESTING_CLOUD_PROVIDER == 'DOCKER':
                    host = config.CREDENTIALS['DOCKER']['host']
                    port = config.CREDENTIALS['DOCKER']['port']
                    clouds_models.DockerCloud(host=host, port=port,
                                              **kwargs).save()
                elif config.API_TESTING_CLOUD_PROVIDER == 'BARE_METAL':
                    host = [config.CREDENTIALS['BARE_METAL']['public_ips']]
                    cloud = clouds_models.OtherCloud(host=host, rdp_port=3389,
                                                     ssh_user='root',
                                                     ssh_port=22,
                                                     **kwargs)
                    cloud.save()
                    machine = Machine()
                    machine.cloud = cloud
                    machine.ssh_port = 22
                    machine.public_ips = [
                        config.CREDENTIALS['BARE_METAL']['public_ips']]
                    machine.private_ips = [
                        config.CREDENTIALS['BARE_METAL']['private_ips']]
                    machine.machine_id = config.API_TESTING_CLOUD.replace('.',
                                                                          '').replace(
                        ' ', '')
                    machine.name = config.API_TESTING_CLOUD
                    machine.os_type = 'unix'
                    machine.save()


def setup_team(org_name, team_name, team_members=[], clean_policy=True):
    if config.SETUP_ENVIRONMENT:
        from mist.io.users.models import User
        from mist.io.users.models import Team
        from mist.io.users.models import Organization
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
            org.add_member_to_team(team_name, User.objects.get(email=team_member))

        org.save()
        return org.get_team(team_name).id


def setup_team_members(org_name, team_name, team_members=[]):
    if config.SETUP_ENVIRONMENT:
        from mist.io.users.models import Team
        from mist.io.users.models import Organization
        org = Organization.objects(name=org_name).get()
        for team_member in team_members:
            org.add_member_to_team(team_name, team_member)
        org.save()
