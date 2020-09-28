# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/diet_stage.py
"""Define CodeSigner base stage class

You can get a stage object using Factory class.

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import binascii, Crypto.Cipher.AES as AES, ctypes, sys, hashlib, logging
from . import Crypto
from . import File as st_file
from .File.Structure import publickey as st_publickey
from . import settings
from . import testkeys
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
__all__ = ('Factory', )
_logger = logging.getLogger('CodeSigner')
_conf = settings.Config()
_default = settings.Default()

class BaseStage:
    __doc__ = 'Base Stage class'
    _VERSION = None
    _opt = None

    def __init__(self):
        """Constructor of BaseStage class

        :return: N/A
        """
        _logger.debug('Call constructor of %s, Version %s' % (self, self._VERSION))
        self._opt = _conf.opt
        self._opt.key_id = self._opt.key_id.lower()
        self._crypto_ = None
        self._change_sign_type(_conf.opt.sign_type)

    def imgmake(self):
        """Image signing function

        This method will be realized on subclasses.

        :return: N/A
        """
        pass

    def verify(self):
        """Secure image verification function

        This method will be realized on subclasses.

        :return: N/A
        """
        pass

    def _refresh_crypto_engine(self):
        """Reload crypto engine using new options

        :return: N/A
        """
        self._crypto_ = Crypto.Factory.create_engine()

    def save_publickey(self, sign_type: int, filename: str):
        """Save publickey

        :param sign_type:
        :param filename:
        :return: N/A
        """
        with open(filename, 'wb') as (f):
            f.write(testkeys.publickey[sign_type])

    def _get_pka_obj(self, sign_type=None, engine=None):
        """Get public key algorithm object

        :param sign_type: (int) sign_type (program argument)
        :param engine: (class) crypto engine
        :return: (class) PKA object
        """
        sign_type = self._opt.sign_type if sign_type is None else sign_type
        engine = self._crypto_ if engine is None else engine
        if settings.SignType.is_rsa(sign_type):
            return engine.RSAPSS
        if settings.SignType.is_ecdsa(sign_type):
            return engine.ECDSA
        _logger.error('Wrong sign_type')
        sys.exit(-1)

    def _export_publickey(self):
        """Export PublicKey

        HSM case) Load publickey from HSM storage
        Standalone case) Load publickey from a file

        :return: (class) Publickey class
        """
        engine = self._get_pka_obj(self._opt.sign_type, self._crypto_)
        return engine.export_publickey()

    def _generate_publickey_block(self, pk, algorithm='hmac'):
        """Generate publickey byte block for HMAC

        :param pk: (class) PublicKey
        :param algorithm: (str) 'hmac' or 'crc32'
        :return: (str) PublicKey message block for HMAC
        """
        mapper = settings.SignType()
        if isinstance(pk, st_publickey.PublicKey):
            pk = pk.rsa if mapper.is_rsa(_conf.opt.sign_type) else pk.ecc
        msg = pk.get_binary()
        if isinstance(pk, st_publickey.ECCPublickey):
            end = ctypes.sizeof(pk)
            if algorithm == 'hmac':
                end -= ctypes.sizeof(pk.padding)
            msg = msg[:end]
        return bytes(msg)

    def _sign(self, data):
        """Generate digital signature

        :param data: (str) plaintext
        :return: (str) digital signature
        """
        sign_type = _conf.opt.sign_type
        engine = self._get_pka_obj(sign_type, self._crypto_)
        if settings.SignType.is_ecdsa(_conf.opt.sign_type):
            hash_engine = self._crypto_.Hash
            hash_engine.sha512(data)
            data = hash_engine.hexdigest()
        else:
            key = testkeys.privatekey[sign_type]
            if settings.SignType.is_rsa(sign_type):
                prv = st_file.Factory.create_rsa_privatekey_file()
                enc_var = _default.aes['PRIVATEKEY_ENCRYPTION']
                key = AES.new(enc_var['KEY'], AES.MODE_CBC, enc_var['INITIAL_VECTOR']).decrypt(key)
            else:
                if settings.SignType.is_ecdsa(sign_type):
                    prv = st_file.Factory.create_ecc_privatekey_file()
                else:
                    _logger(f"Wrong sign_type: {sign_type}")
                    sys.exit(-1)
        prv.set_from_binary(key)
        return engine.generate_signature(data, prv)

    def _verify(self, msg, sign, pk):
        """Verify digital signature

        :param msg: (str) plaintext
        :param sign: (str) target signature
        :param pk: (class) PublicKey object
        :return: (bool) the result of digital signature verification test
        """
        engine = self._get_pka_obj(self._opt.sign_type, Crypto.Factory.create_engine())
        if settings.SignType.is_ecdsa(_conf.opt.sign_type):
            hash_engine = self._crypto_.Hash
            hash_engine.sha512(msg)
            msg = hash_engine.hexdigest()
        return engine.verify(msg, sign, pk)

    def _change_sign_type(self, sign_type):
        """Change sign_type

        Set some variable related with sign_type

        :param sign_type: (int) program argument
        :return: N/A
        """
        mapper = settings.SignType()
        _conf.opt.sign_type = sign_type
        self._refresh_crypto_engine()
        msg = 'sign_type: %d (algorithm: %s, Curve: %s %d bit, %d Byte)'
        _logger.info(msg % (
         sign_type, mapper.get_algorithm(sign_type),
         mapper.get_curve(sign_type),
         mapper.get_bit(sign_type), mapper.get_byte(sign_type)))

    def _load_publickey(self, fname=None):
        """Load publickey

        :param fname: (str) filename
        :return: (obj) publickey
        """
        if settings.SignType.is_rsa(_conf.opt.sign_type):
            return self._load_rsa_publickey()
        else:
            if settings.SignType.is_ecdsa(_conf.opt.sign_type):
                return self._load_ecc_publickey()
            return

    def _load_publickey_file(self, fname=None):
        """Load publickey from file

        :param fname: (str) publickey filename
        :return: (obj) publickey class
        """
        fname = fname if fname is not None else self._get_publickey_file_path()
        pk = None
        dsa = None
        engine = Crypto.Factory.create_engine()
        if settings.SignType.is_rsa(_conf.opt.sign_type):
            pk = st_file.Factory.create_rsa_publickey_file()
            dsa = engine.RSAPSS
        else:
            if settings.SignType.is_ecdsa(_conf.opt.sign_type):
                pk = st_file.Factory.create_ecc_publickey_file()
                dsa = engine.ECDSA
            else:
                _logger.error('Public key file loading fail, %s' % fname)
                sys.exit(-1)
        pk.load(filename=fname,
          _dsa=dsa,
          verify=True,
          _bin=(testkeys.publickey[_conf.opt.sign_type]))
        return pk

    def _load_ecc_publickey(self, filename=None, verify=True):
        """Load ECC publickey

        :param filename: (str) publickey file name
        :param verify: (bool) Check the integrity of publickey
        :return: (obj) ECC publickey object
        """
        return st_file.Factory.create_ecc_publickey_file().load(filename=filename,
          _dsa=(Crypto.Factory.create_engine().ECDSA),
          verify=verify,
          _bin=(testkeys.publickey[_conf.opt.sign_type]))

    def _load_rsa_publickey(self, filename=None, verify=True):
        """Load RSA publickey

        :param filename: (str) publickey file name
        :param verify: (bool) Check the integrity of publickey
        :return: (obj) RSA publickey object
        """
        return st_file.Factory.create_rsa_publickey_file().load(filename=filename,
          _dsa=(Crypto.Factory.create_engine().RSAPSS),
          verify=verify,
          _bin=(testkeys.publickey[_conf.opt.sign_type]))

    def _save(self, contents: bytes, filename: str):
        """Save the contents to the file

        :param contents: (str) file contents
        :param filename: (str) file name
        :return: N/A
        """
        with open(filename, 'wb') as (f):
            f.write(contents)

    def _load(self, filename: str) -> bytes:
        """Load the contents from the file

        :param str filename: file name
        :return bytes: file contents
        """
        with open(filename, 'rb') as (f):
            return f.read()

    def _xor_bytes(self, xs: bytes, ys: bytes):
        """This function calculates string1 (XOR) string2

        :param xs: string variable 1
        :param ys: string variable 2
        :return: the result of (XOR) operation
        """
        len_xs = len(xs)
        len_ys = len(ys)
        if len_xs != len_ys:
            _logger.error(f"{len_xs} != {len_ys}")
            sys.exit(-1)
        return (b'').join(bytes([x ^ y]) for x, y in zip(xs, ys))

    def _checksum(self, img):
        """Calculate checksum for img variable

        :param img: (byte array) plaintext
        :return: (byte array) checksum value
        """
        return hashlib.sha512(img).digest()[:4]

    def _checksum_test(self, bl):
        """Compare a checksum value with another checksum value for bl variable

        :param bl: (class) Boot Loader class
        :return: (bool) The result of checksum test
        """
        _logger.debug('Checksum Test Start')
        checksum = bl.header.get_binary()[4:8]
        validation = self._checksum(bl.get_binary()[16:])
        _logger.debug('Original Checksum : %s' % binascii.hexlify(checksum))
        _logger.debug('Generated Checksum: %s' % binascii.hexlify(validation))
        if checksum == validation:
            return True
        else:
            return False

    def _generate_hmac_key(self, engine=None):
        if _conf.is_pkcs11_enabled():
            engine = self._crypto_.HMAC if engine is None else engine
            engine.keygen(self._opt.key_id + 'efuse', 512)

    def get_version(self):
        return self._VERSION

    def get_hmac_from_publickey_file(self) -> bytes:
        """Get HMAC values for publickey attribute from publickey file

        This function return HMAC value on publickey file.

        :return: (Hex str) HMAC value
        """
        _logger.debug('Load HMAC value from Publickey File')
        pk = self._load_publickey_file()
        return binascii.hexlify(pk.hmac).rjust(64, b'0')


class Stage2Static(BaseStage):
    _VERSION = '5'

    def imgmake(self):
        """Generate Secure BL2 image

        :return: N/A
        """
        bl2 = st_file.Factory.create_sbl2(self._opt.infile, 'imgmake')
        if _conf.opt.key_index == 0:
            _conf.opt.key_index = self._generate_key_index()
        bl2.set_attribute(param=dict(context=dict(rb_count=(_conf.opt.rb_count),
          sign_type=(_conf.opt.sign_type),
          key_type=(_conf.opt.key_type),
          key_index=(_conf.opt.key_index))))
        binary = bl2.get_binary()[:self.get_sign_size(bl2)]
        bl2.signature = self._sign(binary)
        if _conf.opt.debug is True:
            print(bl2)
        bl2.save(_conf.opt.outfile)
        return 0

    def verify(self):
        """Verify the integrity of Secure Boot Image

        :return: N/A
        """
        bl2 = st_file.Factory.create_sbl2(self._opt.outfile, 'verify')
        if _conf.opt.debug is True:
            print(bl2)
        self._change_sign_type(bl2.context.sign_type)
        binary = bl2.get_binary()[:self.get_sign_size(bl2)]
        pk = self._load_publickey()
        if pk is None:
            _logger.error('publickey file loading failed')
            sys.exit(-1)
        result = self._verify(binary, bl2.signature, pk)
        _logger.info('Verification result is %s' % ('True' if result else 'False'))
        if result is not True:
            sys.exit(-1)
        return 0

    def get_sign_size(self, bl):
        """Return the image size to generate signature or verify it.

        :param bl: (obj) an object for Boot Loader class
        :return: (int) the size to generate digital signature for Boot Loader
        """
        return ctypes.sizeof(bl) - ctypes.sizeof(bl.signature)

    def _generate_key_index(self):
        pk = self._load_publickey()
        if pk is None:
            _logger.error('publickey file loading failed')
            sys.exit(-1)
        return binascii.crc32(self._generate_publickey_block(pk, 'crc32'))


class Stage2Dynamic(Stage2Static):
    __doc__ = 'CodeSigner v4.1.1 Stage2 Dynamic Length class\n\n    In this class, CodeSigner uses keygen method of Static class.\n    '
    _VERSION = '5'

    def imgmake(self):
        """Generate Secure EL3-Monitor image

        :return: N/A
        """
        el3 = st_file.Factory.create_el3(_conf.opt.infile, 'imgmake')
        if self._checksum_test(el3) is False:
            _logger.error('CHECKSUM ERROR')
            sys.exit(-1)
        _logger.info('Checksum Test: pass')
        if _conf.opt.key_index == 0:
            _conf.opt.key_index = self._generate_key_index()
        el3.set_attribute(param=dict(header=dict(num_of_sector=(int(ctypes.sizeof(el3) / 512)),
          checksum=0,
          magic_key=(_default.stage2['BL2_MAGIC_MARK']),
          reserved=0),
          context=dict(rb_count=(_conf.opt.rb_count),
          sign_type=(_conf.opt.sign_type),
          key_type=(_conf.opt.key_type),
          key_index=(_conf.opt.key_index))))
        binary = el3.get_binary()[:self.get_sign_size(el3)]
        el3.signature = self._sign(binary)
        checksum = self._checksum(el3.get_binary()[16:])
        el3.str_to_c_byte(checksum, el3.header.checksum)
        if _conf.opt.debug is True:
            print(el3)
        el3.save(_conf.opt.outfile)
        return 0

    def verify(self):
        """Verify the integrity of Secure Boot Image

        :return: N/A
        """
        el3 = st_file.Factory.create_el3(self._opt.outfile, 'verify')
        if _conf.opt.debug is True:
            print(el3)
        if self._checksum_test(el3) is False:
            _logger.error('CHECKSUM ERROR')
            sys.exit(-1)
        _logger.info('Checksum Test: pass')
        el3.bignum_to_c_byte(0, el3.header.checksum)
        self._change_sign_type(el3.context.sign_type)
        binary = el3.get_binary()[:self.get_sign_size(el3)]
        pk = self._load_publickey()
        if pk is None:
            _logger.error('publickey file loading failed')
            sys.exit(-1)
        result = self._verify(binary, el3.signature, pk)
        str_res = 'True' if result is True else 'False'
        _logger.info('Verification result is %s' % str_res)
        if result is False:
            sys.exit(-1)
        return 0