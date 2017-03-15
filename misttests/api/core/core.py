import json

from misttests.api.io.io import MistIoApi

from misttests.api.mistrequests import MistRequests


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
        req = MistRequests(uri=self.uri + '/api/v1/tokens', data=data,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_tokens(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/tokens', api_token=api_token)
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
        req = MistRequests(uri=self.uri + '/api/v1/tokens', data=data,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def revoke_token(self, api_token, api_token_id):
        req = MistRequests(uri=self.uri + '/api/v1/tokens',
                           params={'id': api_token_id},
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def tokens(self, api_token, **kwargs):
        req = MistRequests(uri=self.uri + '/api/v1/tokens', data=kwargs,
                           api_token=api_token)
        req.put = req.unavailable_api_call
        return req

    def check_token(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/ping', api_token=api_token)
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
        req = MistRequests(uri=self.uri + '/api/v1/cronjobs',
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

        req = MistRequests(uri=self.uri + '/api/v1/cronjobs/' + cronjob_id,
                           data=json.dumps(data), api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.post = req.unavailable_api_call
        return req

    def list_cronjobs_entries(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/cronjobs', api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_cronjobs_entry(self, cronjob_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/cronjobs/' + cronjob_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_cronjob(self, cronjob_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/cronjobs/' + cronjob_id,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_job(self, api_token, job_id):
        req = MistRequests(uri=self.uri + '/api/v1/jobs/%s' % job_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def create_org(self, api_token, name=''):
        req = MistRequests(uri=self.uri + '/api/v1/org',
                           json={'name': name},
                           api_token=api_token)

        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_org(self, api_token, org_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s' % org_id,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_user_org(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/org',
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams' % org_id,
                           api_token=api_token, data=data)

        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_teams(self, api_token, org_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams' % org_id,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_team(self, api_token, org_id, team_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s'
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s'
                                          % (org_id, team_id), data=data,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def delete_team(self, api_token, org_id, team_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s'
                                          % (org_id, team_id),
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def invite_member_to_team(self, api_token, org_id, team_id, email):
        data = {'email': email}
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/members' %
                                          (org_id, team_id),
                           api_token=api_token, data=data)

        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_member_from_team(self, api_token, org_id, team_id, user_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/members/%s'
                                          % (org_id, team_id, user_id),
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_team_policy(self, api_token, org_id, team_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/policy'
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/policy'
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/policy/rules'
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/policy/rules/%s'
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/policy/rules/%s'
                                          % (org_id, team_id, index_id),
                           data=data,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def delete_rule_from_policy(self, api_token, org_id, team_id, index_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/policy/rules/%s'
                                          % (org_id, team_id, index_id),
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_team_policy(self, api_token, org_id, team_id, policy):
        data = {'policy': policy}

        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/policy'
                                          % (org_id, team_id),
                           data=json.dumps(data),
                           api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_orgs(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/orgs', api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def set_machine_tags(self, api_token, cloud_id, machine_id, tags):
        resource_data = {
            'item_id': machine_id,
            'type': 'machine',
            'cloud_id': cloud_id
        }
        tags_data = []
        tags_data.append(tags)
        data = [{
            'tags': tags_data,
            'resource': resource_data
        }]
        payload = json.dumps(data)
        req = MistRequests(uri=self.uri + '/api/v1/tags',
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

    def add_vpn_tunnel(self, api_token, cidrs, excluded_cidrs, name, description=''):
        data = {
            'name': name,
            'cidrs': cidrs,
            'excluded_cidrs': excluded_cidrs,
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

    def edit_vpn_tunnel(self, api_token, tunnel_id, cidrs, name, description=''):
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

    def list_schedules(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/schedules', api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def add_schedule(self, api_token, name, schedule_type, schedule_entry='', description='', machines_uuids=[],
                     machines_tags=[], task_enabled=True, expires='', script_id='', action='', max_run_count='',
                     run_immediately=False):
        data = {
            'machines_uuids': machines_uuids,
            'name': name,
            'description': description,
            'machines_tags': machines_tags,
            'schedule_type': schedule_type,
            'schedule_entry': schedule_entry,
            'task_enabled': task_enabled,
            'action': action,
            'script_id': script_id,
            'expires': expires,
            'max_run_count': max_run_count,
            'run_immediately': run_immediately
        }
        req = MistRequests(uri=self.uri + '/api/v1/schedules', api_token=api_token, data=json.dumps(data))
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    # 'params': '', u'start_after': u''

    def delete_schedule(self, api_token, schedule_id):
        req = MistRequests(uri=self.uri + '/api/v1/schedules/' + schedule_id, api_token=api_token)
        req.post = req.unavailable_api_call
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_schedule(self, api_token, schedule_id, data=''):
        req = MistRequests(uri=self.uri + '/api/v1/schedules/' + schedule_id, api_token=api_token, data=data)
        req.post = req.unavailable_api_call
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def show_schedule(self, api_token, schedule_id):
        req = MistRequests(uri=self.uri + '/api/v1/schedules/' + schedule_id, api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req
