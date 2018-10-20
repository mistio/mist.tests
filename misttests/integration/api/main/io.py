import json

from misttests.integration.api.mistrequests import MistRequests


class MistIoApi(object):

    def __init__(self, uri):
        self.uri = uri

    #################################################
    #                     CLOUDS                    #
    #################################################

    def supported_providers(self, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/providers',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_clouds(self, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def add_cloud(self, title, provider, api_token=None, **kwargs):
        payload = {
            'title': title,
            'provider': provider
        }
        payload.update(kwargs)
        req = MistRequests(uri=self.uri + '/api/v1/clouds',
                           data=json.dumps(payload), api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def rename_cloud(self, cloud_id, new_name, cookie=None, csrf_token=None,
                     api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id,
                           data={'new_name': new_name}, cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_cloud(self, cloud_id, cookie=None, csrf_token=None,
                     api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id,
                           cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def toggle_cloud(self, cloud_id, api_token=None, new_state=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id,
                           data={'new_state': new_state}, api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_sizes(self, cloud_id, cookie=None, csrf_token=None,
                   api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' +
                           cloud_id + '/sizes', cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_locations(self, cloud_id, cookie=None, csrf_token=None,
                       api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/locations', cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)

        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    #################################################
    #                     IMAGES                    #
    #################################################

    def list_images(self, cloud_id, search_term=None, cookie=None,
                    csrf_token=None, api_token=None):
        kwargs = {
            'uri': self.uri + '/api/v1/clouds/' + cloud_id + '/images',
            'cookie': cookie,
            'csrf_token': csrf_token,
            'api_token': api_token
        }

        if search_term:
            kwargs.update({'data': {'search_term': search_term}})

        req = MistRequests(**kwargs)
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def star_image(self, cloud_id, image_id, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id
                           + '/images/' + image_id, api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    #################################################
    #                    MACHINES                   #
    #################################################

    def list_machines(self, cloud_id, cookie=None, csrf_token=None,
                      api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/machines', cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def create_machine(self, cloud_id, key_id, name, provider, location, image,
                       size, script="", disk=None, image_extra=None,
                       cookie=None, csrf_token=None, api_token=None,
                       cron_enable=False, cron_type=None, cron_entry=None,
                       cron_script=None, cron_name=None, async=False,
                       monitoring=False, cloud_init="", location_name='',
                       job_id=None):
        # ! disk and image_extra are required only for Linode
        # ! cronjobs' variables are required only if we want to set a scheduler
        # ! this way cronjob vars pass empty in create machine params
        payload = {
            # 'cloud': cloud_id,
            'key': key_id,
            'name': name,
            'provider': provider,
            'location': location,
            'location_name': location_name,
            'image': image,
            'size': size,
            'script': script,
            'disk': disk,
            'image_extra': image_extra,
            'cronjob_enabled': cron_enable,
            'cronjob_type': cron_type,
            'cronjob_entry': cron_entry,
            'cronjob_script_id': cron_script,
            'cronjob_name': cron_name,
            'async': async,
            'monitoring': monitoring,
            'cloud_init': cloud_init,
            'job_id': job_id,
        }
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' +
                           cloud_id + '/machines', cookie=cookie,
                           data=json.dumps(payload), timeout=600,
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def destroy_machine(self, cloud_id, machine_id, cookie=None,
                        csrf_token=None, api_token=None):
        uri = self.uri + '/api/v1/clouds/' + cloud_id + '/machines/'\
              + machine_id
        req = MistRequests(uri=uri, data={'action': 'destroy'}, cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def machine_action(self, cloud_id, machine_id, cookie=None,
                       csrf_token=None, api_token=None, action=''):
        data = {}
        if action:
            data = {'action': action}
        uri = self.uri + '/api/v1/clouds/' + cloud_id +\
            '/machines/' + machine_id
        req = MistRequests(uri=uri, cookie=cookie, data=data,
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
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

    def associate_key(self, cloud_id, machine_id, key_id, cookie=None,
                      csrf_token=None, api_token=None):

        uri = self.uri + '/api/v1/clouds/' + cloud_id + \
              '/machines/' + machine_id + '/keys/' + key_id
        req = MistRequests(uri=uri, cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def machine_monitoring(self, cloud_id, machine_id, cookie=None,
                           csrf_token=None, api_token=None, action=''):
        data = {}
        if action:
            data = {'action': action}
        uri = self.uri + '/api/v1/clouds/' + cloud_id + \
            '/machines/' + machine_id + '/monitoring'
        req = MistRequests(uri=uri, cookie=cookie, data=data,
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    #################################################
    #                      KEYS                     #
    #################################################

    def list_keys(self, cookie=None, csrf_token=None, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys', cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def add_key(self, name, private, cookie=None, csrf_token=None,
                api_token=None, is_default=''):
        payload = {
            'name': name,
            'priv': private
        }

        if is_default:
            payload.update({'isDefault': is_default})
        req = MistRequests(uri=self.uri + '/api/v1/keys', cookie=cookie,
                           data=json.dumps(payload),
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def edit_key(self, id, new_name, cookie=None, csrf_token=None,
                 api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys/' + id,
                           data=json.dumps({'new_name': new_name}),
                           cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_key(self, key_id, cookie=None, csrf_token=None, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys/' + key_id,
                           cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_keys(self, key_ids, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys',
                           api_token=api_token,
                           json={'key_ids': key_ids})
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def generate_keypair(self, cookie=None, csrf_token=None, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys', cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def get_private_key(self, key_id, cookie=None, csrf_token=None,
                        api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys/' + key_id +
                           '/private', cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def get_public_key(self, key_id, cookie=None, csrf_token=None,
                       api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys/' + key_id + '/public',
                           cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def set_default_key(self, key_id, cookie=None, csrf_token=None,
                        api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys/' + key_id,
                           cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    #################################################
    #                    SCRIPTS                    #
    #################################################

    def add_script(self, api_token, script_data, script=None,
                   entrypoint=None, description=None):
        data = {}
        data.update(script_data)

        if script is not None:
            data['script'] = script
        if entrypoint is not None:
            data['entrypoint'] = entrypoint
        if description is not None:
            data['description'] = description

        req = MistRequests(uri=self.uri + '/api/v1/scripts',
                           api_token=api_token, data=data)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def show_script(self, api_token, script_id):
        req = MistRequests(uri=self.uri + '/api/v1/scripts/%s' % script_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def list_scripts(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/scripts',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_script(self, api_token, script_id, new_name, new_description=''):
        data = {'new_name': new_name}
        if new_description:
            data.update({'new_description': new_description})
        req = MistRequests(uri=self.uri + '/api/v1/scripts/%s' % script_id,
                           api_token=api_token, data=data)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def run_script(self, api_token, cloud_id, machine_id, script_id, job_id):
        data = {
            'cloud_id': cloud_id,
            'machine_id': machine_id,
            'job_id': job_id,
        }
        req = MistRequests(uri=self.uri + '/api/v1/scripts/%s' % script_id,
                           api_token=api_token, data=data)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_script(self, api_token, script_id):
        req = MistRequests(uri=self.uri + '/api/v1/scripts/%s' % script_id,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def download_script(self, api_token, script_id):
        req = MistRequests(uri=self.uri + '/api/v1/scripts/%s/file'
                                          % script_id,
                           api_token=api_token)
        req.delete = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def url_script(self, api_token, script_id):
        req = MistRequests(uri=self.uri + '/api/v1/scripts/%s/url' % script_id,
                           api_token=api_token)
        req.delete = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_scripts(self, api_token, script_ids):
        req = MistRequests(uri=self.uri + '/api/v1/scripts',
                           json={'script_ids': script_ids},
                           api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    #################################################
    #                   SCHEDULES                   #
    #################################################

    def list_schedules(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/schedules',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def add_schedule(self, api_token, name, schedule_type,
                     conditions, schedule_entry='',
                     description='', task_enabled=True, expires='',
                     script_id='', action='',
                     max_run_count='', run_immediately=False):
        data = {
            'conditions': conditions,
            'name': name,
            'description': description,
            'schedule_type': schedule_type,
            'schedule_entry': schedule_entry,
            'task_enabled': task_enabled,
            'action': action,
            'script_id': script_id,
            'expires': expires,
            'max_run_count': max_run_count,
            'run_immediately': run_immediately
        }
        req = MistRequests(uri=self.uri + '/api/v1/schedules',
                           api_token=api_token, data=json.dumps(data))
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def delete_schedule(self, api_token, schedule_id):
        req = MistRequests(uri=self.uri + '/api/v1/schedules/' + schedule_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def edit_schedule(self, api_token, schedule_id, data=''):
        req = MistRequests(uri=self.uri + '/api/v1/schedules/' + schedule_id,
                           api_token=api_token, data=data)
        req.post = req.unavailable_api_call
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def show_schedule(self, api_token, schedule_id):
        req = MistRequests(uri=self.uri + '/api/v1/schedules/' + schedule_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    #################################################
    #                     ZONES                     #
    #################################################

    def list_zones(self, api_token, cloud_id):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/dns/zones', api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_records(self, api_token, cloud_id, zone_id):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/dns/zones/' + zone_id + '/records',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def create_zone(self, api_token, cloud_id, domain, type, ttl):
        data = {
            'domain': domain,
            'type': type,
            'ttl': ttl
        }
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/dns/zones', api_token=api_token, data=data)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_zone(self, api_token, cloud_id, zone_id):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/dns/zones/' + zone_id, api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def create_record(self, api_token, cloud_id, zone_id, name, type,
                      data, ttl):
        data = {
            'name': name,
            'type': type,
            'data': data,
            'ttl': ttl
        }
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/dns/zones/' + zone_id + '/records',
                           api_token=api_token, data=data)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_record(self, api_token, cloud_id, zone_id, record_id):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/dns/zones/' + zone_id + '/records/' + record_id,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    #################################################
    #                    TUNNELS                    #
    #################################################

    def list_vpn_tunnels(self, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/tunnels',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def add_vpn_tunnel(self, api_token, cidrs, excluded_cidrs,
                       name, description=''):
        data = {
            'name': name,
            'cidrs': cidrs,
            'excluded_cidrs': excluded_cidrs,
            'description': description
        }
        payload = json.dumps(data)
        req = MistRequests(uri=self.uri + '/api/v1/tunnels', data=payload,
                           api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def del_vpn_tunnel(self, api_token, tunnel_id):
        req = MistRequests(uri=self.uri + '/api/v1/tunnel/' + tunnel_id,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def del_vpn_tunnels(self, api_token, tunnel_ids):
        data = {
            'tunnel_ids': tunnel_ids
        }
        payload = json.dumps(data)
        req = MistRequests(uri=self.uri + '/api/v1/tunnels', data=payload,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.get = req.unavailable_api_call
        return req

    def edit_vpn_tunnel(self, api_token, tunnel_id, cidrs, name,
                        description=''):
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

    #################################################
    #                   NETWORKS                    #
    #################################################

    def list_networks(self, cloud_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/networks', api_token=api_token)

        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_subnets(self, cloud_id, network_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/networks/' + network_id + '/subnets',
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def create_network(self, cloud_id, api_token, network_params=''):
        data = {}
        if network_params:
            data.update(network_params)

        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id
                           + '/networks', api_token=api_token,
                           data=json.dumps(data))
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_network(self, cloud_id, network_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id
                           + '/networks/' + network_id, api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def create_subnet(self, cloud_id, network_id, api_token, subnet_params=''):
        data = {}
        if subnet_params:
            data.update(subnet_params)
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id
                           + '/networks/' + network_id + '/subnets',
                           api_token=api_token, data=json.dumps(data))
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_subnet(self, cloud_id, network_id, subnet_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id
                           + '/networks/' + network_id +
                           '/subnets/' + subnet_id, api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req


    #################################################
    #                   VOLUMES                     #
    #################################################

    def list_volumes(self, cloud_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id +
                           '/volumes', api_token=api_token)

        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def create_volume(self, cloud_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id
                           + '/volumes', api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def delete_volume(self, cloud_id, volume_id, api_token):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id
                           + '/volumes/' + volume_id, api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req


    #################################################
    #                 USER-ACTIONS                  #
    #################################################

    def login(self, email, password, cookie=None):
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
        req = MistRequests(uri=self.uri + '/api/v1/tokens',
                           api_token=api_token)
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

    #################################################
    #                WHITELIST_IPS                  #
    #################################################

    def request_whitelist_ip(self, owner_email, api_token):
        data = {
            'email': owner_email
        }
        req = MistRequests(uri=self.uri + '/request-whitelist-ip',
                           api_token=api_token, data=data)
        req.delete = req.unavailable_api_call
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def confirm_whitelist_ip(self, api_token, key=''):
        data = {
            'key': key
        }
        req = MistRequests(uri=self.uri + '/confirm-whitelist',
                           api_token=api_token, data=data)
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.post = req.unavailable_api_call
        return req

    def whitelist_ips(self, api_token, ips=None):
        data = {
            'ips': ips
        }
        req = MistRequests(uri=self.uri + '/api/v1/whitelist',
                           api_token=api_token, data=json.dumps(data))
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req
