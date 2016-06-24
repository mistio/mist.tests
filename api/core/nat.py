from tests.api.helpers import *
from tests.api.utils import *

from tests.helpers.setup import setup_user_if_not_exists

from tests import config


def test_nat(pretty_print, mist_core, cache, valid_api_token):
    sanitized_url = config.VPN_URL.replace('http://', '').split(':')[0]
    # setting up user
    user = setup_user_if_not_exists(config.EMAIL, config.PASSWORD1)

    print '\n>>> POSTing in /tunnels for a new VPN Tunnel'
    # request a dummy tunnel
    tunnel_data = {
        'client_addr': '',
        'cidrs': ['10.10.10.0/24'],
        'name': 'DummyTestTunnel',
        'description': 'Testing DNAT'
    }
    response = mist_core.add_vpn_tunnel(api_token=valid_api_token,
                                        **tunnel_data).post()
    assert_response_ok(response)

    print '\n>>> GETing forwarding (addr, port) tuples from the OpenVPN server'
    from mist.core.vpn.methods import destination_nat
    # scenarios providing an (addr, port) tuple to be translated
    addr, port1 = destination_nat(user, '10.10.10.5', 80)
    print '(%s, %s) -> (%s, %s)' % ('10.10.10.5', 80, addr, port1)
    assert addr == sanitized_url, addr
    assert port1 is not None, 'No port returned!'
    addr, port = destination_nat(user, '10.10.10.5', 22)
    print '(%s, %s) -> (%s, %s)' % ('10.10.10.5', 22, addr, port)
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    addr, port2 = destination_nat(user, 'http://10.10.10.5', 80)
    print '(%s, %s) -> (%s, %s)' % ('http://10.10.10.5', 80, addr, port2)
    assert addr == sanitized_url, addr
    assert port2 is not None, 'No port returned!'
    # providing only a single URI string to be translated
    # and returned in the same exact format
    addr = destination_nat(user, '10.10.10.5')
    print '%s -> %s' % ('10.10.10.5', addr)
    addr, port3 = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port3 is not None, 'No port returned!'
    # forwarded ports: port1, port2, port3 should be equal, since they all
    # point to the same dst port (80) via the same VPN tunnel
    assert int(port1) == int(port2) == int(port3), 'Ports do not match!'
    addr = destination_nat(user, 'https://10.10.10.5')
    print '%s -> %s' % ('https://10.10.10.5', addr)
    assert addr.startswith('https://'), 'Prefix missing!'
    addr = addr.replace('https://', '')
    addr, port = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    addr = destination_nat(user, '10.10.10.5:5000')
    print '%s -> %s' % ('10.10.10.5:5000', addr)
    addr, port = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    addr = destination_nat(user, 'http://10.10.10.5:5000/api/v1')
    print '%s -> %s' % ('http://10.10.10.5:5000/api/v1', addr)
    assert addr.startswith('http://'), 'Prefix missing!'
    assert addr.endswith('/api/v1'), 'Suffix missing!'
    addr = addr.replace('http://', '')
    addr = addr.replace('/api/v1', '')
    addr, port = addr.split(':')[0], addr.split(':')[1]
    assert addr == sanitized_url, addr
    assert port is not None, 'No port returned!'
    # bad request
    try:
        destination_nat(user, '10.10.10.5:5000', 80)
    except Exception as exc:
        assert str(exc).startswith('Bad Request'), 'Bad response!'

    print "\n>>> GETing /tunnels"
    response = mist_core.list_vpn_tunnels(api_token=valid_api_token).get()
    assert_response_ok(response)

    tunnels = json.loads(response.content)
    assert_list_not_empty(tunnels)
    for tunnel in tunnels:
        if tunnel['name'] == 'DummyTestTunnel':
            _id = tunnel['_id']

    print "\n>>> DELETEing VPN Tunnel"
    response = mist_core.del_vpn_tunnel(api_token=valid_api_token,
                                        tunnel_id=_id).delete()
    assert_response_ok(response)

    print "Success!!!!"
