from misttests.api.helpers import *
from misttests import config
from time import sleep

import pytest
import datetime

############################################################################
#                          Unit Testing Zones                              #
############################################################################


def test_list_zones(pretty_print, mist_core, cache,  owner_api_token):
    response = mist_core.add_cloud('EC2', 'ec2', api_token=owner_api_token,
                                   api_key=config.CREDENTIALS['AWS']['api_key'],
                                   api_secret=config.CREDENTIALS['AWS']['api_secret'],
                                   region=config.CREDENTIALS['AWS']['region']).post()
    assert_response_ok(response)
    response = mist_core.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 1
    cache.set('cloud_id', response.json()[0]['id'])
    response = mist_core.list_zones(cloud_id=cache.get('cloud_id', ''),
                                    api_token=owner_api_token).get()
    assert_response_ok(response)
    print "Success!!!"


def test_list_zones_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.list_zones(cloud_id=cache.get('cloud_id', ''), api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_zones_wrong_api_token(pretty_print, cache, mist_core):
    response = mist_core.list_zones(cloud_id=cache.get('cloud_id', ''), api_token='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_zone_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.create_zone(api_token='', cloud_id=cache.get('cloud_id', ''),
                                     domain='dummy.com', type='master', ttl=3600).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_zone_wrong_api_token(pretty_print, cache, mist_core):
    response = mist_core.create_zone(api_token='dummy', cloud_id=cache.get('cloud_id', ''),
                                     domain='dummy.com', type='master', ttl=3600).post()
    assert_response_unauthorized(response)
    print "Success!!!"

def test_delete_zone_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.delete_zone(api_token='', cloud_id=cache.get('cloud_id', ''), zone_id='dummy').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_zone_wrong_api_token(pretty_print, cache, mist_core):
    response = mist_core.delete_zone(api_token='dummy', cloud_id=cache.get('cloud_id', ''), zone_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_zone_wrong_zone_id(pretty_print, mist_core, cache, owner_api_token):
    response = mist_core.delete_zone(api_token=owner_api_token, cloud_id=cache.get('cloud_id', ''), zone_id='dummy').delete()
    assert_response_not_found(response)
    print "Success!!!"


def test_list_records(pretty_print, mist_core, cache,  owner_api_token):
    response = mist_core.create_zone(api_token=owner_api_token, cloud_id=cache.get('cloud_id', ''),
                                     domain='dummytestzone.com', type='master', ttl=3600).post()
    assert_response_ok(response)
    # assert len(response.json()) == 1
    print response.json()
    cache.set('zone_id', response.json()['id'])
    response = mist_core.list_records(cloud_id=cache.get('cloud_id', ''), zone_id=cache.get('zone_id', ''),
                                      api_token=owner_api_token).get()
    assert_response_ok(response)
    print "Success!!!"


def test_list_records_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.list_records(cloud_id=cache.get('cloud_id', ''), 
                                      zone_id=cache.get('zone_id', ''), api_token='').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_records_wrong_api_token(pretty_print, cache, mist_core):
    response = mist_core.list_records(cloud_id=cache.get('cloud_id', ''), 
                                      zone_id=cache.get('zone_id', ''), api_token='dummy').get()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_create_record_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.create_record(api_token='', cloud_id=cache.get('cloud_id', ''),
                                       zone_id=cache.get('zone_id', ''),
                                       name='blog.dummytestzone.com', type='A',
                                       data="1.2.3.4", ttl=3600).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_record_wrong_api_token(pretty_print, cache, mist_core):
    response = mist_core.create_record(api_token='dummy', cloud_id=cache.get('cloud_id', ''),
                                       zone_id=cache.get('zone_id', ''),
                                       name='blog.dummytestzone.com', type='A',
                                       data="1.2.3.4", ttl=3600).post()
    assert_response_unauthorized(response)
    print "Success!!!"

def test_delete_record_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.delete_record(api_token='', cloud_id=cache.get('cloud_id', ''),
                                       zone_id='dummy', record_id='dummy').delete()
    assert_response_forbidden(response)
    print "Success!!!"


def test_delete_record_wrong_api_token(pretty_print, cache, mist_core):
    response = mist_core.delete_record(api_token='dummy', cloud_id=cache.get('cloud_id', ''),
                                       zone_id='dummy', record_id='dummy').delete()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_delete_record_wrong_record_id(pretty_print, mist_core, cache, owner_api_token):
    response = mist_core.delete_record(api_token=owner_api_token, cloud_id=cache.get('cloud_id', ''),
                                       zone_id=cache.get('zone_id', ''), record_id='dummy').delete()
    assert_response_not_found(response)
    print "Success!!!"




############################################################################
#                         Functional Testing                               #
############################################################################

