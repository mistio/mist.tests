from misttests.integration.api.utils import *


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_tunnels_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_vpn_tunnels(api_token='').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_tunnels_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.list_vpn_tunnels(api_token='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_add_tunnel_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.add_vpn_tunnel(api_token='', name='dummy',
                                       cidrs=[], excluded_cidrs=[]).post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_add_tunnel_wrong_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.add_vpn_tunnel(api_token='dummy', name='dummy',
                                       cidrs=[], excluded_cidrs=[]).post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_add_tunnel_missing_parameter(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.add_vpn_tunnel(api_token=owner_api_token, name='',
                                        cidrs=[], excluded_cidrs=[]).post()
    assert_response_bad_request(response)
    response = mist_api_v1.add_vpn_tunnel(api_token=owner_api_token, name='dummy',
                                        cidrs=[], excluded_cidrs=[]).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_delete_tunnel_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.del_vpn_tunnel(api_token='', tunnel_id='dummy').delete()
    assert_response_forbidden(response)
    print("Success!!!")


# def test_delete_tunnel_wrong_api_token(pretty_print, mist_api_v1):
#     response = mist_api_v1.del_vpn_tunnel(api_token='dummy', tunnel_id='dummy').delete()
#     assert_response_unauthorized(response)
#     print "Success!!!"


def test_delete_tunnel_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.del_vpn_tunnel(api_token=owner_api_token, tunnel_id='dummy').delete()
    assert_response_not_found(response)
    print("Success!!!")


def test_edit_tunnel_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.edit_vpn_tunnel(api_token='', name='dummy',
                                         cidrs=[], tunnel_id='dummy').put()
    assert_response_forbidden(response)
    print("Success!!!")


# def test_edit_tunnel_wrong_api_token(pretty_print, mist_api_v1):
#     response = mist_api_v1.edit_vpn_tunnel(api_token='dummy', name='dummy',
#                                          cidrs=[], tunnel_id='dummy').put()
#     assert_response_forbidden(response)
#     print "Success!!!"


def test_edit_tunnel_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.edit_vpn_tunnel(api_token=owner_api_token, tunnel_id='dummy',
                                         cidrs=[], name='').put()
    assert_response_not_found(response)
    print("Success!!!")


# def test_add_tunnel_wrong_api_token(pretty_print, mist_api_v1):
#     response = mist_api_v1.add_vpn_tunnel(api_token='dummy', name='dummy',
#                                        cidrs=[], excluded_cidrs=[]).post()
#     assert_response_unauthorized(response)
#     print "Success!!!"


# def test_vpn_tunnels(pretty_print, mist_api_v1, cache, owner_api_token):
#     tunnel_data_1 = {
#         'cidrs': ['10.75.75.0/24'],
#         'excluded_cidrs': ['172.17.10.0/24', '172.17.20.0/24'],
#         'name': 'FirstTestTunnel',
#         'description': ''
#     }
#     tunnel_data_2 = {
#         'cidrs': ['192.168.2.0/24'],
#         'excluded_cidrs': [],
#         'name': 'SecondTestTunnel',
#         'description': ''
#     }
#
#     # setup org
#     setup_org_if_not_exists(config.ORG_NAME, config.OWNER_EMAIL,
#                             clean_org=False, add_cloud=False)
#     response = mist_api_v1.list_orgs(api_token=owner_api_token).get()
#     assert_response_ok(response)
#     org_id = None
#     orgs = json.loads(response.content)
#     for org in orgs:
#         if org['name'] == config.ORG_NAME:
#             org_id = org['id']
#             break
#     assert_is_not_none(org_id)
#
#     print "\n>>> POSTing in /tunnels for a new VPN Tunnel"
#     response = mist_api_v1.add_vpn_tunnel(api_token=owner_api_token,
#                                         **tunnel_data_1).post()
#     assert_response_ok(response)
#
#     print "\n>>> POSTing in /tunnels for a second VPN Tunnel"
#     response = mist_api_v1.add_vpn_tunnel(api_token=owner_api_token,
#                                         **tunnel_data_2).post()
#     assert_response_ok(response)
#
#     print "\n>>> GETing /tunnels"
#     response = mist_api_v1.list_vpn_tunnels(api_token=owner_api_token).get()
#     assert_response_ok(response)
#
#     tunnels = json.loads(response.content)
#     assert_list_not_empty(tunnels)
#     for tunnel in tunnels:
#         if tunnel['name'] == 'FirstTestTunnel':
#             # object id
#             _id_1 = tunnel['_id']
#             # id held by the OpenVPN server and used in every request
#             tunnel_id_1 = tunnel['tunnel_id']
#         if tunnel['name'] == 'SecondTestTunnel':
#             _id_2 = tunnel['_id']
#             tunnel_id_2 = tunnel['tunnel_id']
#
#     print "\n>>> POSTing in /tunnels with conflicting CIDRs"
#     # this should fail, as the network 10.75.75.0/30 is a subnet of
#     # 10.75.75.0/24, which is already accessible via tunnel FirstTestTunnel
#     tunnel_data = {
#         'cidrs': ['10.75.75.0/30'],
#         'excluded_cidrs': [],
#         'name': 'InvalidTunnel',
#         'description': ''
#     }
#     response = mist_api_v1.add_vpn_tunnel(api_token=owner_api_token,
#                                         **tunnel_data).post()
#     assert_response_bad_request(response)
#
#     # this should also result in a conflict, since the newly requested VPN
#     # Tunnel points to a network that tends to include the already existing
#     # 10.75.75.0/24
#     tunnel_data = {
#         'cidrs': ['10.75.75.0/16'],
#         'excluded_cidrs': [],
#         'name': 'InvalidTunnel',
#         'description': ''
#     }
#     response = mist_api_v1.add_vpn_tunnel(api_token=owner_api_token,
#                                         **tunnel_data).post()
#     assert_response_bad_request(response)
#
#     print "\n>>> PUTing in /tunnel in order to edit the second VPN Tunnel"
#     tunnel_data_2 = {
#         'cidrs': ['192.168.2.0/24', '10.75.75.0/24'],
#         'name': 'SecondTestTunnel',
#         'description': ''
#     }
#     response = mist_api_v1.edit_vpn_tunnel(api_token=owner_api_token,
#                                          tunnel_id=_id_2, **tunnel_data_2).put()
#     assert_response_bad_request(response)
#
#     tunnel_data_2 = {
#         'cidrs': ['192.168.2.0/24', '192.168.1.0/24'],
#         'name': 'SecondTestTunnel',
#         'description': 'Edited Tunnel 2'
#     }
#     response = mist_api_v1.edit_vpn_tunnel(api_token=owner_api_token,
#                                          tunnel_id=_id_2, **tunnel_data_2).put()
#     assert_response_ok(response)
#
#     print "\n>>> DELETEing all VPN Tunnels as regular member"
#     # setting up an additional user
#     setup_user_if_not_exists(config.MEMBER1_EMAIL, config.MEMBER1_PASSWORD)
#     # and a new team
#     cache.set('rbac/member1_team_id',
#               setup_team(config.ORG_NAME, 'VPNers', [config.MEMBER1_EMAIL]))
#     # creating an API token for the team member
#     response = mist_api_v1.create_token(email=config.MEMBER1_EMAIL,
#                                       password=config.MEMBER1_PASSWORD,
#                                       org_id=org_id).post()
#     member1_api_token_id = response.json().get('id', None)
#     member1_api_token = response.json().get('token', None)
#
#     response = mist_api_v1.del_vpn_tunnels(api_token=member1_api_token,
#                                          tunnel_ids=[_id_1, _id_2]).delete()
#     assert_response_unauthorized(response)
#
#     # finally, revoke the token
#     response = mist_api_v1.revoke_token(member1_api_token, member1_api_token_id).delete()
#     assert_response_ok(response)
#
#     print "\n>>> DELETEing all VPN Tunnels as owner"
#     response = mist_api_v1.del_vpn_tunnels(api_token=owner_api_token,
#                                          tunnel_ids=[_id_1, _id_2]).delete()
#     assert_response_ok(response)
#
#     print "Success!!!!"
