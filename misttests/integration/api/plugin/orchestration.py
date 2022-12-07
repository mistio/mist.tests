import time
import uuid
import pytest
from requests import codes
from misttests.config import inject_vault_credentials
from misttests.integration.api.helpers import *

TPL_NAME_PREFIX = 'test-template'
CLOUD_NAME_PREFIX = 'test-cloud'
KEY_NAME_PREFIX = 'test-key'
STACK_NAME_PREFIX = 'test-stack'
STACK_IMAGE_NAME = 'ubuntu-focal-20.04-amd64-server'
STACK_SIZE_NAME = 't3.medium'
STACK_LOCATION_NAME = "ap-northeast-1a"
STACK_INSTALL_WAIT = 60 * 4
STACK_INSTALL_WAIT_FOR_STORY = 10
STACK_INSTALL_WAIT_STORY_REQUEST = 10
STACK_DELETE_WAIT = 60 * 4


def generate_template_name():
    return f'{TPL_NAME_PREFIX}-{str(uuid.uuid4())[:8]}'


def generate_cloud_name():
    return f'{CLOUD_NAME_PREFIX}-{str(uuid.uuid4())[:8]}'


def generate_stack_name():
    return f'{STACK_NAME_PREFIX}-{str(uuid.uuid4())[:8]}'


def generate_key_name():
    return f'{KEY_NAME_PREFIX}-{str(uuid.uuid4())[:8]}'

############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_templates(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.list_templates(api_token=owner_api_token).get()
    assert_response_ok(response)
    print("Success!!!")


def test_add_template_missing_parameter(pretty_print, mist_api_v1,
                                        owner_api_token):
    response = mist_api_v1.add_template(name='', location_type='github',
                                      api_token=owner_api_token).post()
    assert_response_bad_request(response)
    print("Success!!!")


def test_add_template_wrong_api_token(pretty_print, mist_api_v1,
                                      owner_api_token):
    bad_api_token = '00' + owner_api_token[:-2]
    response = mist_api_v1.add_template(name='test', location_type='github',
                                      api_token=bad_api_token).post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_add_template_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.add_template(name='test', location_type='github',
                                      api_token='').post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_edit_template_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.edit_template(template_id='dummy', name='test',
                                       api_token=owner_api_token).put()
    assert_response_not_found(response)
    print("Success!!!")


def test_edit_template_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.edit_template(template_id='dummy', name='test',
                                       api_token='').put()
    assert_response_forbidden(response)
    print("Success!!!")


def test_edit_template_wrong_api_token(pretty_print, mist_api_v1,
                                       owner_api_token):
    bad_api_token = '00' + owner_api_token[:-2]
    response = mist_api_v1.edit_template(template_id='dummy', name='test',
                                       api_token=bad_api_token).put()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_edit_template_missing_parameter(pretty_print, mist_api_v1,
                                         owner_api_token):
    response = mist_api_v1.edit_template(template_id='dummy', name='test',
                                       api_token=owner_api_token).put()
    assert_response_not_found(response)
    print("Success!!!")


