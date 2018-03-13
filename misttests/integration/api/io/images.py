from misttests.integration.api.helpers import *
from misttests.config import safe_get_var
from misttests import config


# needs to change in the backend: get instead of post...
def test_list_images(pretty_print, mist_core, owner_api_token, cache):
    if config.LOCAL:
        response = mist_core.add_cloud(name, provider='docker', api_token=owner_api_token,
                                   docker_host=config.LOCAL_DOCKER,
                                   docker_port='2375').post()
    else:
        response = mist_core.add_cloud(name, provider='docker', api_token=owner_api_token,
                                   docker_host=safe_get_var('dockerhosts/godzilla', 'host',
                                                            config.CREDENTIALS['DOCKER']['host']),
                                   docker_port=int(safe_get_var('dockerhosts/godzilla', 'port',
                                                            config.CREDENTIALS['DOCKER']['port'])),
                                   authentication=safe_get_var('dockerhosts/godzilla', 'authentication',
                                                               config.CREDENTIALS['DOCKER']['authentication']),
                                   ca_cert_file=safe_get_var('dockerhosts/godzilla', 'ca',
                                                             config.CREDENTIALS['DOCKER']['ca']),
                                   key_file=safe_get_var('dockerhosts/godzilla', 'key',
                                                         config.CREDENTIALS['DOCKER']['key']),
                                   cert_file=safe_get_var('dockerhosts/godzilla', 'cert',
                                                          config.CREDENTIALS['DOCKER']['cert']), show_all=True).post()
    assert_response_ok(response)
    response = mist_core.list_clouds(api_token=owner_api_token).get()
    assert_response_ok(response)
    assert len(response.json()) == 1
    cache.set('cloud_id', response.json()[0]['id'])
    response = mist_core.list_images(cloud_id=cache.get('cloud_id',''), api_token=owner_api_token).post()
    assert_response_ok(response)
    cache.set('image_id', response.json()[0]['id'])
    assert len(response.json()) > 0, "No images are listed for Linode cloud"
    print "Success!!!"


def test_list_images_wrong_api_token(pretty_print, mist_core, cache, owner_api_token):
    response = mist_core.list_images(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token + 'dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_list_images_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.list_images(cloud_id=cache.get('cloud_id', '')).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_list_images_wrong_cloud_id(pretty_print, mist_core, owner_api_token):
    response = mist_core.list_images(cloud_id='dummy', api_token=owner_api_token).post()
    assert_response_not_found(response)
    print "Success!!!"


def test_star_image_no_api_token(pretty_print, cache, mist_core):
    response = mist_core.star_image(cloud_id=cache.get('cloud_id', ''),
                                    image_id=cache.get('image_id', '')).post()
    assert_response_forbidden(response)
    print "Success!!!"


def test_star_image_wrong_api_token(pretty_print, mist_core, cache, owner_api_token):
    response = mist_core.star_image(cloud_id=cache.get('cloud_id', ''), image_id=cache.get('image_id', ''),
                                    api_token=owner_api_token + 'dummy').post()
    assert_response_unauthorized(response)
    print "Success!!!"


def test_star_image_ok(pretty_print, mist_core, cache, owner_api_token):
    response = mist_core.list_images(cloud_id=cache.get('cloud_id',''), api_token=owner_api_token).post()
    assert_response_ok(response)
    assert response.json()[0]['star'], "Image is not starred by default"
    response = mist_core.star_image(cloud_id=cache.get('cloud_id', ''), image_id=cache.get('image_id', ''),
                                    api_token=owner_api_token).post()
    assert_response_ok(response)
    response = mist_core.list_images(cloud_id=cache.get('cloud_id',''), api_token=owner_api_token).post()
    assert_response_ok(response)
    for image in response.json():
        if image['id'] == cache.get('image_id', ''):
            assert not image['star'], "Image was not unstarred!"
            break
    response = mist_core.star_image(cloud_id=cache.get('cloud_id', ''), image_id=cache.get('image_id', ''),
                                    api_token=owner_api_token).post()
    assert_response_ok(response)
    response = mist_core.list_images(cloud_id=cache.get('cloud_id', ''), api_token=owner_api_token).post()
    assert_response_ok(response)
    for image in response.json():
        if image['id'] == cache.get('image_id', ''):
            assert image['star'], "Image was not starred!"
            break
    print "Success!!!"
