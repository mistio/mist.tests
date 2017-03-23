from openid.association import Association
from openid.cryptutil import randomString
from openid.store.nonce import mkNonce as mk_nonce
from openid.store.nonce import split

import string
import time

allowed_handle = []
for c in string.printable:
    if c not in string.whitespace:
        allowed_handle.append(c)
allowed_handle = ''.join(allowed_handle)


def generate_handle(n):
    return randomString(n, allowed_handle)

generateSecret = randomString


def test_store(store):
    """Make sure a given store has a minimum of API compliance. Call
    this function with an empty store.

    Raises AssertionError if the store does not work as expected.

    OpenIDStore -> NoneType
    """
    # Association functions
    now = int(time.time())

    server_url = 'http://www.myopenid.com/openid'

    def gen_assoc(issued, lifetime=600):
        sec = generateSecret(20)
        hdl = generate_handle(128)
        return Association(hdl, sec, now + issued, lifetime, 'HMAC-SHA1')

    def check_retrieve(url, handle=None, expected=None):
        retrieved_assoc = store.getAssociation(url, handle)
        assert retrieved_assoc == expected, (retrieved_assoc, expected)
        if expected is not None:
            if retrieved_assoc is expected:
                print ('Unexpected: retrieved a reference to the expected '
                       'value instead of a new object')
            assert retrieved_assoc.handle == expected.handle
            assert retrieved_assoc.secret == expected.secret

    def check_remove(url, handle, expected):
        present = store.removeAssociation(url, handle)
        assert bool(expected) == bool(present)

    assoc = gen_assoc(issued=0)

    # Make sure that a missing association returns no result
    check_retrieve(server_url)

    # Check that after storage, getting returns the same result
    store.storeAssociation(server_url, assoc)
    check_retrieve(server_url, None, assoc)

    # more than once
    check_retrieve(server_url, None, assoc)

    # Storing more than once has no ill effect
    store.storeAssociation(server_url, assoc)
    check_retrieve(server_url, None, assoc)

    # Removing an association that does not exist returns not present
    check_remove(server_url, assoc.handle + 'x', False)

    # Removing an association that does not exist returns not present
    check_remove(server_url + 'x', assoc.handle, False)

    # Removing an association that is present returns present
    check_remove(server_url, assoc.handle, True)

    # but not present on subsequent calls
    check_remove(server_url, assoc.handle, False)

    # Put assoc back in the store
    store.storeAssociation(server_url, assoc)

    # More recent and expires after assoc
    assoc2 = gen_assoc(issued=1)
    store.storeAssociation(server_url, assoc2)

    # After storing an association with a different handle, but the
    # same server_url, the handle with the later issue date is returned.
    check_retrieve(server_url, None, assoc2)

    # We can still retrieve the older association
    check_retrieve(server_url, assoc.handle, assoc)

    # Plus we can retrieve the association with the later issue date
    # explicitly
    check_retrieve(server_url, assoc2.handle, assoc2)

    # More recent, and expires earlier than assoc2 or assoc. Make sure
    # that we're picking the one with the latest issued date and not
    # taking into account the expiration.
    assoc3 = gen_assoc(issued=2, lifetime=100)
    store.storeAssociation(server_url, assoc3)

    check_retrieve(server_url, None, assoc3)
    check_retrieve(server_url, assoc.handle, assoc)
    check_retrieve(server_url, assoc2.handle, assoc2)
    check_retrieve(server_url, assoc3.handle, assoc3)

    check_remove(server_url, assoc2.handle, True)

    check_retrieve(server_url, None, assoc3)
    check_retrieve(server_url, assoc.handle, assoc)
    check_retrieve(server_url, assoc2.handle, None)
    check_retrieve(server_url, assoc3.handle, assoc3)

    check_remove(server_url, assoc2.handle, False)
    check_remove(server_url, assoc3.handle, True)

    check_retrieve(server_url, None, assoc)
    check_retrieve(server_url, assoc.handle, assoc)
    check_retrieve(server_url, assoc2.handle, None)
    check_retrieve(server_url, assoc3.handle, None)

    check_remove(server_url, assoc2.handle, False)
    check_remove(server_url, assoc.handle, True)
    check_remove(server_url, assoc3.handle, False)

    check_retrieve(server_url, None, None)
    check_retrieve(server_url, assoc.handle, None)
    check_retrieve(server_url, assoc2.handle, None)
    check_retrieve(server_url, assoc3.handle, None)

    check_remove(server_url, assoc2.handle, False)
    check_remove(server_url, assoc.handle, False)
    check_remove(server_url, assoc3.handle, False)

    # test expired associations
    # assoc 1: server 1, valid
    # assoc 2: server 1, expired
    # assoc 3: server 2, expired
    # assoc 4: server 3, valid
    assoc_valid1 = gen_assoc(issued=-3600, lifetime=7200)
    assoc_valid2 = gen_assoc(issued=-5)
    assoc_expired1 = gen_assoc(issued=-7200, lifetime=3600)
    assoc_expired2 = gen_assoc(issued=-7200, lifetime=3600)

    store.cleanupAssociations()
    store.storeAssociation(server_url + '1', assoc_valid1)
    store.storeAssociation(server_url + '1', assoc_expired1)
    store.storeAssociation(server_url + '2', assoc_expired2)
    store.storeAssociation(server_url + '3', assoc_valid2)

    cleaned = store.cleanupAssociations()
    assert cleaned == 2, cleaned

    # Nonce functions

    def check_use_nonce(nonce, expected, server_url, msg=''):
        stamp, salt = split(nonce)
        actual = store.useNonce(server_url, stamp, salt)
        assert bool(actual) == bool(expected), "%r != %r: %s" % (actual,
                                                                 expected,
                                                                 msg)

    for url in [server_url, '']:
        # Random nonce (not in store)
        nonce1 = mk_nonce()

        # A nonce is allowed by default
        check_use_nonce(nonce1, True, url)

        # Storing once causes useNonce to return True the first, and only
        # the first, time it is called after the store.
        check_use_nonce(nonce1, False, url)
        check_use_nonce(nonce1, False, url)

        # Nonces from when the universe was an hour old should not pass
        # these days.
        old_nonce = mk_nonce(3600)
        check_use_nonce(old_nonce, False, url, "Old nonce (%r) passed." %
                        (old_nonce,))

    old_nonce1 = mk_nonce(now - 20000)
    old_nonce2 = mk_nonce(now - 10000)
    recent_nonce = mk_nonce(now - 600)

    from openid.store import nonce as nonceModule
    orig_skew = nonceModule.SKEW
    try:
        nonceModule.SKEW = 0
        store.cleanupNonces()
        # Set SKEW high so stores will keep our nonces.
        nonceModule.SKEW = 100000
        assert store.useNonce(server_url, *split(old_nonce1))
        assert store.useNonce(server_url, *split(old_nonce2))
        assert store.useNonce(server_url, *split(recent_nonce))

        nonceModule.SKEW = 3600
        cleaned = store.cleanupNonces()
        assert cleaned == 2, "Cleaned %r nonces." % (cleaned,)

        nonceModule.SKEW = 100000
        # A roundabout method of checking that the old nonces were cleaned is
        # to see if we're allowed to add them again.
        assert store.useNonce(server_url, *split(old_nonce1))
        assert store.useNonce(server_url, *split(old_nonce2))
        # The recent nonce wasn't cleaned, so it should still fail.
        assert not store.useNonce(server_url, *split(recent_nonce))
    finally:
        nonceModule.SKEW = orig_skew


def test_filestore():
    from openid.store import filestore
    import tempfile
    import shutil
    try:
        temp_dir = tempfile.mkdtemp()
    except AttributeError:
        import os
        temp_dir = os.tmpnam()
        os.mkdir(temp_dir)

    store = filestore.FileOpenIDStore(temp_dir)
    try:
        test_store(store)
        store.cleanup()
    except:
        raise
    else:
        shutil.rmtree(temp_dir)


def test_memstore():
    from openid.store import memstore
    test_store(memstore.MemoryStore())
