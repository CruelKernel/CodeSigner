# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/Crypto/PyCrypto/publickey_cipher.py
"""Publickey algorithm module

We implement RSA-PSS class only using pycrypto
because pycrypto does not support ECDSA.

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import binascii, hashlib, hmac, logging, os, sys, Crypto.Hash.SHA256, Crypto.Hash.SHA512, Crypto.PublicKey.RSA, Crypto.Random, Crypto.Signature.PKCS1_PSS
from ...File.Structure import publickey as st_publickey
from ...File.Structure import privatekey as st_privatekey
from ...File.Structure import signature as st_signature
from ... import File as st_file
from ... import settings
__VERSION__ = '2'
__AUTHOR__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')
_conf = settings.Config()

def egcd(a, b):
    """Extended Euclidean algorithm

    :param a: (int)
    :param b: (int)
    :return: (tuple) gcd, x, y
    """
    x, y, u, v = (0, 1, 1, 0)
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = (a, r, u, v, m, n)

    return (
     b, x, y)


def inverse(a, m):
    """Modular Inverse Function

    :param a: (int)
    :param m: (int)
    :return: (int) Inverse value or None
    """
    gcd, x, y = egcd(m, a)
    if gcd == 1:
        return x % a


class PKA:
    __doc__ = 'Public Key Algorithm class\n\n    This is a base class for RSA-PSS and ECDSA class.\n    '

    def __init__(self):
        self._opt = _conf.opt
        self._engine = None

    def generate_publickey(self, privatekey):
        pass

    def export_publickey(self):
        pk = st_publickey.PublicKey()
        return pk

    def get_privatekey(self):
        pass

    def generate_signature(self, hash_digest):
        pass

    def verify(self, hex_digest, sign, pk):
        pass

    def _return_signature(self, reply_msg):
        pass

    def _get_interface(self):
        pass


class RSAPSS(PKA):
    __doc__ = 'RSA-PSS Class'

    def __init__(self):
        PKA.__init__(self)

    def generate_privatekey(self):
        """Generate private key

        :return: (obj) RSAPrivateKey
        """
        mapper = settings.SignType()
        sign_type = _conf.opt.sign_type
        key_size = mapper.get_bit(sign_type)
        privatekey = Crypto.PublicKey.RSA.generate(bits=key_size,
          e=3,
          randfunc=(Crypto.Random.new().read))
        _dp = privatekey.d % (privatekey.p - 1)
        _dq = privatekey.d % (privatekey.q - 1)
        _q_inv = inverse(privatekey.p, privatekey.q) % privatekey.p
        prv = st_privatekey.RSAPrivateKey()
        prv.set_attribute(param=dict(n=(privatekey.n),
          e=(privatekey.e),
          d=(privatekey.d),
          p=(privatekey.p),
          q=(privatekey.q),
          dP=_dp,
          dQ=_dq,
          Q_inv=_q_inv))
        return prv

    def generate_publickey(self, privatekey):
        """Generate public key

        This function implements public key generation logic

        :param privatekey: (obj) RSAPrivateKey object
        :return: (obj) RSAPublicKey object
        """
        if not isinstance(privatekey, st_privatekey.RSAPrivateKey):
            _logger.error('Wrong Privatekey')
            sys.exit(-1)
        pub = st_publickey.RSAPublickey(size_of_n=(settings.SignType().get_byte(_conf.opt.sign_type)),
          n=(privatekey.n),
          size_of_e=4,
          e=(privatekey.e))
        return pub

    def generate_keypair(self):
        """Generate Key-pair

        :return: N/A
        """
        privatekey = self.generate_privatekey()
        publickey = self.generate_publickey(privatekey)
        self.import_privatekey(privatekey)
        self.import_publickey(publickey)
        if self.export_publickey() is None:
            _logger.error('Wrong publickey file')
            sys.exit(-1)
        _logger.info('Key-pair generation was well done.')

    def import_privatekey(self, privatekey):
        """Save privatekey to privatekey file

        :param privatekey: (obj) RSAPrivateKey
        :return: N/A
        """
        path = self._opt.path + self._opt.key_id
        privatekey_filename = path + _conf.default['COMMON']['PRIVATEKEY_EXT']
        prv_file = st_file.Factory.create_rsa_privatekey_file()
        prv_file.save(privatekey_filename, privatekey)

    def import_publickey(self, publickey):
        """Save publickey to publickey file

        :param publickey: (obj) RSAPublicKey
        :return: N/A
        """
        pub_file = st_file.Factory.create_rsa_publickey_file()
        path = self._opt.path + self._opt.key_id
        pub_filename = path + _conf.default['COMMON']['PUBLICKEY_EXT']
        pub_file.set_key(publickey)
        pub_file.save(filename=pub_filename,
          _dsa=self,
          hmac=(int(hmac.new(key=(hashlib.sha256(_conf.opt.key_id).digest()), msg=(publickey.rsa.get_binary()), digestmod=(hashlib.sha256)).hexdigest(), 16) if _conf.opt.STAGE1 is True else 0))

    def export_privatekey(self):
        """Load privatekey from file

        :return: (obj) File/Privatekey/RSA
        """
        default = settings.Default()
        f_prv_key = st_file.Factory.create_rsa_privatekey_file()
        path = self._opt.path + self._opt.key_id
        privatekey_filename = path + default.common['PRIVATEKEY_EXT']
        f_prv_key.load(privatekey_filename)
        return f_prv_key

    def export_publickey(self):
        """Load publickey from file

        :return: (obj) File/Publickey/RSA
        """
        f_pub_key = st_file.Factory.create_rsa_publickey_file()
        path = self._opt.path + self._opt.key_id
        publickey_filename = path + _conf.default['COMMON']['PUBLICKEY_EXT']
        result = f_pub_key.load(filename=publickey_filename, _dsa=self)
        if result is None:
            _logger.error('publickey file verification fail. (%s)' % f_pub_key)
            sys.exit(-1)
        return result

    def generate_signature(self, plaintext, privatekey=None):
        """Generate signature

        :param plaintext: (str) plaintext
        :param privatekey: (obj) RSAPrivateKey
        :return: (obj) RSA Signature
        """
        prv = self.export_privatekey() if privatekey is None else privatekey
        p = prv.c_byte_to_bignum(prv.p)
        q = prv.c_byte_to_bignum(prv.q)
        u = inverse(q, p) % q
        prv = Crypto.PublicKey.RSA.RSAImplementation().construct((
         prv.c_byte_to_bignum(prv.n), prv.e, prv.c_byte_to_bignum(prv.d),
         p, q, u))
        signer = Crypto.Signature.PKCS1_PSS.new(prv)
        _hash = Crypto.Hash.SHA512.new(plaintext)
        _logger.debug('SHA512: %s' % _hash.hexdigest())
        sign = signer.sign(_hash)
        _logger.debug('signature: 0x%s' % binascii.hexlify(sign))
        return self._return_signature(sign)

    def _return_signature(self, reply_msg):
        """Formatting return value of generate_signature() method

        :param reply_msg: (str) signature value
        :return: (obj) RSA Signature
        """
        sign = st_signature.Signature()
        sign.rsa.bignum_to_c_byte(int(binascii.hexlify(reply_msg), 16), sign.rsa.sign)
        return sign

    def verify(self, plaintext, sign, pk, key_size=0):
        """Verify digital signature

        :param plaintext: (str) plaintext to generate signature
        :param sign: (str) signature (for verification)
        :param pk: (obj) RSAPublicKey
        :param key_size: (int) key size (bit)
        :return: (bool) The result of verification test
        """
        if key_size == 0:
            start = settings.SignType().get_byte(_conf.opt.sign_type) - 1
        else:
            start = key_size / 8 - 1
        _hash = Crypto.Hash.SHA512.new(plaintext)
        pub_key = Crypto.PublicKey.RSA.RSAImplementation().construct((
         pk.rsa.c_byte_to_bignum(pk.rsa.n), pk.rsa.e))
        verifier = Crypto.Signature.PKCS1_PSS.new(pub_key)
        return verifier.verify(_hash, sign.rsa.get_binary()[start::-1])