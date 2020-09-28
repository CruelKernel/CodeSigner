# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/Crypto/LSI/__init__.py
"""Samsung Electronics S.LSI In-house Crypto package

This is implemented for only CodeSigner.

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import hashlib, logging, sys, hmac
from . import ecc, ecdsa, libs
from ...File.Structure import publickey as st_publickey
from ...File.Structure import privatekey as st_privatekey
from ...File.Structure import signature as st_signature
from ... import File as st_file
from ... import settings
__all__ = ('ecc', 'ecdsa')
__VERSION__ = '2'
__AUTHOR__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')
_conf = settings.Config()

class PKA:
    __doc__ = 'Public Key Algorithm class'

    def __init__(self):
        _logger.debug('Run LSI PKA Constructor, %s' % self)
        self._engine = None

    def generate_keypair(self):
        self.generate_privatekey()
        self.generate_publickey()

    def generate_privatekey(self):
        pass

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

    def set_engine(self, sign_type=None):
        mapper = settings.SignType()
        sign_type = _conf.opt.sign_type if sign_type is None else sign_type
        if settings.SignType.is_ecdsa(sign_type) is False:
            self._engine = None
        else:
            curve = mapper.get_curve(sign_type)
            bits = mapper.get_bit(sign_type)
            _logger.debug('Set engine, %s >> %s-%s' % (self, curve, bits))
            self._engine = ecdsa.ECDSA(curve, bits)


class ECDSA(PKA):
    __doc__ = 'ECDSA Class'

    def __init__(self, sign_type=None):
        _logger.debug('Run LSI ECDSA Constructor, %s' % self)
        PKA.__init__(self)
        self._engine = None
        sign_type = _conf.opt.sign_type if sign_type is None else sign_type
        self.set_engine(sign_type)

    def generate_privatekey(self):
        """Generate private key

        :return: (obj) ECCPrivateKey
        """
        import struct
        _logger.debug('Generate ECDSA Private key')
        privatekey = self._engine.generate_privatekey()
        prv = st_privatekey.ECCPrivateKey()
        prv.size_of_key = 68
        a = privatekey.to_bytes((prv.size_of_key), byteorder='big')
        struct.pack_into(f"{prv.size_of_key}s", prv.key, 0, a)
        return prv

    def generate_publickey(self, privatekey):
        """Generate public key

        :param privatekey: (obj) ECCPrivateKey
        :return: (obj) ECCPublicKey
        """
        _logger.debug('Generate ECDSA Public key')
        if not isinstance(privatekey, st_privatekey.ECCPrivateKey):
            _logger.error('Wrong privatekey type was used.')
            sys.exit(-1)
        prv = int(bytes(privatekey.key).hex(), 16)
        pub_key = self._engine.generate_publickey(prv)
        publickey = st_publickey.ECCPublickey()
        publickey.bignum_to_c_byte(pub_key.x, publickey.x)
        publickey.bignum_to_c_byte(pub_key.y, publickey.y)
        return publickey

    def generate_keypair(self):
        """Generate private key and public key

        :return: N/A
        """
        privatekey = self.generate_privatekey()
        publickey = self.generate_publickey(privatekey)
        self.import_privatekey(privatekey)
        self.import_publickey(publickey)
        if self.export_publickey() is None:
            _logger.error('Wrong publickey file type')
            sys.exit(-1)
        _logger.info('Key-pair generation was well done.')

    def save_privatekey(self, privatekey):
        """Save private key to a file

        :param privatekey: (obj) ECCPrivateKey
        :return: N/A
        """
        self.import_privatekey(privatekey)

    def save_publickey(self, publickey, _hmac='0' * 32):
        """Save public key to a file

        :param publickey: (obj) ECCPublicKey
        :param _hmac: (str) HMAC hexdigest value
        :return: (obj) ECC object defined in "structure/file/publickey.py"
        """
        pub_file = st_file.Factory.create_ecc_publickey_file()
        path = _conf.opt.path + _conf.opt.key_id
        publickey_filename = path + _conf.default['common']['publickey_ext']
        pub_file.set_key(publickey)
        pub_file.save(filename=publickey_filename,
          _dsa=self,
          _hash=(hashlib.sha512),
          hmac=_hmac)
        _logger.debug('Publickey file was saved. (%s)' % publickey_filename)
        return pub_file

    def import_privatekey(self, privatekey):
        """Save private key to a file

        :param privatekey: (obj) ECCPrivateKey
        :return: N/A
        """
        path = _conf.opt.path + _conf.opt.key_id
        privatekey_filename = path + _conf.default['common']['privatekey_ext']
        prv_file = st_file.Factory.create_ecc_privatekey_file()
        prv_file.save(privatekey_filename, privatekey)
        _logger.debug('Privatekey file was saved. (%s)' % privatekey_filename)

    def import_publickey(self, publickey):
        """Save public key to a file

        :param publickey: (obj) ECCPublicKey
        :return: N/A
        """
        config = pkg.settings.Config()
        pub_file = st_file.Factory.create_ecc_publickey_file()
        path = _conf.opt.path + _conf.opt.key_id
        publickey_filename = path + '.publickey'
        pub_file.set_key(publickey)
        _logger.debug('Publickey file was saved. (%s)' % publickey_filename)
        pub_file.save(filename=publickey_filename,
          _dsa=self,
          _hash=(hashlib.sha512),
          hmac=(int(hmac.new(key=(hashlib.sha256(config.opt.key_id).digest()), msg=(publickey.rsa.get_binary()), digestmod=(hashlib.sha256)).hexdigest(), 16) if config.opt.STAGE1 is True else 0))

    def export_privatekey(self):
        """Load private key from a file

        :return: (obj) ECCPrivateKey
        """
        f_pvk = st_file.Factory.create_ecc_privatekey_file()
        fname = _conf.opt.path + _conf.opt.key_id + '.privatekey'
        return f_pvk.load(fname)

    def export_publickey(self):
        """Load public key from a file

        :return: (obj) ECCPublicKey
        """
        f_pbk = st_file.Factory.create_ecc_publickey_file()
        fname = _conf.opt.path + _conf.opt.key_id + '.publickey'
        return f_pbk.load(filename=fname, _dsa=self, _hash=(hashlib.sha512))

    def generate_signature(self, hash_digest, privatekey=None):
        """Generate digital signature

        :param hash_digest: (str) Hash digest for plaintext (hex string)
        :param privatekey: (obj) ECCPrivateKey
        :return: (obj) ECC Signature
        """
        key = self.export_privatekey() if privatekey is None else privatekey
        key = key.c_byte_to_bignum(key.key)
        reply_msg = self._engine.sign(key, hash_digest)
        return self._return_signature(reply_msg)

    def _return_signature(self, reply_msg):
        """Formatting return value of generate_signature() method

        :param reply_msg: (str) signature value
        :return: (obj) ECC Signature
        """
        sign = st_signature.Signature()
        sign.ecc.bignum_to_c_byte(reply_msg[0], sign.ecc.r)
        sign.ecc.bignum_to_c_byte(reply_msg[1], sign.ecc.s)
        sign.ecc.refresh_padding()
        return sign

    def verify(self, hex_digest, sign, pk):
        """Verify digital signature

        :param hex_digest: (str) plaintext to generate signature
        :param sign: (str) signature (for verification)
        :param pk: (obj) ECCPublicKey
        :return: (bool) The result of verification test
        """
        ecpoint_pk = ecc.ECPoint()
        ecpoint_pk.x = pk.ecc.c_byte_to_bignum(pk.ecc.x)
        ecpoint_pk.y = pk.ecc.c_byte_to_bignum(pk.ecc.y)
        return self._engine.verify(ecpoint_pk, sign.ecc.c_byte_to_bignum(sign.ecc.r), sign.ecc.c_byte_to_bignum(sign.ecc.s), hex_digest)