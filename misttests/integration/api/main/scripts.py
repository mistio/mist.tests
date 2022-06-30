from misttests.integration.api.helpers import *

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_scripts(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_scripts(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print("Success!!!")


def test_add_script_missing_parameter(pretty_print, mist_core, owner_api_token,
                                      script_missing_param):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=script_missing_param).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_add_script_missing_script(pretty_print, mist_core,
                                   owner_api_token, base_exec_inline_script):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=base_exec_inline_script).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_add_script_wrong_parameter(pretty_print, mist_core, owner_api_token,
                                    script_wrong_param):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=script_wrong_param).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_add_script_wrong_script(pretty_print, mist_core, owner_api_token,
                                 script_wrong_script, base_exec_inline_script):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=base_exec_inline_script,
                                    script=script_wrong_script).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_add_script_wrong_entrypoint(pretty_print, mist_core,
                                     owner_api_token, base_exec_inline_script):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=base_exec_inline_script,
                                    entrypoint='/home/yada/yada').post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_add_ansible_wrong_yaml_format(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data={'name':'test',
                                                 'location_type':'inline',
                                                 'exec_type':'ansible'},
                                    script=ansible_script_with_error,
                                    entrypoint='').post()
    assert_response_server_error(response)
    print("Success!!!")


def test_show_script_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.show_script(owner_api_token,
                                     script_id='dummy1234').get()
    assert_response_not_found(response)
    print("Success!!!")


def test_delete_script_wrong_api_token(pretty_print, mist_core,
                                       owner_api_token):
    response = mist_core.delete_script(api_token='00' + owner_api_token[:-2],
                                       script_id='bla').delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_delete_script_wrong_script_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_script(api_token=owner_api_token,
                                       script_id='bla').delete()
    assert_response_not_found(response)
    print("Success!!!")


def test_download_script_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.download_script(api_token='00' + owner_api_token[:-2],
                                         script_id='bla').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_download_script_wrong_script_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.download_script(api_token=owner_api_token,
                                         script_id='bla').get()
    assert_response_not_found(response)
    print("Success!!!")


def test_url_script_wrong_api_token(pretty_print, mist_core,
                                    owner_api_token):
    response = mist_core.url_script(api_token='00' + owner_api_token[:-2],
                                    script_id='bla').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_url_script_wrong_script_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.url_script(api_token=owner_api_token,
                                    script_id='bla').get()
    assert_response_not_found(response)
    print("Success!!!")


