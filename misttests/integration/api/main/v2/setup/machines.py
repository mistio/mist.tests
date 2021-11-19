# from time import sleep
# from misttests import config
# from misttests.integration.api.helpers import assert_response_ok
# from misttests.integration.api.helpers import uniquify_string
# from misttests.integration.api.mistrequests import MistRequests

# This variable is used by the machines test module. It must contain a list of
# all the machines test methods in the specific order in which they should be
# run.
TEST_METHOD_ORDERING = [
    'create_machine',
    'reboot_machine',
    'resize_machine',
    'stop_machine',
    'start_machine',
    'ssh',
    'associate_key',
    'disassociate_key',
    'edit_machine',
    'rename_machine',
    'get_machine',
    'list_machines',
    'clone_machine',
    'console',
    'suspend_machine',
    'resume_machine',
    'destroy_machine',
    'undefine_machine',
]


def setup(api_token):
    pass


def teardown(api_token, setup_data):
    pass
