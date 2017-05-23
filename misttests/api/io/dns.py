from misttests.api.helpers import *
from misttests.helpers.vault import safe_get_var
from misttests import config

import pytest

############################################################################
#                          Unit Testing Zones                              #
############################################################################


def test_list_zones(pretty_print, mist_core, cache,  owner_api_token):
    response = mist_core.add_cloud('EC2', 'ec2', api_token=owner_api_token,
                                   api_key=safe_get_var('clouds/aws', 'api_key', config.CREDENTIALS['EC2']['api_key']),
                                   api_secret=safe_get_var('clouds/aws', 'api_secret', config.CREDENTIALS['EC2']['api_secret']),
                                   region='ap-northeast-1').post()
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
    domain = 'dummytestzone%d.com' % random.randint(1,200)
    response = mist_core.create_zone(api_token=owner_api_token, cloud_id=cache.get('cloud_id', ''),
                                     domain='dummytestzone.com', type='master', ttl=3600).post()
    assert_response_ok(response)
    cache.set('zone_id', response.json()['id'])
    cache.set('domain', response.json()['domain'])
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
    domain = cache.get('domain', '')
    name = 'blog.' + domain
    response = mist_core.create_record(api_token='', cloud_id=cache.get('cloud_id', ''),
                                       zone_id=cache.get('zone_id', ''),
                                       name=name, type='A',
                                       data="1.2.3.4", ttl=3600).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_create_record_wrong_api_token(pretty_print, cache, mist_core):
    domain = cache.get('domain', '')
    name = 'blog.' + domain
    response = mist_core.create_record(api_token='dummy', cloud_id=cache.get('cloud_id', ''),
                                       zone_id=cache.get('zone_id', ''),
                                       name=name, type='A',
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

@pytest.mark.incremental
class TestSchedulesFunctionality:

    def test_list_zones_contains_created_zone(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_zones(api_token=owner_api_token,
                                        cloud_id=cache.get('cloud_id', '')
                                       ).get()
        assert_response_ok(response)
        assert len(response.json()['zones']) >= 1
        zone_id = cache.get('zone_id', '')
        zone_found = False
        for zone in response.json()['zones']:
            if zone['id'] == zone_id:
                zone_found = True
                break
        assert zone_found
        print "Success!!!"

    def test_create_records(self, pretty_print, mist_core, owner_api_token, cache):
        domain = cache.get('domain', '')
        nameA = 'subdomain.' + domain
        response = mist_core.create_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           name=nameA,
                                           type='A',
                                           data='172.16.254.1',
                                           ttl=3600
                                          ).post()
        assert_response_ok(response)
        cache.set('Arecord_id', response.json()['id'])

        nameAAAA = 'subdomain2.' + domain
        response = mist_core.create_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           name=nameAAAA,
                                           type='AAAA',
                                           data='2001:db8:0:1234:0:567:8:1',
                                           ttl=3600
                                          ).post()
        assert_response_ok(response)
        cache.set('AAAArecord_id', response.json()['id'])

        nameCNAME = 'subdomain3.' + domain
        response = mist_core.create_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           name=nameCNAME,
                                           type='CNAME',
                                           data='host.example.com',
                                           ttl=3600
                                          ).post()
        assert_response_ok(response)
        cache.set('CNAMErecord_id', response.json()['id'])

        nameMX = 'mailserver.' + domain
        response = mist_core.create_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           name=nameMX,
                                           type='MX',
                                           data='10 mailserver.mist.com.',
                                           ttl=3600
                                          ).post()
        assert_response_ok(response)
        cache.set('MXrecord_id', response.json()['id'])

        nameTXT = 'text.' + domain
        response = mist_core.create_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           name=nameTXT,
                                           type='TXT',
                                           data='Just some text',
                                           ttl=3600
                                          ).post()
        assert_response_ok(response)
        cache.set('TXTrecord_id', response.json()['id'])
        print "Success!!!"

    def test_record_listing(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.list_records(cloud_id=cache.get('cloud_id', ''),
                                          zone_id=cache.get('zone_id', ''),
                                          api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 7
        for record in response.json():
            if record['type'] == 'A':
                assert record['name'] == 'subdomain'
                assert record['rdata'] == ['172.16.254.1']
            elif record['type'] == 'AAAA':
                assert record['name'] == 'subdomain2'
                assert record['rdata'] == ['2001:db8:0:1234:0:567:8:1']
            elif record['type'] == 'CNAME':
                assert record['name'] == 'subdomain3'
                assert record['rdata'] == ['host.example.com.']
            elif record['type'] == 'TXT':
                assert record['name'] == 'text'
                assert record['rdata'] == ['"Just some text"']
        print "Success!!!"

    def test_delete_records(self, pretty_print, mist_core, owner_api_token, cache):
        response = mist_core.delete_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           record_id=cache.get('Arecord_id', '')
                                          ).delete()
        assert_response_ok(response)
        response = mist_core.delete_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           record_id=cache.get('AAAArecord_id', '')
                                          ).delete()
        assert_response_ok(response)
        response = mist_core.delete_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           record_id=cache.get('CNAMErecord_id', '')
                                          ).delete()
        assert_response_ok(response)
        response = mist_core.delete_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           record_id=cache.get('MXrecord_id', '')
                                          ).delete()
        assert_response_ok(response)
        response = mist_core.delete_record(api_token=owner_api_token,
                                           cloud_id=cache.get('cloud_id', ''),
                                           zone_id=cache.get('zone_id', ''),
                                           record_id=cache.get('TXTrecord_id', '')
                                          ).delete()
        assert_response_ok(response)
        # Paranoid check, make sure we only have 2 records in the provider
        # the NS and SOA required onces
        response = mist_core.list_records(cloud_id=cache.get('cloud_id', ''),
                                          zone_id=cache.get('zone_id', ''),
                                          api_token=owner_api_token).get()
        assert_response_ok(response)
        assert len(response.json()) == 2
        print "Success!!!"

    def test_delete_zone(self, pretty_print, mist_core, owner_api_token, cache):
        #Let's delete the zone
        response = mist_core.delete_zone(api_token=owner_api_token,
                                         cloud_id=cache.get('cloud_id', ''),
                                         zone_id=cache.get('zone_id', '')
                                        ).delete()
        assert_response_ok(response)
        #And make sure that the zone has been deleted:
        response = mist_core.list_zones(api_token=owner_api_token,
                                        cloud_id=cache.get('cloud_id', '')).get()
        assert_response_ok(response)
        assert len(response.json()['zones']) >= 1
        zone_id = cache.get('zone_id', '')
        zone_not_found = True
        for zone in response.json()['zones']:
            if zone['id'] == zone_id:
                zone_not_found = False
        assert zone_not_found

        print "Success!!!"

    