from tests import config

from behave import step

from mist.core.user.models import User
from mist.core.user.models import Owner


@step(u'I setup user with email "{user_email}"')
def setup_user(context, user_email):
    if config.SETUP_ENVIRONMENT:
        try:
            Owner.objects.get(email=user_email)
        except Owner.DoesNotExist:
            user = User()
            user.email = user_email
            user.save()


@step(u'I setup user with email "{user_email}" with cloud "{provider}"')
def setup_user_and_cloud(context, user_email, provider):
    if config.SETUP_ENVIRONMENT:
        context.execute_steps(u"""
            Given I am logged in to mist.core
            Given "%s" cloud has been added
            Then I logout
            And I wait for 2 seconds
        """ % provider)
