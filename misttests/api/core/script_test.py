from misttests.api.helpers import *


############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_scripts(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_scripts(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 0
    print "Success!!!"


def test_add_script_missing_parameter(pretty_print, mist_core, owner_api_token,
                                      script_missing_param):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=script_missing_param).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_add_script_missing_script(pretty_print, cache, mist_core,
                                   owner_api_token, base_exec_inline_script):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=base_exec_inline_script).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_add_script_wrong_parameter(pretty_print, mist_core, owner_api_token,
                                    script_wrong_param):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=script_wrong_param).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_add_script_wrong_script(pretty_print, mist_core, owner_api_token,
                                 script_wrong_script, base_exec_inline_script):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=base_exec_inline_script,
                                    script=script_wrong_script).post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_add_script_wrong_entrypoint(pretty_print, cache, mist_core,
                                     owner_api_token, base_exec_inline_script):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data=base_exec_inline_script,
                                    entrypoint='/home/yada/yada').post()
    assert_response_bad_request(response)
    print "Success!!!"


def test_add_ansible_wrong_yaml_format(pretty_print, cache, mist_core,
                                       owner_api_token):
    response = mist_core.add_script(api_token=owner_api_token,
                                    script_data={'name':'test',
                                    'location_type':'inline',
                                    'exec_type':'ansible'},
                                    script=ansible_script_with_error,
                                    entrypoint='').post()
    assert_response_server_error(response)
    print "Success!!!"


def test_show_script_wrong_id(pretty_print, mist_core,
                              owner_api_token):
    response = mist_core.show_script(owner_api_token,
                                     script_id='dummy1234').get()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_script_wrong_api_token(pretty_print, mist_core,
                                       owner_api_token):
    response = mist_core.delete_script(api_token='00' + owner_api_token[:-2],
                                       script_id='bla').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_script_wrong_script_id(pretty_print, cache, mist_core,
                                       owner_api_token):
    response = mist_core.delete_script(api_token=owner_api_token,
                                       script_id='bla').delete()
    assert_response_not_found(response)
    print "Success!!!"


# def test_download_script_wrong_api_token(pretty_print, mist_core,
#                                                 owner_api_token):
#     response = mist_core.download_script(api_token='00' + owner_api_token[:-2],
#                                          script_id='bla').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"


def test_download_script_wrong_script_id(pretty_print, cache, mist_core,
                                         owner_api_token):
    response = mist_core.download_script(api_token=owner_api_token,
                                         script_id='bla').get()
    assert_response_not_found(response)
    print "Success!!!"


# def test_url_script_wrong_api_token(pretty_print, mist_core,
#                                     owner_api_token):
#     response = mist_core.url_script(api_token='00' + owner_api_token[:-2],
#                                     script_id='bla').get()
#     assert_response_unauthorized(response)
#     print "Success!!!"


def test_url_script_wrong_script_id(pretty_print, cache, mist_core,
                                    owner_api_token):
    response = mist_core.url_script(api_token=owner_api_token,
                                    script_id='bla').get()
    assert_response_not_found(response)
    print "Success!!!"


def test_delete_multiple_scripts_wrong_api_token(pretty_print, cache,
                                                 mist_core, owner_api_token):
    response = mist_core.delete_scripts(api_token='00' + owner_api_token[:-2],
                                        script_ids=[]).delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_multiple_scripts_no_script_ids(pretty_print, cache,
                                               mist_core, owner_api_token):
    response = mist_core.delete_scripts(api_token=owner_api_token,
                                        script_ids=[]).delete()
    assert_response_bad_request(response)
    print "Success!!!"


def test_delete_multiple_wrong_script_ids(pretty_print, cache,
                                          mist_core, owner_api_token):
    response = mist_core.delete_scripts(api_token=owner_api_token,
                                        script_ids=['bla', 'bla2']).delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_edit_script_wrong_id(pretty_print, cache,
                              mist_core, owner_api_token):
    response = mist_core.edit_script(api_token=owner_api_token,
                                     script_id='bad', new_name='dummy').put()
    assert_response_not_found(response)
    print "Success!!!"


def test_edit_script_wrong_api_token(pretty_print, cache,
                                     mist_core, owner_api_token):
    response = mist_core.edit_script(api_token='00' + owner_api_token[:-2],
                                     script_id='bad', new_name='dummy').put()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_edit_script_no_new_name(pretty_print, cache,
                                 mist_core, owner_api_token):
    response = mist_core.edit_script(api_token=owner_api_token,
                                     script_id='bla', new_name='').put()
    assert_response_not_found(response)
    print "Success!!!"


