import json
import requests
import logging

from behave import step

from misttests.helpers.setup import setup_user_if_not_exists
from misttests.helpers.setup import remove_user_if_exists


log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@step(u'I setup user with email "{user_email}"')
def setup_user(context, user_email):
    if context.mist_config.get(user_email):
        user_email = context.mist_config.get(user_email)
    setup_user_if_not_exists(user_email)


@step(u'I make sure user with email "{user_email}" is absent')
def remove_user(context, user_email):
    if context.mist_config.get(user_email):
        user_email = context.mist_config.get(user_email)
    remove_user_if_exists(context.mist_config['MIST_URL'], user_email)


@step(u'user with email "{user_email}" is registered')
def register_user(context, user_email):
    payload = {
        'email': context.mist_config['EMAIL'],
        'password': context.mist_config['PASSWORD1'],
        'name': "Atheofovos Gkikas"
    }

    requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'],
                  data=json.dumps(payload))
