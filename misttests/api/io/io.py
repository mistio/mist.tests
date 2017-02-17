import json

from misttests.api.mistrequests import MistRequests


class MistIoApi(object):

    def __init__(self, uri):
        self.uri = uri

    def supported_providers(self, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/providers', api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_clouds(self, api_token=None):

        req = MistRequests(uri=self.uri + '/api/v1/clouds', api_token=api_token)
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
        req = MistRequests(uri=self.uri + '/api/v1/clouds', data=json.dumps(payload),
                           api_token=api_token)
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
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id, cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

    def toggle_cloud(self, cloud_id, api_token=None, new_state=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id,
                           data={'new_state':new_state}, api_token=api_token)
        req.get = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        req.put = req.unavailable_api_call
        return req

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

    def list_sizes(self, cloud_id, cookie=None, csrf_token=None,
                   api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id + '/sizes',
                           cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_locations(self, cloud_id, cookie=None, csrf_token=None,
                       api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id + '/locations',
                           cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)

        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def list_machines(self, cloud_id, cookie=None, csrf_token=None,
                      api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id + '/machines',
                           cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def create_machine(self, cloud_id, key_id, name, provider, location, image, size,
                       script="", disk=None, image_extra=None, cookie=None,
                       csrf_token=None, api_token=None, cron_enable=False,
                       cron_type=None, cron_entry=None, cron_script=None,
                       cron_name=None, async=False, monitoring=False,
                       cloud_init="", location_name='', job_id=None):
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
        req = MistRequests(uri=self.uri + '/api/v1/clouds/' + cloud_id + '/machines',
                           cookie=cookie, data=json.dumps(payload), timeout=600,
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def destroy_machine(self, cloud_id, machine_id, cookie=None,
                        csrf_token=None, api_token=None):
        uri = self.uri + '/api/v1/clouds/' + cloud_id + '/machines/' + machine_id
        req = MistRequests(uri=uri, data={'action': 'destroy'}, cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def start_machine(self, cloud_id, machine_id, cookie=None,
                      csrf_token=None, api_token=None):
        uri = self.uri + '/api/v1/clouds/' + cloud_id + '/machines/' + machine_id
        req = MistRequests(uri=uri, data={'action': 'start'}, cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def stop_machine(self, cloud_id, machine_id, cookie=None, csrf_token=None,
                     api_token=None):
        uri = self.uri + '/api/v1/clouds/' + cloud_id + '/machines/' + machine_id
        req = MistRequests(uri - uri, data={'action': 'stop'}, cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def reboot_machine(self, cloud_id, machine_id, cookie=None,
                       csrf_token=None, api_token=None):
        uri = self.uri + '/api/v1/clouds/' + cloud_id + '/machines/' + machine_id
        req = MistRequests(uri=uri, cookie=cookie, data={'action': 'reboot'},
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def machine_action(self, cloud_id, machine_id, cookie=None,
                       csrf_token=None, api_token=None, action = ''):
        data={}
        if action:
            data= {'action': action}
        uri = self.uri + '/api/v1/clouds/' + cloud_id + '/machines/' + machine_id
        req = MistRequests(uri=uri, cookie=cookie, data=data,
                           csrf_token=csrf_token, api_token=api_token)

        req.get = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def associate_key(self, api_token, cloud_id, machine_id, key_id):
        uri = self.uri + '/api/v1/clouds/%s/machines/%s/keys/%s' \
                         '' % (cloud_id, machine_id, key_id)
        req = MistRequests(uri=uri, api_token=api_token)

        req.get = req.unavailable_api_call
        req.post = req.unavailable_api_call
        req.delete = req.unavailable_api_call

        return req

    def list_keys(self, cookie=None, csrf_token=None, api_token=None):
        req = MistRequests(uri=self.uri + '/api/v1/keys', cookie=cookie,
                           csrf_token=csrf_token, api_token=api_token)
        req.post = req.unavailable_api_call
        req.put = req.unavailable_api_call
        req.delete = req.unavailable_api_call
        return req

    def add_key(self, name, private, cookie=None, csrf_token=None,
                 api_token=None):
        payload = {
            'name': name,
            'priv': private
        }
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
        req = MistRequests(uri=self.uri + '/api/v1/keys/' + key_id + '/private',
                           cookie=cookie, csrf_token=csrf_token,
                           api_token=api_token)
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