# #############################################################################
# # Scenarios
# #############################################################################
#
#
# @pytest.mark.incremental
# class TestSimpleUserScript:
#     def test_add_bash_script(self, pretty_print, cache, mist_core,
#                              owner_api_token):
#         script_id, script_name = add_bash_script(mist_core, owner_api_token)
#         cache.set('script_tests/bash_script_name', script_name)
#         cache.set('script_tests/bash_script_id', script_id)
#         print "Success!!!"
#
#     def test_add_duplicate_bash_script(self, pretty_print, cache, mist_core,
#                                        owner_api_token):
#         response = mist_core.add_script(api_token=owner_api_token,
#                                         name=cache.get(
#                                             'script_tests/bash_script_name',
#                                             ''),
#                                         location_type='inline',
#                                         exec_type='executable',
#                                         script=bash_script).post()
#         assert_response_conflict(response)
#         print "Success!!!"
#
#     def test_show_script(self, pretty_print, cache, mist_core, owner_api_token):
#         response = mist_core.show_script(owner_api_token,
#                                          cache.get(
#                                              'script_tests/bash_script_id',
#                                              '')).get()
#         assert_response_ok(response)
#         script = json.loads(response.content)
#         assert_equal(script['script'], bash_script, script['script'])
#         print "Success!!!"
#
#     def test_add_ansible_script(self, pretty_print, cache, mist_core,
#                                      owner_api_token):
#         response = mist_core.list_scripts(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         ansible_script_name = get_random_script_name(
#             json.loads(response.content))
#         response = mist_core.add_script(api_token=owner_api_token,
#                                         name=ansible_script_name,
#                                         location_type='inline',
#                                         exec_type='ansible',
#                                         script=ansible_script,
#                                         entrypoint='bla').post()
#         assert_response_ok(response)
#         cache.set('script_tests/ansible_script_name', ansible_script_name)
#         response = mist_core.list_scripts(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         script = get_scripts_with_name(
#             cache.get('script_tests/ansible_script_name', ''),
#             json.loads(response.content))
#         assert_list_not_empty(script, "Script was added but is not visible in "
#                                       "the list of scripts")
#         script = script[0]
#         cache.set('script_tests/ansible_script_id', script['id'])
#         print "Success!!!"
#
#     def test_rename_script(self, pretty_print, cache, mist_core,
#                            owner_api_token):
#         response = mist_core.list_scripts(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         new_script_name = get_random_script_name(json.loads(response.content))
#         response = mist_core.edit_script(api_token=owner_api_token,
#                                          script_id=cache.get(
#                                              'script_tests/bash_script_id', ''),
#                                          new_name=new_script_name).put()
#         assert_response_ok(response)
#         assert_equal(json.loads(response.content)['new_name'], new_script_name)
#         response = mist_core.list_scripts(api_token=owner_api_token).get()
#         assert_response_ok(response)
#         script = get_scripts_with_name(
#             cache.get('script_tests/bash_script_name', ''),
#             json.loads(response.content))
#         assert len(script) == 0, \
#             "Script with old name is still listed in the scripts"
#         script = get_scripts_with_name(
#             new_script_name,
#             json.loads(response.content))
#         assert_list_not_empty(script, "Script was renamed but is not visible "
#                                       "in the list of scripts")
#         cache.set('script_tests/bash_script_name', new_script_name)
#         print "Success!!!"
#
#     def test_delete_script(self, pretty_print, cache, mist_core,
#                            owner_api_token):
#         print "Deleting script with id: %s" % cache.get(
#             'script_tests/bash_script_id',
#             '')
#         response = mist_core.delete_script(api_token=owner_api_token,
#                                            script_id=cache.get(
#                                                'script_tests/bash_script_id',
#                                                '')).delete()
#         assert_response_ok(response)
#         print "Success!!!"

#    def test_delete_multiple_scripts(self, pretty_print, cache,
#                                     mist_core,
#                                     owner_api_token):
#        script_ids = [cache.get('script_tests/bash_script_id', ''),
#                      cache.get('script_tests/bash_script_id', '')]
#        # add 3 more scripts and then delete them along with the scripts
#        # created previously
#        for i in range(3):
#            response = mist_core.list_scripts(api_token=owner_api_token).get()
#            assert_response_ok(response)
#            new_script_name = get_random_script_name(
#                json.loads(response.content))
#            response = mist_core.add_script(api_token=owner_api_token,
#                                            name=new_script_name,
#                                            location_type='inline',
#                                            exec_type='executable',
#                                            script=bash_script).post()
#            assert_response_ok(response)
#            response = mist_core.list_scripts(api_token=owner_api_token).get()
#            assert_response_ok(response)
#            script = get_scripts_with_name(new_script_name,
#                                           json.loads(response.content))
#            assert_list_not_empty(script, "Script was added but is not visible"
#                                          " in the list of scripts")
#            script_ids.append(script[0]['id'])
#
#        script_ids.append('bla')
#        script_ids.append('bla2')
#
#        script_ids.append(cache.get('script_tests/ansible_script_id', ''))
#        script_ids.append(cache.get('script_tests/ansible_script_id', ''))
#
#        print "Deleting scripts with id %s" % script_ids
#
#        response = mist_core.delete_scripts(api_token=owner_api_token,
#                                            script_ids=script_ids).delete()
#        assert_response_ok(response)
#        report = json.loads(response.content)
#        for script_id in script_ids:
#            if 'bla' not in script_id:
#                assert_equal(report.get(script_id, ''), 'deleted', report)
#            if 'bla' in script_id:
#                assert_equal(report.get(script_id, ''), 'not_found', report)
#
#        print "Success!!!"
