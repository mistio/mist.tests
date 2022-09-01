import pytest

from misttests.integration.api.helpers import assert_response_unauthorized
from misttests.integration.api.utils import assert_less_or_equal, assert_response_not_found
from misttests.config import safe_get_var
from misttests.integration.api.helpers import assert_response_ok

DIRS_PATH = 'tmp/test/dirs/'
MIXED_PATH = 'tmp/test/mixed/'

############################################################################
#                             Unit Testing                                 #
############################################################################


def test_list_buckets_no_api_token(mist_api_v1):
    response = mist_api_v1.list_buckets().get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_buckets_wrong_api_token(mist_api_v1):
    response = mist_api_v1.list_buckets(api_token='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_get_bucket_no_api_token(mist_api_v1):
    response = mist_api_v1.get_bucket(bucket_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_get_bucket_wrong_api_token(mist_api_v1):
    response = mist_api_v1.get_bucket(bucket_id='dummy',
                                    api_token='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_get_bucket_wrong_bucket_id(mist_api_v1, owner_api_token):
    response = mist_api_v1.get_bucket(bucket_id='dummy',
                                    api_token=owner_api_token).get()
    assert_response_not_found(response)
    print("Success!!!")


def list_bucket_content_no_api_token(mist_api_v1):
    response = mist_api_v1.list_bucket_content(bucket_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_bucket_content_wrong_api_token(mist_api_v1):
    response = mist_api_v1.list_bucket_content(api_token='dummy',
                                             bucket_id='dummy').get()
    assert_response_unauthorized(response)
    print("Success!!!")


def test_list_bucket_content_wrong_bucket_id(mist_api_v1, owner_api_token):
    response = mist_api_v1.list_bucket_content(api_token=owner_api_token,
                                             bucket_id='dummy').get()
    assert_response_not_found(response)
    print("Success!!!")

############################################################################
#                         Functional Testing                               #
############################################################################


@pytest.mark.incremental
class TestBucketsFunctionality:

    def test_list_buckets(self, pretty_print, mist_api_v1, cache,
                          owner_api_token):

        response = mist_api_v1.add_cloud(
            name='EC2', provider='ec2', api_token=owner_api_token,
            region=safe_get_var('clouds/aws', 'region'),
            apikey=safe_get_var('clouds/aws', 'apikey'),
            apisecret=safe_get_var('clouds/aws', 'apisecret'),
            object_storage_enabled=True
        ).post()
        assert_response_ok(response)
        assert mist_api_v1.poll_buckets(owner_api_token)
        response = mist_api_v1.list_buckets(api_token=owner_api_token).get()
        assert_response_ok(response)
        cache.set(
            'bucket_id', [bucket['id'] for bucket in response.json()
                          if bucket['name'] == 'infdepth'][0])
        print("Success!!!")

    def test_get_bucket(self, pretty_print, mist_api_v1, cache,
                        owner_api_token):
        response = mist_api_v1.list_bucket_content(
            bucket_id=cache.get('bucket_id', ''),
            api_token=owner_api_token
        ).get()

        assert_response_ok(response)
        print("Success!!!")

    def test_list_bucket_content(self, pretty_print, mist_api_v1, cache,
                                 owner_api_token):

        # Test path containing only dirs
        response = mist_api_v1.list_bucket_content(
            bucket_id=cache.get('bucket_id', ''),
            api_token=owner_api_token,
            path=DIRS_PATH
        ).get()
        assert_response_ok(response)

        data = response.json()

        assert_less_or_equal(len(data['content']), 100)

        # Test path containing only files
        response = mist_api_v1.list_bucket_content(
            bucket_id=cache.get('bucket_id', ''),
            api_token=owner_api_token,
            path=DIRS_PATH+'0000_dir/'
        ).get()
        assert_response_ok(response)

        data = response.json()
        assert_less_or_equal(len(data['content']), 100)

        # Test path containing files and directories
        response = mist_api_v1.list_bucket_content(
            bucket_id=cache.get('bucket_id', ''),
            api_token=owner_api_token,
            path=MIXED_PATH
        ).get()
        assert_response_ok(response)

        data = response.json()
        assert_less_or_equal(
            len(data['content']), 100)
