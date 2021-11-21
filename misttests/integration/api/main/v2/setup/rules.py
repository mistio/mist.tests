def setup(api_token):
    query_request_body = {
        'queries': [
            {
                'target': 'type:session',
                'operator': 'gt',
                'threshold': 1,
                'aggregation': 'count'
            }
        ],
        'actions': [
            {
                'type': 'notification',
                'level': 'warning'
            }
        ],
        'data_type': 'logs',
        'window': {
            'period': 'minutes',
            'start': 1
        },
        'trigger_after': {
            'offset': 0,
            'period': 'seconds'
        },
        'frequency': {
            'period': 'minutes',
            'every': 1
        }
    }
    add_rule = edit_rule = {'request_body': query_request_body}
    return dict(add_rule=add_rule,
                edit_rule=edit_rule,
                rule='rule')


def teardown(api_token, setup_data):
    pass
