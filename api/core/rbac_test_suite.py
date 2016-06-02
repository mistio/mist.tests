from tests.api.helpers import get_random_str


PERMISSIONS_TREE = {
    # 'script': {
    #     'read': {
    #         'weight': 1
    #     },
    #     'add': {
    #         'weight': 2
    #     },
    #     'edit': {
    #         'weight': 3
    #     },
    #     'run': {
    #         'weight': 4
    #     },
    #     'remove': {
    #         'weight': 5
    #     }
    # },
    #
    #
    # 'cloud': [
    #     'add',
    #     'read',
    #     'edit',
    #     'remove',
    #     'create_resources',  # refers to creating resource
    # ],
    # 'machine': [
    #     'read',
    #     'edit',
    #     'create',
    #     'edit_tags',
    #     'edit_rules',
    #     'edit_graphs',
    #     'edit_custom_metrics',
    #     'start',
    #     'stop',
    #     'reboot',
    #     'destroy',
    #     'resize',
    #     'run_script',
    #     'open_shell',
    #     'associate_key',
    #     'disassociate_key',
    # ],

    'key': {
        'read': {
            'key': 'add'
        },
        'read_private': {
            'key': 'read'
        },
        'add': {},
        'edit': {
            'key': 'read'
        },
        'remove': {
            'key': 'read'
        }
    }

}

PERMISSIONS_TO_TEST = [
    ('key', 'read_private'),
    # ('key', 'remove')
]


def test_rbac(mist_core, cache):
    acquired_permissions = {}
    permissions_queue = []
    owner_api_token = ''
    random_tag_value = get_random_str()
    # import ipdb
    # ipdb.set_trace()
    for tup in PERMISSIONS_TO_TEST:
        permissions_queue.append(tup)
        recurse_on_permissions(mist_core,
                               permissions_queue,
                               acquired_permissions,
                               owner_api_token,
                               random_tag_value)
    print "Map of permissions:"
    for permission in permissions_queue:
        print "%s" % repr(permission)


def recurse_on_permissions(mist_core, permissions_queue, acquired_permissions,
                           owner_api_token, random_tag_value):
    current_tup = permissions_queue[-1]
    resource = current_tup[0]
    permission_type = current_tup[1]
    # if there are other permissions that need to be acquired before setting
    # the current one, add them to the queue
    if PERMISSIONS_TREE[resource].get(permission_type):
        other_permissions = PERMISSIONS_TREE[resource].get(permission_type)
        for other_resource in other_permissions.keys():
            other_type = other_permissions[other_resource]
            if other_type not in acquired_permissions.get(other_resource, []):
                # if this permission has not been acquired yet, add it to
                # the queue
                permissions_queue.append((other_resource, other_type))
                recurse_on_permissions(mist_core,
                                       permissions_queue,
                                       acquired_permissions,
                                       owner_api_token,
                                       random_tag_value)
