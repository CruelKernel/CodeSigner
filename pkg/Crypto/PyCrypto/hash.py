# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/Crypto/PyCrypto/hash.py
"""Hash function modules

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import binascii, hashlib, hmac, logging
__VERSION__ = '1'
__AUTHOR__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class Hash:
    __doc__ = 'Hash class\n\n    This class uses hashlib module of python std. lib. for Hash algorithm.\n    '

    def __init__(self):
        """Constructor"""
        self._hash = None

    def digest(self):
        """Return hash digest

        :return: (str) byte string formed Hash digest
        """
        if self._hash is None:
            return
        else:
            return self._hash.digest()

    def hexdigest(self):
        """Return hash digest as hex string formed

        :return: (str) hex string formed Hash digest
        """
        if self._hash is None:
            return
        else:
            return self._hash.hexdigest()

    def sha1(self, msg):
        """Run SHA1 algorithm

        :param msg: (str) plaintext
        :return: (str) Hash digest
        """
        self._hash = hashlib.sha1(msg)
        return self.digest()

    def sha256(self, msg):
        """Run SHA256 algorithm

        :param msg: (str) plaintext
        :return: (str) Hash digest
        """
        self._hash = hashlib.sha256(msg)
        return self.digest()

    def sha384(self, msg):
        """Run SHA384 algorithm

        :param msg: (str) plaintext
        :return: (str) Hash digest
        """
        self._hash = hashlib.sha384(msg)
        return self.digest()

    def sha512(self, msg):
        """Run SHA512 algorithm

        :param msg: (str) plaintext
        :return: (str) Hash digest
        """
        self._hash = hashlib.sha512(msg)
        return self.digest()


class HMAC:
    __doc__ = 'HMAC class\n\n    This class uses hmac and hashlib modules of python std. lib.\n    for HMAC algorithm.\n    '

    def __init__(self):
        """Constructor"""
        _logger.debug('Run constructor of HMAC class, %s' % self)

    def keygen(self, key, bit):
        """This is not implemented."""
        pass

    def _run(self, msg=None, key=None, key_id=None, _hash=None):
        return hmac.new(binascii.unhexlify(key), binascii.unhexlify(msg), _hash).hexdigest()

    def sha256(self, msg=None, key=None, key_id=None):
        """Run HMAC algorithm using SHA256 hash algorithm.

        :param msg: (str) plaintext
        :param key: (str) Key for HMAC
        :param key_id: None (Not used)
        :return: (binary array) Result of HMAC
        """
        _logger.debug('Run HMAC-SHA256')
        _logger.debug('[HMAC-SHA256] msg: %s' % msg)
        _logger.debug('[HMAC-SHA256] key: %s' % key)
        _logger.debug('[HMAC-SHA256] key_id: %s' % key_id)
        rv = self._run(msg, key, key_id, hashlib.sha256)
        _logger.debug('[HMAC-SHA256] Return, %s' % rv)
        return rv

    def sha512(self, msg=None, key=None, key_id=None):
        """Run HMAC algorithm using SHA256 hash algorithm.

        :param msg: (str) plaintext
        :param key: (str) Key for HMAC
        :param key_id: None (Not used)
        :return: (binary array) Result of HMAC
        """
        _logger.debug('Run HMAC-SHA512')
        _logger.debug('[HMAC-SHA512] msg: %s' % msg)
        _logger.debug('[HMAC-SHA512] key: %s' % key)
        _logger.debug('[HMAC-SHA512] key_id: %s' % key_id)
        rv = self._run(msg, key, key_id, hashlib.sha512)
        _logger.debug('[HMAC-SHA512] Return, %s' % rv)
        return rv