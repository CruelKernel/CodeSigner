# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/File/publickey.py
"""CodeSigner public key file image

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import ctypes, hashlib, logging, sys
from .Structure import interface
from .Structure import publickey
from .Structure import signature
__all__ = ('Factory', )
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class Factory:
    __doc__ = 'Public key file image generator'

    def __init__(self):
        pass

    @staticmethod
    def create(algorithm='ecc'):
        """Public key object generator

        :param algorithm: (str) 'ecc' or 'rsa' (default: 'ecc')
        :return: (obj) Publickey file object
        """
        _classes = {'ecc':ECC, 
         'rsa':RSA}
        return _classes[algorithm.lower()]()


class RSA(interface.Base):
    __doc__ = 'PublicKey for RSA algorithm'
    _fields_ = (
     (
      'publickey', publickey.RSAPublickey),
     (
      'hmac', ctypes.c_ubyte * 32),
     (
      'signature_size', ctypes.c_uint32),
     (
      'signature', signature.Signature))

    def set_key(self, st_key):
        """Set public key

        :param st_key: (obj) RSA public key data object
        :return: N/A
        """
        if isinstance(st_key, publickey.PublicKey):
            self.publickey = st_key.rsa
        else:
            if isinstance(st_key, publickey.RSAPublickey):
                self.publickey = st_key
            else:
                _logger.error('Unknown publickey type')
                sys.exit(-1)

    def get_key(self):
        """Get public key

        :return: (obj) RSA public key data object
        """
        pk = publickey.PublicKey()
        pk.rsa = self.publickey
        return pk

    def save(self, filename, hmac=0, _dsa=None, _hash=None):
        """Save public key to a file

        :param filename: (str) filename
        :param hmac: (int) HMAC hash digest
        :param _dsa: (obj) crypto engine
        :param _hash: (str) H(plaintext), bytes string form
        :return: N/A
        """
        interface.Base.bignum_to_c_byte(hmac, self.hmac)
        self.signature_size = ctypes.sizeof(self.signature)
        binary_for_sign = self.get_binary()
        binary_size = ctypes.sizeof(self.publickey) + ctypes.sizeof(self.hmac)
        self.signature = _dsa.generate_signature(binary_for_sign[:binary_size])
        f = open(filename, 'wb')
        f.write(self.get_binary())
        f.close()

    def load(self, filename=None, _dsa=None, _hash=None, verify=True, _bin=None):
        """Load public key from a file

        :param filename: (str) filename
        :param _dsa: (obj) crypto engine
        :param _hash: (obj) <NOT USED>
        :param verify: (bool) validation check for the public key file
        :param bin:
        :return: (obj) public key data object
        """
        if _bin is not None:
            _logger.debug('Loading from Testkey')
        else:
            _logger.debug(f"{filename} loading")
            with open(filename, 'rb') as (f):
                _bin = f.read()
        self.set_from_binary(_bin)
        key = self.get_key()
        if verify is True:
            _logger.debug('Public key file verification start')
            binary_for_sign = self.get_binary()
            binary_size = ctypes.sizeof(self.publickey)
            binary_size += ctypes.sizeof(self.hmac)
            verification = _dsa.verify(binary_for_sign[:binary_size], self.signature, key)
            if verification is True:
                _logger.debug('%s is a valid file.' % filename)
            else:
                _logger.error('%s is an invalid file.' % filename)
                return
        return key


class ECC(interface.Base):
    __doc__ = 'PublicKey for ECC'
    _fields_ = (
     (
      'size_of_key', ctypes.c_uint32),
     (
      'x', ctypes.c_ubyte * 68),
     (
      'y', ctypes.c_ubyte * 68),
     (
      'hmac', ctypes.c_ubyte * 32),
     (
      'signature_size', ctypes.c_uint32),
     (
      'r', ctypes.c_ubyte * 68),
     (
      's', ctypes.c_ubyte * 68))

    def set_key(self, key):
        """Set all attributes for the key"""
        self.size_of_key = ctypes.sizeof(self.x)
        if isinstance(key, publickey.PublicKey):
            self.x = key.ecc.x
            self.y = key.ecc.y
        else:
            if isinstance(key, publickey.ECCPublickey):
                self.x = key.x
                self.y = key.y
            else:
                _logger.error('Unknown publickey type')
                sys.exit(-1)

    def get_key(self):
        """Get public key data object

        :return: (obj) public key
        """
        pk = publickey.PublicKey()
        end = 4 + ctypes.sizeof(self.x) + ctypes.sizeof(self.y)
        pk.ecc.set_from_binary(self.get_binary()[4:end])
        return pk

    def save(self, filename, hmac=0, _dsa=None, _hash=None):
        """Save public key to a file

        :param filename: (str) filename
        :param hmac: (int) HMAC digest
        :param _dsa: (obj) crypto engine
        :param _hash: (str) H(plaintext)
        :return: N/A
        """
        self.bignum_to_c_byte(hmac, self.hmac)
        self.signature_size = ctypes.sizeof(self.r)
        binary_for_sign = self.get_binary()
        binary_size = 4
        binary_size += ctypes.sizeof(self.x)
        binary_size += ctypes.sizeof(self.y)
        binary_size += ctypes.sizeof(self.hmac)
        _hash = hashlib.sha512 if _hash is None else _hash
        _hash = _hash(binary_for_sign[:binary_size])
        sign = _dsa.generate_signature(_hash.hexdigest())
        self.r = sign.ecc.r
        self.s = sign.ecc.s
        with open(filename, 'wb') as (f):
            f.write(self.get_binary())

    def load(self, filename=None, _dsa=None, _hash=None, verify=True, _bin=None):
        """Load public key from a file

        :param filename: (str) filename
        :param _dsa: (obj) crypto engine
        :param _hash: (obj) hash algorithm object
        :param verify: (bool) validation check for the public key file
        :return: (obj) public key
        """
        if _bin is not None:
            _logger.debug('Loading from Testkey')
        else:
            _logger.debug(f"{filename} loading")
            with open(filename, 'rb') as (f):
                _bin = f.read()
        self.set_from_binary(_bin)
        key = self.get_key()
        if len(_bin) != 312 and verify is True:
            if self.r == 0 or self.s == 0:
                return
            sign = signature.Signature()
            sign.ecc.r = self.r
            sign.ecc.s = self.s
            binary_for_sign = self.get_binary()
            binary_size = 4
            binary_size += ctypes.sizeof(self.x)
            binary_size += ctypes.sizeof(self.y)
            binary_size += ctypes.sizeof(self.hmac)
            _hash = hashlib.sha512 if _hash is None else _hash
            _hash = _hash(binary_for_sign[:binary_size])
            verification = _dsa.verify(_hash.hexdigest(), sign, key)
            if verification is not True:
                return
        return key