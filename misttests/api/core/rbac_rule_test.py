from pytest import raises

from misttests.api.helpers import get_random_str

from mongoengine import ValidationError

# Imports to solve dependency issues
from mist.io.clouds.models import Cloud
from mist.io.schedules.models import Schedule
from mist.io.scripts.models import Script
from mist.io.keys.models import Key
from mist.core.orchestration.models import Stack

def test_rbac_policy_rule_validation(pretty_print, email):
    from mist.core.rbac.models import Rule

    from mist.io.users.models import User
    from mist.io.users.models import Team
    from mist.io.users.models import Organization

    def rule_should_raise_exc(rule_dict, org, team):
        rule = Rule(**rule_dict)

        team.policy.rules.append(rule)
        with raises(ValidationError):
            org.save()

        team.policy.rules.remove(rule)

    org = Organization()
    org.name = get_random_str()

    user = User.objects(email=email).get()
    org.add_member_to_team('Owners', user)

    team = Team()
    team.name = get_random_str()

    org.teams.append(team)
    org.save()

    print "\n>>>  Test rule operator can only be ALLOW or DENY"
    rule_should_raise_exc(rule_dict={
        'operator': 'bla',
        'action': '',
        'rtype': '',
        'rid': '',
        'rtags': ''
    }, org=org, team=team)

    print "\n>>>  Test rule action must be at least a known one"
    rule_should_raise_exc(rule_dict={
        'operator': 'ALLOW',
        'action': 'bla',
        'rtype': '',
        'rid': '',
        'rtags': ''
    }, org=org, team=team)

    print "\n>>>  Test rule rtype must be a known one"
    rule_should_raise_exc(rule_dict={
        'operator': 'ALLOW',
        'action': '',
        'rtype': 'bla',
        'rid': '',
        'rtags': ''
    }, org=org, team=team)

    print "\n>>>  Test rule must have either rid or rtags but not both"
    rule_should_raise_exc(rule_dict={
        'operator': 'ALLOW',
        'action': '',
        'rtype': 'key',
        'rid': 'bla',
        'rtags': {
            'bla': 'blabla'
        }
    }, org=org, team=team)

    print "\n>>>  Test rule has an rtype when it has an rid"
    rule_should_raise_exc(rule_dict={
        'operator': 'ALLOW',
        'action': '',
        'rtype': '',
        'rid': 'bla',
        'rtags': ''
    }, org=org, team=team)

    print "\n>>>  Test rule allows only the specific actions for a resource"
    rule_should_raise_exc(rule_dict={
        'operator': 'ALLOW',
        'action': 'restart',
        'rtype': 'key',
        'rid': '',
        'rtags': ''
    }, org=org, team=team)

    org.delete()
