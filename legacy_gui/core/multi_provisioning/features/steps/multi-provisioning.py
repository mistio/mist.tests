import os
import json
import random

from behave import *
from tests.legacy_gui.steps.utils import safe_get_element_text

providers_to_check = ["Azure",
                      "DigitalOcean",
                      "Linode",
                      "NephoScale",
                      "SoftLayer",
                      "EC2",
                      "GCE",
                      "Rackspace"]


provider_data = {
    "Azure": {
        "credentials": "AZURE",
        "size": "ExtraSmall",
        "name_prefix": "tmAzure",
        "location_button_text": "Select Location",
        "location": "West Europe"
    },
    "DigitalOcean": {
        "credentials": "DIGITALOCEAN",
        "size": "512mb",
        "name_prefix": "tmDigital",
        "location_button_text": "Select Location",
        "location": "New York 1"
    },
    "Linode": {
        "credentials": "LINODE",
        "size": "Linode 1024",
        "name_prefix": "tmLinode",
        "location_button_text": "Select Location",
        "location": "Dallas"
    },
    "NephoScale": {
        "credentials": "NEPHOSCALE",
        "size": "CS05",
        "name_prefix": "tmNephoscale",
        "location_button_text": "Select Location",
        "location": "SJC-1"
    },
    "SoftLayer": {
        "credentials": "SOFTLAYER",
        "size": "ram:1024",
        "name_prefix": "tmSoftLayer",
        "location_button_text": "Select Location",
        "location": "Amsterdam"
    },
    "EC2": {
        "credentials": "EC2",
        "size": "Micro Instance",
        "name_prefix": "tmEC2",
        "location_button_text": "Select Location",
        "location": "ap-northeast-1a"
    },
    "GCE": {
        "credentials": "GCE",
        "size": "f1-micro",
        "name_prefix": "tmGCE",
        "location_button_text": "Select Location",
        "location": "europe-west1-b"
    },
    "Rackspace": {
        "credentials": "RACKSPACE",
        "size": "512MB",
        "name_prefix": "tmRackspace",
        "location_button_text": "Default",
        "location": "Default"
    }
}

# provider    | credentials | size          | button_location| location
# Azure       | AZURE       | ExtraSmall    | Select Location| West Europe
# DigitalOcean| DIGITALOCEAN| 512mb         | Select Location| New York 1
# Linode      | LINODE      | Linode 1024   | Select Location| Dallas
# NephoScale  | NEPHOSCALE  | CS05          | Select Location| SJC-1
# SoftLayer   | SOFTLAYER   | ram:1024      | Select Location| Amsterdam
# EC2         | EC2         | Micro Instance| Select Location| ap-northeast-1a
# GCE         | GCE         | f1-micro      | Select Location| europe-west1-b
# Rackspace   | RACKSPACE   | 512MB         | Default        | Default


@when(u"I decide which provider and image I'm going to test")
def make_a_decision_on_provider_and_image(context, json_object=None):
    if not json_object:
        if not os.path.isfile(context.mist_config['MP_DB_DIR']):
            json_object = {}
        else:
            fp = open(context.mist_config['MP_DB_DIR'])
            json_object = json.load(fp)
            fp.close()

    images = context.browser.find_elements_by_class_name('staron')
    images = sorted(images, key=lambda image: image.find_element_by_tag_name('h3').text)
    images = sorted(images, key=lambda image: image.find_element_by_class_name('tag').text)

    for provider in providers_to_check:
        if not json_object.get(provider):
            json_object[provider] = {'images_left': True,
                                     'images_already_checked': []}

    done = False
    while not done:
        providers_left_to_check = filter(lambda x: json_object[x]['images_left'], providers_to_check)
        # assert len(providers_left_to_check) > 0, "No providers left to check"
        next_provider_to_check = min(providers_left_to_check, key=lambda x: len(json_object.get(x).get('images_already_checked')))
        images_already_checked = json_object[provider]['images_already_checked']
        images_available = filter(
            lambda image: safe_get_element_text(image.find_element_by_class_name('tag')).lower() == next_provider_to_check.lower(), images)
        images_available = map(
            lambda image: safe_get_element_text(image.find_element_by_tag_name('h3')).lower(), images_available)
        images_left_to_check = [image for image in images_available if
                                image not in images_already_checked]
        while len(images_left_to_check) > 0:
            image = images_left_to_check.pop()
            if 'coreos' in image.lower() or 'true' in image.lower() or 'eee' in image.lower():
                json_object[provider]['images_already_checked'].append(image)
            else:
                json_object['next_image_to_check'] = image
                json_object['next_provider_to_check'] = next_provider_to_check
                context.mist_config['MP_MACHINE_TO_TEST'] = image
                context.mist_config['MP_PROVIDER_TO_TEST'] = next_provider_to_check
                context.mist_config['MP_NEW_MACHINE_NAME'] = provider_data[next_provider_to_check]["name_prefix"] + "TestMachine" + str(random.randint(1, 10000))
                context.mist_config['MP_MACHINE_LOCATION'] = provider_data[next_provider_to_check]["location"]
                context.mist_config['MP_MACHINE_LOCATION_BUTTON'] = provider_data[next_provider_to_check]["location_button_text"]
                context.mist_config['MP_MACHINE_SIZE'] = provider_data[next_provider_to_check]["size"]
                done = True
                break
        if len(images_left_to_check) == 0:
            json_object[provider]['images_left'] = False

    fp = open(context.mist_config['MP_DB_DIR'], 'w')
    json.dump(json_object, fp)
    fp.close()


@then(u'I add the machine to the db as successfuly tested')
def mark_test_as_success(context):
    fp = open(context.mist_config['MP_DB_DIR'])
    json_object = json.load(fp)
    fp.close()

    image_name = context.mist_config['MP_MACHINE_TO_TEST']
    provider = context.mist_config['MP_PROVIDER_TO_TEST']
    json_object[provider]['images_already_checked'].append(image_name)
    json_object['next_provider_to_check'] = ""
    json_object['next_image_to_check'] = ""

    fp = open(context.mist_config['MP_DB_DIR'], 'w')
    json.dump(json_object, fp)
    fp.close()
