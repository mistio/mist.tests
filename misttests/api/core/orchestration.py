from misttests.api.helpers import *
from misttests import config

import pytest


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_templates(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_templates(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"

# GETS 500
# def test_add_template_missing_parameter(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_template(name='', location_type='github',
#                                       api_token=owner_api_token).post()
#     assert_response_bad_request(response)
#     print "Success!!!"


def test_add_template_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.add_template(name='test', location_type='github',
                                      api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_add_template_no_api_token(pretty_print, mist_core):
    response = mist_core.add_template(name='test', location_type='github',
                                      api_token='').post()
    assert_response_forbidden(response)
    print "Success!!!"


# GETS 500
# def test_add_template_ok(pretty_print, mist_core, owner_api_token):
#     response = mist_core.add_template(name='test', location_type='github',
#                                       api_token=owner_api_token).post()
#     assert_response_ok(response)
#     print "Success!!!"


def test_edit_template_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_template(template_id='dummy', name='test',
                                       api_token=owner_api_token).put()
    assert_response_not_found(response)
    print "Success!!!"


def test_edit_template_no_api_token(pretty_print, mist_core):
    response = mist_core.edit_template(template_id='dummy', name='test',
                                       api_token='').put()
    assert_response_forbidden(response)
    print "Success!!!"


def test_edit_template_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_template(template_id='dummy', name='test',
                                       api_token='00' + owner_api_token[:-2]).put()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_edit_template_missing_parameter(pretty_print, mist_core, owner_api_token):
    response = mist_core.edit_template(template_id='dummy', name='test',
                                       api_token=owner_api_token).put()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_template_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_template(template_id='dummy', api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success"


def test_delete_template_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_template(template_id='dummy', api_token='').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_template_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_template(template_id='dummy', api_token='00' + owner_api_token[:-2]).delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_template_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.show_template(template_id='dummy', api_token='00' + owner_api_token[:-2]).get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_template_no_api_token(pretty_print, mist_core):
    response = mist_core.show_template(template_id='dummy', api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_template_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.show_template(template_id='dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_list_stacks(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_stacks(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"

# GETS 500
# def test_create_stack(pretty_print, mist_core, owner_api_token):
#     response = mist_core.create_stack(api_token=owner_api_token, name='test',
#                                       template_id='dummy').post()
#     assert_response_not_found(response)
#     print "Success!!!"


def test_create_stack_no_api_token(pretty_print, mist_core):
    response = mist_core.create_stack(api_token='', name='test',
                                      template_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_stack_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_stack(api_token='00' + owner_api_token[:-2], name='test',
                                      template_id='dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_stack_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_stack(stack_id='dummy', api_token=owner_api_token).delete()
    assert_response_not_found(response)
    print "Success"


def test_delete_stack_no_api_token(pretty_print, mist_core):
    response = mist_core.delete_stack(stack_id='dummy', api_token='').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_stack_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.delete_stack(stack_id='dummy', api_token='00' + owner_api_token[:-2]).delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_stack_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.show_stack(stack_id='dummy', api_token='00' + owner_api_token[:-2]).get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_stack_no_api_token(pretty_print, mist_core):
    response = mist_core.show_stack(stack_id='dummy', api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_show_stack_wrong_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.show_stack(stack_id='dummy', api_token=owner_api_token).get()
    assert_response_not_found(response)
    print "Success!!!"


def test_run_workflow_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.run_workflow(stack_id='dummy', api_token='00' + owner_api_token[:-2]).post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_run_workflow_no_api_token(pretty_print, mist_core):
    response = mist_core.run_workflow(stack_id='dummy', api_token='').post()
    assert_response_forbidden(response)
    print "Success!!!"


#def test_run_workflow_wrong_id(pretty_print, mist_core, owner_api_token):
 #   response = mist_core.run_workflow(stack_id='dummy', api_token=owner_api_token).post()
 #   assert_response_not_found(response)
 #   print "Success!!!"


############################################################################
#                          Functional Testing                              #
############################################################################

@pytest.mark.incremental
class TestOrchestrationFunctionality:

    def test_add_docker_orchestrator(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.add_cloud(title='Docker', provider='docker', api_token=owner_api_token,
                                       docker_host=config.CREDENTIALS['DOCKER_ORCHESTRATOR']['host'],
                                       docker_port=config.CREDENTIALS['DOCKER_ORCHESTRATOR']['port']).post()
        assert_response_ok(response)
        cache.set('cloud_id', response.json()['id'])
        print "Success!!!"

    def test_add_template_missing_parameter(self, pretty_print, mist_core, owner_api_token):
        response = mist_core.add_template(api_token=owner_api_token, name='Template1', location_type='github',
                                          template_github='https://github.com/mistio/kubernetes-blueprint').post()
        assert_response_bad_request(response)
        response = mist_core.add_template(api_token=owner_api_token, name='Template1', location_type='github',
                                          template_github='',
                                          entrypoint='blueprint.yaml').post()
        assert_response_bad_request(response)
        response = mist_core.add_template(api_token=owner_api_token, name='Template1', location_type='url',
                                          template_github='https://github.com/mistio/kubernetes-blueprint',
                                          entrypoint='blueprint.yaml').post()
        assert_response_bad_request(response)
        response = mist_core.add_template(api_token=owner_api_token, name='Template1', location_type='inline',
                                          template_github='https://github.com/mistio/kubernetes-blueprint',
                                          entrypoint='blueprint.yaml').post()
        assert_response_bad_request(response)
        print "Success!!!"

    def test_add_template_ok(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.add_template(api_token=owner_api_token, name='Template1', location_type='github',
                                          template_github='https://github.com/mistio/kubernetes-blueprint',
                                          entrypoint="blueprint.yaml").post()
        cache.set('template_id', response.json()['id'])
        assert_response_ok(response)
        response = mist_core.add_template(api_token=owner_api_token, name='Template2', location_type='github',
                                          template_github='https://github.com/mistio/kubernetes-blueprint',
                                          entrypoint="blueprint.yaml").post()
        cache.set('template_to_use_id', response.json()['id'])
        assert_response_ok(response)
        response = mist_core.list_templates(api_token=owner_api_token).get()
        assert len(response.json()) == 2, "Although template has been added, it is not visible in list_templates"
        # response = mist_core.add_template(api_token=owner_api_token, name='Template2', location_type='url',
        #                                   template_url='https://github.com',
        #                                   entrypoint="/mistio/kubernetes-blueprint/blueprint.yaml").post()
        # assert_response_ok(response)
        # response = mist_core.list_templates(api_token=owner_api_token).get()
        # assert len(response.json()) == 2, "Although template has been added, it is not visible in list_templates"
        print "Success!!!"

    # def test_add_template_conflict(self, pretty_print, mist_core, owner_api_token):
    #     response = mist_core.add_template(api_token=owner_api_token, name='Template1', location_type='github',
    #                                       template_github='https://github.com/mistio/kubernetes-blueprint',
    #                                       entrypoint="blueprint.yaml").post()
    #     assert_response_conflict(response)
    #     print "Success!!!"

# below isok
    # def test_edit_template_missing_param(self, pretty_print, mist_core, owner_api_token, cache):
    #     response = mist_core.edit_template(api_token=owner_api_token,
    #                                        template_id=cache.get('template_id', ''),
    #                                        name='').put()
    #     assert_response_bad_request(response)
    #     print "Success!!!"

    def test_edit_template_ok(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.edit_template(api_token=owner_api_token,
                                           template_id=cache.get('template_id', ''),
                                           name='EditedTemplate').put()
        assert_response_ok(response)
        response = mist_core.list_templates(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert 'EditedTemplate' in response.json()[0]['name'], \
            'Template has not been renamed although response was 200!'
        print "Success!!!"

    def test_delete_template_ok(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.delete_template(api_token=owner_api_token,
                                             template_id=cache.get('template_id', '')).delete()
        assert_response_ok(response)
        response = mist_core.delete_template(api_token=owner_api_token,
                                             template_id=cache.get('template_id', '')).delete()
        assert_response_not_found(response)
        response = mist_core.list_templates(api_token=owner_api_token).get()
        assert len(response.json()) == 1, "Although template has been deleted, it is still visible in list_templates"
        print "Success!!!"

    def test_show_template(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.show_template(api_token=owner_api_token,
                                           template_id=cache.get('template_id', '')).get()
        assert_response_not_found(response)
        response = mist_core.show_template(api_token=owner_api_token,
                                           template_id=cache.get('template_to_use_id', '')).get()
        assert_response_ok(response)
        print "Success!!!"

    def test_create_stack(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.create_stack(api_token=owner_api_token, name='TestStack',
                                          template_id=cache.get('template_to_use_id', ''),
                                          cloud_id=cache.get('cloud_id',''), machine_name='Spiros-test').post()
        assert_response_ok(response)
        cache.set('stack_id', response.json()['id'])
        response = mist_core.list_stacks(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 1, "Although stack has been added, it is not" \
                                          "visible in list_stacks"
        print "Success!!!"

    def test_delete_stack(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.delete_stack(api_token=owner_api_token,
                                          stack_id=cache.get('stack_id',''))
        assert_response_ok(response)
        response = mist_core.list_stacks(api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 0, "Although stack has been deleted, it is still" \
                                          "visible in list_stacks"
        print "Success!!!"

# check UI
# CODE REVIEWS

# scale_up
# scale_down
# other options

# how to add template wih location_type=url
# should return conflict when adding a template with same name
