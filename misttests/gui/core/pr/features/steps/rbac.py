import json
import random
import requests

from misttests.gui.steps.team import *
from misttests.gui.steps.policy import *
from misttests.gui.steps.org_context import *

@step(u'rbac members are initialized')
def initiliaze_rbac_members(context):
    BASE_EMAIL = context.mist_config['BASE_EMAIL']
    context.mist_config['MEMBER1_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))
    context.mist_config['MEMBER2_EMAIL'] = "%s+%d@gmail.com" % (BASE_EMAIL, random.randint(1,200000))

    context.mist_config['ORG_NAME'] = "rbac_org_%d" % random.randint(1,200000)

    payload = {
        'email': context.mist_config['MEMBER1_EMAIL'],
        'password': context.mist_config['MEMBER1_PASSWORD'],
        'name': "Atheofovos Gkikas"
    }

    re = requests.post("%s/api/v1/dev/register" % context.mist_config['MIST_URL'], data=json.dumps(payload))
    return
