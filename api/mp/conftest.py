import os
import json
import pytest
import shutil

from datetime import datetime

from tests import config

from tests.api.core.core import MistCoreApi


@pytest.fixture
def mist_core():
    return MistCoreApi('https://mist.io')


@pytest.fixture
def api_token():
    return config.MIST_API_TOKEN


@pytest.fixture
def mp_json(request):
    # mp_json is a file used by the tests that for each provider has a dict
    # where each id is an image that has been tested and the value is another
    # dict with the human readable name of the image and the outcome of the
    # machine creation.
    db_path = config.MP_DB_DIR
    if not os.path.isfile(db_path):
        json_object = {}
    else:
        fp = open(db_path, 'r')
        json_object = json.load(fp)
        fp.close()

    def close_object_on_exit():
        if 'updated' in json_object:
            del json_object['updated']
            fp = open(db_path, 'w')
            json.dump(json_object, fp)
            fp.close()
        else:
            shutil.move(db_path,
                        db_path + '.' + datetime.utcnow().strftime('%Y-%m-%d'))

    request.addfinalizer(close_object_on_exit)

    return json_object
