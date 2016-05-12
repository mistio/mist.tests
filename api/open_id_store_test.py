from mist.core.auth.oidstore import OpenIdMistStore
from mist.core.tests.api import openidstoretest


def test_001_test_native_openid_store(pretty_print):
    print ">>> Testing memstore"
    openidstoretest.test_memstore()
    print ">>> Testing filestorestore"
    openidstoretest.test_filestore()
    print ">>> Testing native store"
    openidstoretest.test_store(OpenIdMistStore())
