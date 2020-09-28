# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/File/privatekey.py
"""CodeSigner private key file image

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import ctypes, logging, Crypto.Cipher.AES as AES
from .Structure import privatekey
from .. import settings
__all__ = ('Factory', )
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class Factory:
    __doc__ = 'Private key file object generator'

    @staticmethod
    def create(algorithm='ecc'):
        """Create private key image

        :param algorithm: (str) 'ecc' or 'rsa'
        :return: RSAPrivatekey file image for publickey file image
        """
        _classes = {'ecc':ECC, 
         'rsa':RSA}
        return _classes[algorithm.lower()]()


class RSA(privatekey.RSAPrivateKey):
    __doc__ = 'Private key file class for RSA Algorithm (SUPPORT 2048bits only)'

    def init_aes(self):
        """Initialize information for AES algorithm

        We use pycrypto lib. for AES algorithm.

        :return: (obj) AES object
        """
        default = settings.Default()
        iv = default.aes['PRIVATEKEY_ENCRYPTION']['INITIAL_VECTOR']
        key = default.aes['PRIVATEKEY_ENCRYPTION']['KEY']
        return AES.new(key, AES.MODE_CBC, iv)

    def save(self, filename, key=None):
        """Save private key to file

        Key file contents will be encrypted by AES.

        :param filename: (str) filename
        :param key: (obj) RSA Private Key
        :return: N/A
        """
        aes = self.init_aes()
        self.refresh_padding()
        f = open(filename, 'wb')
        f.write(aes.encrypt(key.get_binary()))
        f.close()

    def load(self, filename):
        """Load private key from a file and set all attributes from it.

        :param filename: (str) filename
        :return: N/A
        """
        aes = self.init_aes()
        f = open(filename, 'rb')
        self.set_from_binary(aes.decrypt(f.read()))
        f.close()

    @staticmethod
    def c_byte_to_bignum(val):
        """Transform the number from bytes string to bignumber type

        :param val: (str) byte string
        :return: (ing) bignumber
        """
        hexstring = memoryview(val).tobytes()
        return int.from_bytes(hexstring, byteorder='little')


class ECC(privatekey.ECCPrivateKey):
    __doc__ = 'Private key file class for ECC Algorithm'

    def save(self, filename, key=None):
        """Save private key to file

        :param filename: (str) filename
        :param key: (obj) ECC Private Key
        :return: N/A
        """
        self.size_of_key = ctypes.sizeof(self.key)
        self.key = key.key
        with open(filename, 'wb') as (f):
            f.write(self.get_binary())

    def load(self, filename):
        """Load private key from a file and set all attributes from it.

        :param filename: (str) filename
        :return: (obj) ECC PrivateKey
        """
        with open(filename, 'rb') as (f):
            self.set_from_binary(f.read())
        key = privatekey.ECCPrivateKey()
        key.size_of_key = self.size_of_key
        key.key = self.key
        return key