def test_delete_template_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.delete_template(
        template_id='dummy', api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print("Success")


def test_delete_template_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_template(
        template_id='dummy', api_token='').delete()
    assert_response_forbidden(response)
    print("Success!!!")


def test_delete_template_wrong_api_token(pretty_print, mist_api_v1,
                                         owner_api_token):
    response = mist_api_v1.delete_template(
        template_id='dummy', api_token='00' + owner_api_token[:-2]).delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_template_wrong_api_token(pretty_print, mist_api_v1,
                                       owner_api_token):
    response = mist_api_v1.show_template(
        template_id='dummy', api_token='00' + owner_api_token[:-2]).get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_template_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.show_template(template_id='dummy', api_token='').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_template_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.show_template(
        template_id='dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print("Success!!!")


def test_list_stacks(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.list_stacks(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print("Success!!!")


def test_create_stack_wrong_template_id(pretty_print, mist_api_v1,
                                        owner_api_token):
    response = mist_api_v1.create_stack(api_token=owner_api_token, name='test',
                                      template_id='dummy').post()
    assert_response_not_found(response)
    print("Success!!!")


def test_create_stack_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.create_stack(api_token='', name='test',
                                      template_id='dummy').post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_create_stack_wrong_api_token(pretty_print, mist_api_v1,
                                      owner_api_token):
    bad_api_token = '00' + owner_api_token[:-2]
    response = mist_api_v1.create_stack(api_token=bad_api_token, name='test',
                                      template_id='dummy').post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_delete_stack_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.delete_stack(
        stack_id='dummy', api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print("Success")


def test_delete_stack_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.delete_stack(stack_id='dummy', api_token='').delete()
    assert_response_forbidden(response)
    print("Success!!!")


def test_delete_stack_wrong_api_token(pretty_print, mist_api_v1,
                                      owner_api_token):
    response = mist_api_v1.delete_stack(
        stack_id='dummy', api_token='00' + owner_api_token[:-2]).delete()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_stack_wrong_api_token(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.show_stack(
        stack_id='dummy', api_token='00' + owner_api_token[:-2]).get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_stack_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.show_stack(stack_id='dummy', api_token='').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_show_stack_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.show_stack(
        stack_id='dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print("Success!!!")


def test_run_workflow_wrong_api_token(pretty_print, mist_api_v1,
                                      owner_api_token):
    response = mist_api_v1.run_workflow(
        stack_id='dummy', api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_run_workflow_no_api_token(pretty_print, mist_api_v1):
    response = mist_api_v1.run_workflow(stack_id='dummy', api_token='').post()
    assert_response_forbidden(response)
    print("Success!!!")


def test_run_workflow_wrong_id(pretty_print, mist_api_v1, owner_api_token):
    response = mist_api_v1.run_workflow(
        stack_id='dummy', api_token=owner_api_token).post()
    assert_response_not_found(response)
    print("Success!!!")


############################################################################
#                          Functional Testing                              #
############################################################################

@pytest.mark.incremental
class TestOrchestrationFunctionality:

    def test_add_template_missing_parameter(self, pretty_print, mist_api_v1,
                                            owner_api_token):
        response = mist_api_v1.add_template(
            api_token=owner_api_token,
            name='Template1',
            location_type='github',
            template_github='https://github.com/mistio/kubernetes-blueprint'
        ).post()
        assert_response_bad_request(response)
        response = mist_api_v1.add_template(
            api_token=owner_api_token,
            name='Template1',
            location_type='github',
            template_github='',
            entrypoint='blueprint.yaml').post()
        assert_response_bad_request(response)
        response = mist_api_v1.add_template(
            api_token=owner_api_token,
            name='Template1',
            location_type='url',
            template_github='https://github.com/mistio/kubernetes-blueprint',
            entrypoint='blueprint.yaml').post()
        assert_response_bad_request(response)
        response = mist_api_v1.add_template(
            api_token=owner_api_token,
            name='Template1',
            location_type='inline',
            template_github='https://github.com/mistio/kubernetes-blueprint',
            entrypoint='blueprint.yaml').post()
        assert_response_bad_request(response)
        print("Success!!!")

    def test_add_template_ok(self, pretty_print, mist_api_v1, owner_api_token,
                             cache, template_github):
        tplname1 = generate_template_name()
        response = mist_api_v1.add_template(
            api_token=owner_api_token,
            name=tplname1,
            location_type='github',
            template_github=template_github,
            entrypoint="blueprint.yaml").post()
        assert_response_ok(response)
        cache.set('template_name', tplname1)
        cache.set('template_id', response.json()['id'])
        tplname2 = generate_template_name()
        response = mist_api_v1.add_template(
            api_token=owner_api_token,
            name=tplname2, location_type='github',
            template_github=template_github,
            entrypoint="blueprint.yaml").post()
        assert_response_ok(response)
        cache.set('template_to_use_id', response.json()['id'])
        response = mist_api_v1.list_templates(api_token=owner_api_token).get()
        assert_response_ok(response)
        tpls = response.json()
        tplnames = [tpl['name'] for tpl in tpls]
        tpls_returned = all(name in tplnames for name in [tplname1, tplname2])
        assert tpls_returned,\
            "Template added, however list_templates did not return them"
        print("Success!!!")

    def test_add_template_conflict(self, pretty_print, mist_api_v1,
                                   owner_api_token, cache):
        response = mist_api_v1.add_template(
            api_token=owner_api_token,
            name=cache.get('template_name', ''),
            location_type='github',
            template_github='https://github.com/mistio/kubernetes-blueprint',
            entrypoint="blueprint.yaml").post()
        assert_response_conflict(response)
        print("Success!!!")

    def test_edit_template_missing_param(self, pretty_print, mist_api_v1,
                                         owner_api_token, cache):
        response = mist_api_v1.edit_template(api_token=owner_api_token,
                                           template_id=cache.get(
                                               'template_id', ''),
                                           name='').put()
        assert_response_bad_request(response)
        print("Success!!!")

    def test_edit_template_ok(self, pretty_print, mist_api_v1,
                              owner_api_token, cache):
        edited_tplname = f"edited-{cache.get('template_name', '')}"
        response = mist_api_v1.edit_template(api_token=owner_api_token,
                                           template_id=cache.get(
                                               'template_id', ''),
                                           name=edited_tplname).put()
        assert_response_ok(response)
        response = mist_api_v1.list_templates(api_token=owner_api_token).get()
        assert_response_ok(response)
        tpls = response.json()
        tpl_names = [tpl['name'] for tpl in tpls]
        assert edited_tplname in tpl_names, \
            'Template rename failed, despite ok response'
        print("Success!!!")

    def test_delete_template_ok(self, pretty_print, mist_api_v1,
                                owner_api_token, cache):
        tplid = cache.get('template_id', '')
        response = mist_api_v1.delete_template(api_token=owner_api_token,
                                             template_id=tplid).delete()
        assert_response_ok(response)
        response = mist_api_v1.delete_template(api_token=owner_api_token,
                                             template_id=tplid).delete()
        assert_response_not_found(response)
        response = mist_api_v1.list_templates(api_token=owner_api_token).get()
        assert_response_ok(response)
        tpls = response.json()
        tplids = [tpl['id'] for tpl in tpls]
        assert tplid not in tplids, "Template returned, despite deletion"
        print("Success!!!")

    def test_show_template(self, pretty_print, mist_api_v1,
                           owner_api_token, cache):
        response = mist_api_v1.show_template(
            api_token=owner_api_token,
            template_id=cache.get('template_id', '')).get()
        assert_response_not_found(response)
        response = mist_api_v1.show_template(
            api_token=owner_api_token,
            template_id=cache.get('template_to_use_id', '')).get()
        assert_response_ok(response)
        print("Success!!!")

    def test_create_stack(self, pretty_print, mist_api_v1,
                          owner_api_token, cache, private_key):
        cloud_name = generate_cloud_name()
        add_cloud_kwargs = dict(
            name=cloud_name,
            provider='amazon',
            api_token=owner_api_token,
            apikey=None,
            apisecret=None,
            region=None
        )
        inject_vault_credentials(add_cloud_kwargs)
        cloud_response = mist_api_v1.add_cloud(
            **add_cloud_kwargs).post()
        assert_response_ok(cloud_response)
        key_name = generate_key_name()
        key_response = mist_api_v1.add_key(
            name=key_name,
            private=private_key,
            api_token=owner_api_token).put()
        assert_response_ok(key_response)
        key_id = key_response.json()['id']
        cloud_id = cloud_response.json()['id']
        list_images_response = mist_api_v1.list_images(
            cloud_id=cloud_id,
            api_token=owner_api_token).get()
        assert_response_ok(list_images_response)
        images = list_images_response.json()
        for image in images:
            if STACK_IMAGE_NAME in image['name']:
                image_id = image['id']
                break
        else:
            image_id = None
        assert image_id is not None, "Stack image not found"
        list_sizes_response = mist_api_v1.list_sizes(
            cloud_id=cloud_id,
            api_token=owner_api_token).get()
        sizes = list_sizes_response.json()
        for size in sizes:
            if STACK_SIZE_NAME in size['name']:
                size_id = size['id']
                break
        else:
            size_id = None
        assert size_id is not None, "Stack size not found"
        list_locations_response = mist_api_v1.list_locations(
            cloud_id=cloud_id,
            api_token=owner_api_token).get()
        locations = list_locations_response.json()
        for location in locations:
            if STACK_LOCATION_NAME in location['name']:
                location_id = location['id']
                break
        else:
            location_id = None
        assert location_id is not None, "Stack location not found"
        name = generate_stack_name()
        template_id = cache.get('template_to_use_id', '')
        response = mist_api_v1.create_stack(
            deploy=False,
            api_token=owner_api_token,
            name=name,
            template_id=template_id,
            cloud_id=cloud_id,
            key_id=key_id,
            image_id=image_id,
            size_id=size_id,
            location_id=location_id,
        ).post()
        assert_response_ok(response)
        stack = response.json()
        cache.set('stack_id', stack['id'])
        list_stacks_response = mist_api_v1.list_stacks(
            api_token=owner_api_token).get()
        assert_response_ok(list_stacks_response)
        stacks = list_stacks_response.json()
        stack_names = [s['name'] for s in stacks]
        assert name in stack_names, "Stack not returned, despite being created"
        print("Success!!!")

    def test_show_stack(self, pretty_print, mist_api_v1,
                        owner_api_token, cache):
        response = mist_api_v1.show_stack(
            api_token=owner_api_token,
            stack_id=cache.get('stack_id', '')).get()
        assert_response_ok(response)
        print("Success!!!")

    def test_install_stack(self, pretty_print, mist_api_v1,
                           owner_api_token, cache):
        stack_id = cache.get('stack_id', '')
        response = mist_api_v1.run_workflow(
            api_token=owner_api_token,
            stack_id=stack_id,
            workflow='install').post()
        assert_response_ok(response)
        job_id = response.json()['job_id']
        workflow_finished = False
        t_end = time.time() + STACK_INSTALL_WAIT
        while time.time() < t_end:
            fetch_story_response = mist_api_v1.fetch_story(
                api_token=owner_api_token,
                job_id=job_id).get()
            if fetch_story_response.status_code == codes.not_found:
                time.sleep(STACK_INSTALL_WAIT_FOR_STORY)
                continue
            assert_response_ok(fetch_story_response)
            logs = fetch_story_response.json()['logs']
            for log in logs:
                assert log['error'] is False, \
                    'Install workflow failed'
                if log['action'] == 'workflow_finished':
                    workflow_finished = True
                    break
            if workflow_finished:
                break
            time.sleep(STACK_INSTALL_WAIT_STORY_REQUEST)
        else:
            raise RuntimeError('Install stack action is taking too long')
        print("Success!!!")

    def test_delete_stack(self, pretty_print, mist_api_v1,
                          owner_api_token, cache):
        stack_id = cache.get('stack_id', '')
        response = mist_api_v1.delete_stack(
            api_token=owner_api_token,
            stack_id=stack_id).delete()
        assert_response_ok(response)
        t_end = time.time() + STACK_DELETE_WAIT
        while time.time() < t_end:
            list_stacks_response = mist_api_v1.list_stacks(
                api_token=owner_api_token).get()
            assert_response_ok(list_stacks_response)
            stacks = list_stacks_response.json()
            stack_ids = [s['id'] for s in stacks]
            if stack_id in stack_ids:
                continue
            break
        else:
            raise RuntimeError('Delete stack action is taking too long')
        print("Success!!!")
