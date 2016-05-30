from behave import step

from tests.helpers.setup import setup_user_if_not_exists
from tests.helpers.setup import remove_user_if_exists


@step(u'I setup user with email "{user_email}"')
def setup_user(context, user_email):
    setup_user_if_not_exists(user_email)


@step(u'I make sure user with email "{user_email}" is absent')
def remove_user(context, user_email):
    remove_user_if_exists(user_email)
