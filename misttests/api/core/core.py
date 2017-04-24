import json

from misttests.api.io.io import MistIoApi

from misttests.api.mistrequests import MistRequests


class MistCoreApi(MistIoApi):
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/'
                                          'policy/rules''' % (org_id, team_id),
                           data=data, api_token=api_token)
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/'
                           'policy/rules/%s' % (org_id, team_id, index_id),
                           data=data, api_token=api_token)
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
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/'
                           '%s/policy/rules/%s'
                           % (org_id, team_id, index_id),
                           data=data, api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def delete_rule_from_policy(self, api_token, org_id, team_id, index_id):
        req = MistRequests(uri=self.uri + '/api/v1/org/%s/teams/%s/'
                           'policy/rules/%s' % (org_id, team_id, index_id),
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

    def list_templates(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/templates',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def add_template(self, api_token, name, location_type,
                     exec_type='cloudify', **kwargs):
        payload = {
            'name': name,
            'location_type': location_type,
            'exec_type': exec_type
        }
        payload.update(kwargs)
        req = MistRequests(uri=self.uri + '/api/v1/templates',
                           data=json.dumps(payload), api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_template(self, api_token, template_id):
        req = MistRequests(uri=self.uri + '/api/v1/templates/' + template_id,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_template(self, api_token, template_id, name,
                      description='', **kwargs):
        payload = {
            'name': name,
            'description': description
        }
        payload.update(kwargs)
        req = MistRequests(uri=self.uri + '/api/v1/templates/' + template_id,
                           data=payload, api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def show_template(self, api_token, template_id):
        req = MistRequests(uri=self.uri + '/api/v1/templates/' + template_id,
                           api_token=api_token)
        req.put = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_stacks(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/stacks',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def create_stack(self, api_token, name, template_id):
        payload = {
            'name': name,
            'template_id': template_id,
            'workflow': 'install',
            'deploy': True
        }
        req = MistRequests(uri=self.uri + '/api/v1/stacks',
                           data=payload, api_token=api_token)
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def delete_stack(self, api_token, stack_id):
        req = MistRequests(uri=self.uri + '/api/v1/stacks/' + stack_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def show_stack(self, api_token, stack_id):
        req = MistRequests(uri=self.uri + '/api/v1/stacks/' + stack_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def run_workflow(self, api_token, stack_id, workflow=''):
        payload = {
            'workflow': workflow
        }
        req = MistRequests(uri=self.uri + '/api/v1/stacks/' + stack_id,
                           data=json.dumps(payload), api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

# CODE REVIEW
