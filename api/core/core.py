import json

from tests.api.io.io import MistIoApi

from tests.api.mistrequests import MistRequests


class MistCoreApi(MistIoApi):
    def login(self, email, password, service=None, cookie=None):
        req = MistRequests(uri=self.uri + '/login', cookie=cookie, data={
            'email': email,
            'password': password
        })
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def logout(self, cookie, csrf):
        req = MistRequests(uri=self.uri + '/logout', cookie=cookie, csrf=csrf)
        return req

    def check_auth(self, email, password='', api_token_name='', ttl='',
                   org_id=None, api_token=None):
        data = {'email': email}
        if password:
            data.update({'password': password})
        if api_token_name:
            data.update({'name': api_token_name})
        if ttl:
            data.update({'ttl': ttl})
        if org_id:
            data.update({'org_id': org_id})
        req = MistRequests(uri=self.uri + '/auth', data=data,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_tokens(self, api_token):
        req = MistRequests(uri=self.uri + '/tokens', api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def create_token(self, email, password, api_token=None, ttl=None,
                     org_id=None, new_api_token_name=None):
        data = {
            'email': email,
            'password': password,
            'ttl': ttl,
            'org_id': org_id
        }
        if new_api_token_name:
            data.update({'name': new_api_token_name})
        req = MistRequests(uri=self.uri + '/tokens', data=data,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def revoke_token(self, api_token, api_token_id):
        req = MistRequests(uri=self.uri + '/tokens',
                           params={'id': api_token_id},
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def tokens(self, api_token, **kwargs):
        req = MistRequests(uri=self.uri + '/tokens', data=kwargs,
                           api_token=api_token)
        req.put = req.unavailable_api_call
        return req

    def check_token(self, api_token):
        req = MistRequests(uri=self.uri + '/check_token', api_token=api_token)
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def su(self, api_token):
        req = MistRequests(uri=self.uri + '/su', api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def add_cronjob_entry(self, name, machines_per_cloud, enabled,
                          cronjob_type, cronjob_entry, api_token,
                          expires='', script_id='', action=''):
        data = {
            'name': name,
            'script_id': script_id,
            'action': action,
            'machines_per_cloud': machines_per_cloud,
            'enabled': enabled,
            'expires': expires,
            'cronjob_type': cronjob_type,
            'cronjob_entry': cronjob_entry
        }
        req = MistRequests(uri=self.uri + '/cronjobs',
                           data=json.dumps(data), api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_cronjob_entry(self, name, machines_per_cloud, enabled,
                           cronjob_type, cronjob_entry, cronjob_id, api_token,
                           expires='', script_id='', action=''):
        data = {
            'name': name,
            'script_id': script_id,
            'action': action,
            'machines_per_cloud': machines_per_cloud,
            'enabled': enabled,
            'expires': expires,
            'cronjob_type': cronjob_type,
            'cronjob_entry': cronjob_entry
        }

        req = MistRequests(uri=self.uri + '/cronjobs/' + cronjob_id,
                           data=json.dumps(data), api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.post = req.unavailable_api_call
        return req

    def list_cronjobs_entries(self, api_token):
        req = MistRequests(uri=self.uri + '/cronjobs', api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_cronjobs_entry(self, cronjob_id, api_token):
        req = MistRequests(uri=self.uri + '/cronjobs/' + cronjob_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_cronjob(self, cronjob_id, api_token):
        req = MistRequests(uri=self.uri + '/cronjobs/' + cronjob_id,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_job(self, api_token, job_id):
        req = MistRequests(uri=self.uri + '/jobs/%s' % job_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def add_script(self, api_token, name, exec_type, location_type, script=None,
                   entrypoint=None, description=None):
        data = {
            'name': name,
            'exec_type': exec_type,
            'location_type': location_type
        }
        if script is not None:
            data['script'] = script
        if entrypoint is not None:
            data['entrypoint'] = entrypoint
        if description is not None:
            data['description'] = description
        req = MistRequests(uri=self.uri + '/scripts', api_token=api_token,
                           data=data)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_script(self, api_token, script_id):
        req = MistRequests(uri=self.uri + '/scripts/%s' % script_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_scripts(self, api_token):
        req = MistRequests(uri=self.uri + '/scripts', api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_script(self, api_token, script_id, new_name, new_description=''):
        data = {'new_name': new_name}
        if new_description:
            data.update({'new_description': new_description})

        req = MistRequests(uri=self.uri + '/scripts/%s' % script_id,
                           api_token=api_token, data=data)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def run_script(self, api_token, cloud_id, machine_id, script_id):
        data = {
            'cloud_id': cloud_id,
            'machine_id': machine_id,
        }
        req = MistRequests(uri=self.uri + '/script/%s' % script_id,
                           api_token=api_token, data=data)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_script(self, api_token, script_id):
        req = MistRequests(uri=self.uri + '/scripts/%s' % script_id,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_scripts(self, api_token, script_ids):
        req = MistRequests(uri=self.uri + '/scripts',
                           json={'script_ids': script_ids},
                           api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def create_org(self, api_token, name=''):
        req = MistRequests(uri=self.uri + '/org',
                           json={'name': name},
                           api_token=api_token)

        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_org(self, api_token, org_id):
        req = MistRequests(uri=self.uri + '/org/%s' % org_id,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_user_org(self, api_token):
        req = MistRequests(uri=self.uri + '/org',
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_user_invitations(self, api_token):
        req = MistRequests(uri=self.uri + '/user_invitations',
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def add_team(self, api_token, org_id, name, description=None):
        data = {'name': name,
                }
        if description is not None:
            data.update({'description': description})
        req = MistRequests(uri=self.uri + '/org/%s/teams' % org_id,
                           api_token=api_token, data=data)

        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_teams(self, api_token, org_id):
        req = MistRequests(uri=self.uri + '/org/%s/teams' % org_id,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_team(self, api_token, org_id, team_id):
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s'
                                          % (org_id, team_id),
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_team(self, api_token, org_id, team_id, name, description=None):
        data = {'new_name': name,
                }

        if description is not None:
            data.update({'new_description': description})
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s'
                                          % (org_id, team_id), data=data,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def delete_team(self, api_token, org_id, team_id):
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s'
                                          % (org_id, team_id),
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def invite_member_to_team(self, api_token, org_id, team_id, email):
        data = {'email': email}
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/members' %
                                          (org_id, team_id),
                           api_token=api_token, data=data)

        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_member_from_team(self, api_token, org_id, team_id, user_id):
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/members/%s'
                                          % (org_id, team_id, user_id),
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_team_policy(self, api_token, org_id, team_id):
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy'
                                          % (org_id, team_id),
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_team_policy_operator(self, api_token, org_id, team_id,
                                  policy_operator):
        data = {'policy_operator': policy_operator,
                }
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy'
                                          % (org_id, team_id), data=data,
                           api_token=api_token)

        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def append_rule_to_policy(self, api_token, org_id, team_id, operator,
                              action, rtype, rid, rtags):
        if isinstance(rtags, dict):
            rtags = json.dumps(rtags)
        data = {'operator': operator,
                'action': action,
                'rtype': rtype,
                'rid': rid,
                'rtags': rtags
                }
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy/rules'
                                          '' % (org_id, team_id),
                           data=data,
                           api_token=api_token)

        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def insert_rule_to_policy(self, api_token, org_id, team_id, index_id,
                              operator, action, rtype, rid, rtags):
        data = {'operator': operator,
                'action': action,
                'rtype': rtype,
                'rid': rid,
                'rtags': rtags
                }
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy/rules/%s'
                                          % (org_id, team_id, index_id),
                           data=data,
                           api_token=api_token)

        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def edit_rule_to_policy(self, api_token, org_id, team_id, index_id,
                            operator,
                            action, rtype, rid, rtags):
        data = {'operator': operator,
                'action': action,
                'rtype': rtype,
                'rid': rid,
                'rtags': rtags
                }
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy/rules/%s'
                                          % (org_id, team_id, index_id),
                           data=data,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def delete_rule_from_policy(self, api_token, org_id, team_id, index_id):
        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy/rules/%s'
                                          % (org_id, team_id, index_id),
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_team_policy(self, api_token, org_id, team_id, policy):
        data = {'policy': policy}

        req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy'
                                          % (org_id, team_id),
                           data=json.dumps(data),
                           api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_orgs(self, api_token):
        req = MistRequests(uri=self.uri + '/orgs', api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    # def patch_rule_to_policy(self, api_token, org_id, team_id, index_id, operator,
    #                           action, rtype, rid, rtags, pos):
    #     data={'operator':operator,
    #           'action':action,
    #           'rtype':rtype,
    #           'rid':rid,
    #           'rtags':rtags,
    #           'pos':pos,
    #     }
    #     req = MistRequests(uri=self.uri + '/org/%s/teams/%s/policy/rules/%s'
    #                                       % (org_id, team_id, index_id), data=data,
    #                        api_token=api_token)
    #
    #     req.post = req.unavailable_api_call
    #     req.put = req.unavailable_api_call
    #     req.delete = req.unavailable_api_call
    #     req.get = req.unavailable_api_call
    #     return req

    def set_machine_tags(self, api_token, cloud_id, machine_id, **tags):
        data = {
            'tags': tags
        }
        payload = json.dumps(data)
        req = MistRequests(uri=self.uri + '/clouds/' + cloud_id +
                           '/machines/' + machine_id + '/tags',
                           data=payload, api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_vpn_tunnels(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/tunnels', api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def add_vpn_tunnel(self, api_token, client_addr, cidrs, name, description):
        data = {
            'name': name,
            'cidrs': cidrs,
            'client_addr': client_addr,
            'description': description
        }
        payload = json.dumps(data)
        req = MistRequests(uri=self.uri + '/api/v1/tunnels', data=payload, api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def del_vpn_tunnel(self, api_token, tunnel_id):
        req = MistRequests(uri=self.uri + '/api/v1/tunnel/' + tunnel_id, api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def del_vpn_tunnels(self, api_token, tunnel_ids):
        data = {
            'tunnel_ids': tunnel_ids
        }
        payload = json.dumps(data)
        req = MistRequests(uri=self.uri + '/api/v1/tunnels', data=payload, api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def edit_vpn_tunnel(self, api_token, tunnel_id, cidrs, name, description):
        data = {
            'cidrs': cidrs,
            'name': name,
            'description': description
        }
        payload = json.dumps(data)
        req = MistRequests(uri=self.uri + '/api/v1/tunnel/' + tunnel_id,
                           data=payload, api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req
