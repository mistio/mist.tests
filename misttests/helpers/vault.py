from misttests import config

import requests
import os


def safe_get_var(vault_path, vault_key, test_settings_var):

    if config.VAULT_ENABLED:

        print "Vault enabled"

        headers = {"X-Vault-Token": os.environ['vault_client_token']}

        re = requests.get(config.VAULT_SERVER + '/v1/secret/%s' % vault_path, headers=headers)

        json_data = re.json().get('data')

        return json_data.get(vault_key)

    else:

        print "Vault disabled"

        return test_settings_var