def test_delete_multiple_scripts_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_scripts(api_token='00' + owner_api_token[:-2],
                                        script_ids=[]).delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_delete_multiple_scripts_no_script_ids(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_scripts(api_token=owner_api_token,
                                        script_ids=[]).delete()
    assert_response_bad_request(response)
    print("Success!!!")


def test_delete_multiple_wrong_script_ids(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_scripts(api_token=owner_api_token,
                                        script_ids=['bla', 'bla2']).delete()
    assert_response_not_found(response)
    print("Success!!!")


def test_edit_script_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_script(api_token=owner_api_token,
                                     script_id='bad', new_name='dummy').put()
    assert_response_not_found(response)
    print("Success!!!")


def test_edit_script_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_script(api_token='00' + owner_api_token[:-2],
                                     script_id='bad', new_name='dummy').put()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_edit_script_no_new_name(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_script(api_token=owner_api_token,
                                     script_id='bla', new_name='').put()
    assert_response_not_found(response)
    print("Success!!!")


############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestSimpleUserScript:
    def test_add_script_duplicate_name(self, pretty_print, cache, mist_core,
                             owner_api_token):

        script_data = {'location_type':'inline','exec_type':'executable', 'name': 'Script1'}
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=bash_script).post()
        assert_response_ok(response)

        cache.set('bash_inline', response.json()['id'])
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=bash_script).post()
        assert_response_conflict(response)
        script_data['name'] = 'Script2'
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=bash_script).post()
        assert_response_ok(response)
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        cache.set('script_id', response.json()[0]['id'])
        print("Success!!!")

    def test_setup_machine(self, pretty_print, cache, mist_core,
                           owner_api_token):
        # add cloud_key

        response = mist_core.add_key(
                name = uniquify_string('kvm_key'),
                private = safe_get_var('clouds/kvm', 'key'),
                api_token=owner_api_token).put()
        assert_response_ok(response)
        key_id = response.json()['id']
        kwargs = {
           'machines': [{
               'machine_hostname': safe_get_var('clouds/kvm', 'hostname'),
               'machine_name': '',
               'operating_system': 'unix',
               'machine_key': key_id,
               'user': 'root',
               'machine_port': '22',
               'monitoring': False
           }]
        }
        # add cloud
        response = mist_core.add_cloud(title='KVM',
                                       provider='bare_metal',
                                       api_token=owner_api_token,
                                       **kwargs).post()
        assert_response_ok(response)
        cloud_id = response.json()['id']

        # get machine_id
        response = mist_core.list_machines(cloud_id,
                                           api_token=owner_api_token).get()
        assert_response_ok(response)
        machine_id = response.json()[0]['machine_id']
        internal_id = response.json()[0]['id']

        key_associations = list(response.json()[0]['key_associations'].values())[0]
        assert_equal(key_id, key_associations['key'])
        assert_equal(internal_id, key_associations['machine'])
        cache.set('cloud', cloud_id)
        cache.set('machine', machine_id)

    def test_run_bash_inline(self, pretty_print, cache, mist_core,
                             owner_api_token):

        response = mist_core.run_script(
            api_token=owner_api_token,
            cloud_id=cache.get('cloud', ''),
            machine_id=cache.get('machine', ''),
            script_id=cache.get('bash_inline', ''),
            job_id='',
            env='FILE_PATH=~/test_file',
            params='-u thin -f thingirl').post()

        assert_response_ok(response)

        job_id = response.json()['job_id']
        # Wait for job log to become available
        params = [('action', 'script_finished')]
        print(mist_core.get_logs(owner_api_token, params).get().json())
        assert mist_core.poll_logs(owner_api_token,
                                   params=params,
                                   data={
                                       'job_id': job_id})

        response = mist_core.show_job(
             api_token=owner_api_token,
             job_id=job_id
        ).get()

        assert_response_ok(response)

        data = response.json()
        assert_equal(data['error'], False)
        assert_not_equal(data['finished_at'], 0)
        assert_equal(data['logs'][-1]['stdout'],
                     'Username: thin\nFull Name: thingirl\n0\n0\n')

    def test_show_script(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.show_script(owner_api_token,
                                         cache.get('script_id', '')).get()
        assert_response_ok(response)
        print("Success!!!")

    # def test_url_script(self, pretty_print, cache, mist_core, owner_api_token):
    #     response = mist_core.url_script(owner_api_token,
    #                                     cache.get('script_id', '')).get()
    #     assert_response_ok(response)
    #     print "Success!!!"

    def test_download_script(self, pretty_print, cache, mist_core,
                             owner_api_token):
        response = mist_core.download_script(api_token=owner_api_token,
                                             script_id=cache.get('script_id', '')).get()
        assert_response_ok(response)
        print("Success!!!")

    def test_edit_script(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.edit_script(owner_api_token, cache.get('script_id',''),
                                         new_name='Renamed').put()
        assert_response_ok(response)
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        for script in response.json():
            if script['name'] == 'Renamed':
                print("Success!!!")
                return
        assert False, "Renaming script did not work!!!"

    def test_edit_script_missing_parameter(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.edit_script(owner_api_token, cache.get('script_id',''),
                                         new_name='').put()
        assert_response_bad_request(response)
        print("Success!!!")

    def test_delete_script(self, pretty_print, cache, mist_core, owner_api_token):
        response = mist_core.delete_script(api_token=owner_api_token,
                                           script_id=cache.get('script_id','')).delete()
        assert_response_ok(response)
        response = mist_core.show_script(owner_api_token,
                                         cache.get('script_id', '')).get()
        assert_response_not_found(response)
        response = mist_core.edit_script(owner_api_token, cache.get('script_id', ''),
                                         new_name='dummy').put()
        assert_response_not_found(response)
        response = mist_core.delete_script(api_token=owner_api_token,
                                           script_id=cache.get('script_id', '')).delete()
        assert_response_not_found(response)
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1
        print("Success!!!")

    def test_add_ansible_script_inline(self, pretty_print, mist_core,
                                owner_api_token):
        script_data = {'location_type': 'inline', 'exec_type': 'ansible', 'name': 'AnsibleScript'}
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=ansible_script).post()
        assert_response_ok(response)
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print("Success!!!")

    def test_add_ansible_script_wrong_format(self, pretty_print, mist_core,
                                             owner_api_token, cache):
        script_data = {'location_type': 'inline', 'exec_type': 'ansible', 'name': 'AnsibleScript2'}
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=ansible_script_with_error).post()
        assert_response_server_error(response)
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        cache.set('script_id', response.json()[0]['id'])
        print("Success!!!")

    def test_delete_multiple_scripts_wrong_id(self, pretty_print, cache, mist_core, owner_api_token):
        mist_core.delete_scripts(api_token=owner_api_token,
                                 script_ids=[cache.get('script_id', ''), 'bla2']).delete()
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        cache.set('script_id', response.json()[0]['id'])
        assert len(response.json()) == 1, "Valid script was not deleted!"
        print("Success!!!")

    def test_delete_multiple_scripts_duplicate_script_ids(self, pretty_print, cache,
                                                          mist_core, owner_api_token):
        mist_core.delete_scripts(api_token=owner_api_token,
                                 script_ids=[cache.get('script_id', ''), cache.get('script_id', ''),
                                             cache.get('script_id', ''), 'bla2']).delete()
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 0, "Valid script was not deleted!"
        print("Success!!!")

    def test_delete_multiple_scripts(self, pretty_print, cache,
                                     mist_core, owner_api_token):
        script_data = {'location_type':'inline','exec_type':'executable', 'name': 'Script5'}
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=bash_script).post()
        assert_response_ok(response)

        script_data = {'location_type':'inline','exec_type':'executable', 'name': 'Script6'}
        response = mist_core.add_script(api_token=owner_api_token, script_data=script_data,
                                        script=bash_script).post()
        assert_response_ok(response)

        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert len(response.json()) == 2
        assert_response_ok(response)
        cache.set('script_id', response.json()[0]['id'])
        cache.set('script_id_2', response.json()[1]['id'])
        mist_core.delete_scripts(api_token=owner_api_token,
                                 script_ids=[cache.get('script_id', ''), cache.get('script_id_2', '')]).delete()
        response = mist_core.list_scripts(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 0, "Not all of the scripts were deleted!"
        print("Success!!!")

    def test_run_bash_url(self, pretty_print, cache, mist_core,
                          owner_api_token):

        response = mist_core.add_script(api_token=owner_api_token,
                                        script_data={
                                            'name': 'BashUrl',
                                            'description': '',
                                            'exec_type': 'executable',
                                            'location_type': 'url',
                                            'script_url': bash_url,
                                            'entrypoint': 'bash_example.sh'},
                                        ).post()
        assert_response_ok(response)
        script_id = response.json()['id']

        response = mist_core.run_script(
            api_token=owner_api_token,
            cloud_id=cache.get('cloud', ''),
            machine_id=cache.get('machine', ''),
            script_id=script_id,
            job_id='').post()

        assert_response_ok(response)

        job_id = response.json()['job_id']
        # Wait for job log to become available
        params = [('action', 'script_finished')]
        assert mist_core.poll_logs(owner_api_token,
                                   params=params,
                                   data={
                                       'job_id': job_id})

        response = mist_core.show_job(
             api_token=owner_api_token,
             job_id=job_id
        ).get()

        assert_response_ok(response)
        data = response.json()
        assert_equal(data['error'], False)
        assert_not_equal(data['finished_at'], 0)
        assert_equal(data['logs'][-1]['stdout'], "whatever\nwhat else\n0\n0\n")
        
        
    def test_run_bash_git(self, pretty_print, cache, mist_core,
                          owner_api_token):

        response = mist_core.add_script(api_token=owner_api_token,
                                        script_data={
                                            'name': 'bash_git',
                                            'description': '',
                                            'exec_type': 'executable',
                                            'location_type': 'github',
                                            'script_github': examples_repo,
                                            'entrypoint': 'bash_example.sh'},
                                        ).post()
        assert_response_ok(response)
        script_id = response.json()['id']

        response = mist_core.run_script(
            api_token=owner_api_token,
            cloud_id=cache.get('cloud', ''),
            machine_id=cache.get('machine', ''),
            script_id=script_id,
            job_id='').post()

        assert_response_ok(response)

        job_id = response.json()['job_id']
        # Wait for job log to become available
        params = [('action', 'script_finished')]
        assert mist_core.poll_logs(owner_api_token,
                                   params=params,
                                   data={
                                       'job_id': job_id})
        response = mist_core.show_job(
             api_token=owner_api_token,
             job_id=job_id
        ).get()

        assert_response_ok(response)
        data = response.json()
        assert_equal(data['error'], False)
        assert_equal(data['logs'][-1]['stdout'], "whatever\nwhat else\n0\n0\n")
        assert_not_equal(data['finished_at'], 0)

    def test_run_ansible_inline(self, pretty_print, cache, mist_core,
                          owner_api_token):

        response = mist_core.add_script(api_token=owner_api_token,
                                        script_data={
                                            'name': 'ansible_inline',
                                            'description': '',
                                            'exec_type': 'ansible',
                                            'location_type': 'inline',
                                            'script_inline': ansible_script,
                                            'entrypoint': ''},
                                        ).post()
        assert_response_ok(response)
        script_id = response.json()['id']

        response = mist_core.run_script(
            api_token=owner_api_token,
            cloud_id=cache.get('cloud', ''),
            machine_id=cache.get('machine', ''),
            script_id=script_id,
            job_id='').post()

        assert_response_ok(response)

        job_id = response.json()['job_id']
        # Wait for job log to become available
        params = [('action', 'script_finished')]
        assert mist_core.poll_logs(owner_api_token,
                                   params=params,
                                   data={
                                       'job_id': job_id})
        response = mist_core.show_job(
             api_token=owner_api_token,
             job_id=job_id
        ).get()
        
        assert_response_ok(response)
        data = response.json()
        assert_equal(data['error'], False)
        assert "Does this work?" in data['logs'][-1]['stdout']
        assert_not_equal(data['finished_at'], 0)  
        
    def test_run_ansible_git(self, pretty_print, cache, mist_core,
                          owner_api_token):

        response = mist_core.add_script(api_token=owner_api_token,
                                        script_data={
                                            'name': 'ansible_git',
                                            'description': '',
                                            'exec_type': 'ansible',
                                            'location_type': 'github',
                                            'script_github': examples_repo,
                                            'entrypoint': 'create_file.yaml'},
                                        ).post()
        assert_response_ok(response)
        script_id = response.json()['id']

        response = mist_core.run_script(
            api_token=owner_api_token,
            cloud_id=cache.get('cloud', ''),
            machine_id=cache.get('machine', ''),
            script_id=script_id,
            job_id='').post()

        assert_response_ok(response)

        job_id = response.json()['job_id']
        # Wait for job log to become available
        params = [('action', 'script_finished')]
        assert mist_core.poll_logs(owner_api_token,
                                   params=params,
                                   data={
                                       'job_id': job_id})
        response = mist_core.show_job(
             api_token=owner_api_token,
             job_id=job_id
        ).get()
        
        assert_response_ok(response)
        data = response.json()
        assert_equal(data['error'], False)
        assert "Does this work?" in data['logs'][-1]['stdout']
        assert_not_equal(data['finished_at'], 0)   
    
    def test_run_ansible_url(self, pretty_print, cache, mist_core,
                          owner_api_token):

        response = mist_core.add_script(api_token=owner_api_token,
                                        script_data={
                                            'name': 'ansible_url',
                                            'description': '',
                                            'exec_type': 'ansible',
                                            'location_type': 'url',
                                            'script_url': ansible_url,
                                            'entrypoint': 'create_file.yaml'},
                                        ).post()
        assert_response_ok(response)
        script_id = response.json()['id']

        response = mist_core.run_script(
            api_token=owner_api_token,
            cloud_id=cache.get('cloud', ''),
            machine_id=cache.get('machine', ''),
            script_id=script_id,
            job_id='').post()

        assert_response_ok(response)

        job_id = response.json()['job_id']
        # Wait for job log to become available
        params = [('action', 'script_finished')]
        assert mist_core.poll_logs(owner_api_token,
                                   params=params,
                                   data={
                                       'job_id': job_id})
        response = mist_core.show_job(
             api_token=owner_api_token,
             job_id=job_id
        ).get()
        
        assert_response_ok(response)
        data = response.json()
        assert_equal(data['error'], False)
        assert "Does this work?" in data['logs'][-1]['stdout']
        assert_not_equal(data['finished_at'], 0)  

    def test_run_ansible_with_params(self, pretty_print, cache, mist_core,
                                     owner_api_token):

        response = mist_core.add_script(api_token=owner_api_token,
                                        script_data={
                                            'name': 'ansible_w_params',
                                            'description': '',
                                            'exec_type': 'ansible',
                                            'location_type': 'inline',
                                            'script_inline': ansible_script_w_params,
                                            'entrypoint': ''},
                                        ).post()
        assert_response_ok(response)
        script_id = response.json()['id']

        content = f"'{uniquify_string('Does this work?')}'"
        response = mist_core.run_script(
            api_token=owner_api_token,
            cloud_id=cache.get('cloud', ''),
            machine_id=cache.get('machine', ''),
            script_id=script_id,
            params=f'"content={content}" "dest=~/test_file"',
            job_id='').post()

        assert_response_ok(response)

        job_id = response.json()['job_id']
        # Wait for job log to become available
        params = [('action', 'script_finished')]
        assert mist_core.poll_logs(owner_api_token,
                                   params=params,
                                   data={
                                       'job_id': job_id})
        response = mist_core.show_job(
             api_token=owner_api_token,
             job_id=job_id
        ).get()

        content = content[1:-2]  # Remove extra quotes

        assert_response_ok(response)
        data = response.json()
        assert_equal(data['error'], False)
        assert content in data['logs'][-1]['stdout']
        assert_not_equal(data['finished_at'], 0)