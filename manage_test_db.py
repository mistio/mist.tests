import logging
import argparse
from time import time
from time import sleep
import mongoengine as me

from mist.core import config

from mist.core.user.models import User
from mist.core.user.models import Owner
from mist.core.user.models import Organization

from mist.core.keypair.models import Keypair

from mist.core.cloud.models import Cloud
from mist.core.cloud.models import Machine

from mist.core.tag.models import Tag
from mist.core.rule.models import Rule
from mist.io.scripts.models import Script


log = logging.getLogger(__name__)


def add_user(email, password, first_name, last_name):
    log.info("Adding user %s" % email)
    try:
        user = User.objects.get(email=email)
        clean_owner(user)
    except:
        user = User()
        user.email = email
        user.activation_time = time()
        user.registration_time = time()
        user.save()

    user.first_name = first_name
    user.last_name = last_name
    user.last_login = time()
    user.status = 'confirmed'
    user.set_password(password)
    user.save()


# create/set an org with name
def add_org(owner, name):
    if not isinstance(owner, Owner):
        if isinstance(owner, basestring):
            if '@' in owner:
                owner = User.objects.get(email=owner)
            else:
                owner = Owner.objects.get(id=owner)
    log.info("Adding organization to owner with id %s" % owner.id)

    try:
        org = Organization.objects.get(name=name)
        clean_owner(owner)
    except:
        org = Organization()
    org.add_member_to_team('Owners', owner)
    org.name = name
    org.save()


def delete_user(email):
    log.info("Deleting user %s" % email)
    try:
        User.objects.get(email=email).delete()
    except:
        pass
    log.info("User %s deleted" % email)


def delete_org_by_name(name):
    # delete an organization and all it's resources
    try:
        org = Organization.objects.get(name=name)
        clean_owner(org)
        org.delete()
    except:
        pass


def clean_owner(owner):
    if not isinstance(owner, Owner):
        if isinstance(owner, basestring):
            if '@' in owner:
                owner = User.objects.get(email=owner)
            else:
                owner = Owner.objects.get(id=owner)
    log.info("Cleaning owner with id %s" % owner.id)

    clouds = Cloud.objects(owner=owner)
    for cloud in clouds:
        machines = Machine.objects(cloud=cloud)
        for machine in machines:
            machine.delete()
    clouds.delete()
    keypairs = Keypair.objects(owner=owner)
    keypairs.delete()
    scripts = Script.objects(owner=owner)
    scripts.delete()
    rules = Rule.objects(owner=owner)
    rules.delete()
    tags = Tag.objects(owner=owner)
    tags.delete()


def clean_db():
    log.info("Cleaning db")
    Cloud.drop_collection()
    Owner.drop_collection()
    Machine.drop_collection()
    Keypair.drop_collection()
    Tag.drop_collection()
    Script.drop_collection()


class FixCreateUsersAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            setattr(namespace, self.dest, True)
        else:
            setattr(namespace, self.dest, int(values[0]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--add-user', type=str, action='append', default=[])
    parser.add_argument('--clean-user', type=str, action='append', default=[])
    parser.add_argument('--delete-user', type=str, action='append', default=[])
    parser.add_argument('--clean-org', type=str, action='append', default=[])
    parser.add_argument('--delete-org', type=str, action='append', default=[])
    parser.add_argument('--delete-db', action='store_true', default=False)

    params = parser.parse_known_args()[0]

    t_end = time() + 60
    conFlag = False
    while time() < t_end:
        log.info("Trying to connect to mongo")
        try:
            me.connect(db="mist2",
                       host=config.MONGO_URI)
            conFlag = True
            break
        except:
            log.info("Mongo not accessible yet")
            sleep(2)

    if not conFlag:
        exit(-1)

    log.info("Connection to mongo, succeeded!")

    for user in params.add_user:
        user_data = user.split(':')
        user_data.extend([''] * (4 - len(user_data)))
        email, name, pass1, pass2 = user_data[0], user_data[1], user_data[2], user_data[3]
        first, sep, last = name.rpartition(' ')
        add_user(email, pass1, first, last)

    for user in params.clean_user:
        clean_owner(user)

    for user in params.delete_user:
        delete_user(user)

    for user in params.clean_org:
        clean_owner(user)
