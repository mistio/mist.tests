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
    response = mist_core.edit_template(template_id='dummy', name='',
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
#                                       stack_id='dummy').post()
#     assert_response_not_found(response)
#     print "Success!!!"


def test_create_stack_no_api_token(pretty_print, mist_core):
    response = mist_core.create_stack(api_token='', name='test',
                                      stack_id='dummy').post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_stack_wrong_api_token(pretty_print, mist_core, owner_api_token):
    response = mist_core.create_stack(api_token='00' + owner_api_token[:-2], name='test',
                                      stack_id='dummy').post()
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

############################################################################
#                          Functional Testing                              #
############################################################################
