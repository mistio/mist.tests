from functools import partial

from misttests.config import inject_vault_credentials
from misttests.config import MIST_URL
from misttests.integration.api.helpers import assert_response_ok
from misttests.integration.api.helpers import poll
from misttests.integration.api.helpers import uniquify_string
from misttests.integration.api.mistrequests import MistRequests

V2_ENDPOINT = 'api/v2'
CLOUDS_ENDPOINT = f'{V2_ENDPOINT}/clouds'
CLUSTERS_ENDPOINT = f'{V2_ENDPOINT}/clusters'
LOCATIONS_ENDPOINT = f'{V2_ENDPOINT}/locations'


def setup(api_token):
    cloud_name = uniquify_string('test-cloud')
    add_cloud_request = {
        'name': cloud_name,
        'provider': 'google',
        'credentials': {
            'projectId': 'projectId',
            'privateKey': 'privateKey',
            'email': 'email'
        },
        'features': {
            'container': True,
        },
    }
    inject_vault_credentials(add_cloud_request)
    clouds_uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}'
    request = MistRequests(
        api_token=api_token, uri=clouds_uri, json=add_cloud_request)
    response = request.post()
    assert_response_ok(response)

    # Wait for gce locations to become available
    assert poll(api_token=api_token,
                uri=f'{MIST_URL}/{LOCATIONS_ENDPOINT}',
                query_params=[('cloud', cloud_name)],
                timeout=800,
                data={'name': 'us-central1-c'})

    cluster_name = uniquify_string('test-cluster')
    nodepool_name = f'{cluster_name}-pool-0'
    cluster_uri = f'{MIST_URL}/{CLUSTERS_ENDPOINT}/{cluster_name}'
    test_args = {
        'create_cluster': {
            'request_body': {
                'cloud': cloud_name,
                'location': 'us-central1-c',
                'name': cluster_name,
                'provider': 'google'
            },
            'callback': partial(poll,
                                api_token=api_token,
                                uri=cluster_uri,
                                data={'state': 'running'},
                                timeout=800),
        },
        'scale_nodepool': {
            'request_body': {
                'desired_nodes': 1,
            },
            'callback': partial(poll,
                                api_token=api_token,
                                uri=cluster_uri,
                                data={'total_nodes': 1},
                                timeout=800),
            'cluster': cluster_name,
            'nodepool': nodepool_name,
        },
        'get_cluster': {
            'cluster': cluster_name,
        },
        'destroy_cluster': {'cluster': cluster_name}
    }
    setup_data = dict(**test_args, cloud=cloud_name)
    return setup_data


def teardown(api_token, setup_data):
    cloud_name = setup_data['cloud']
    cloud_uri = f'{MIST_URL}/{CLOUDS_ENDPOINT}/{cloud_name}'
    request = MistRequests(api_token=api_token, uri=cloud_uri)
    request.delete()
