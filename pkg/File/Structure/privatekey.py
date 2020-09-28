# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/File/Structure/privatekey.py
"""CodeSigner Private Key structure

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import binascii, ctypes, logging, random, struct
from . import interface
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')
__all__ = ('ECCPrivateKey', 'RSAPrivateKey')

class RSAPrivateKey(interface.Base):
    __doc__ = 'PrivateKey for RSA algorithm'
    _fields_ = (
     (
      'size_of_n', ctypes.c_uint32),
     (
      'n', ctypes.c_ubyte * 512),
     (
      'size_of_e', ctypes.c_uint32),
     (
      'e', ctypes.c_uint32),
     (
      'size_of_d', ctypes.c_uint32),
     (
      'd', ctypes.c_ubyte * 512),
     (
      'size_of_p', ctypes.c_uint32),
     (
      'p', ctypes.c_ubyte * 256),
     (
      'size_of_q', ctypes.c_uint32),
     (
      'q', ctypes.c_ubyte * 256),
     (
      'size_of_dP', ctypes.c_uint32),
     (
      'dP', ctypes.c_ubyte * 256),
     (
      'size_of_dQ', ctypes.c_uint32),
     (
      'dQ', ctypes.c_ubyte * 256),
     (
      'size_of_Q_inv', ctypes.c_uint32),
     (
      'Q_inv', ctypes.c_ubyte * 256),
     (
      'padding', ctypes.c_ubyte * 12))
    _bytes_variables = [
     'n', 'd', 'p', 'q', 'dP', 'dQ', 'Q_inv']

    def __init__(self):
        """Constructor"""
        interface.Base.__init__(self)
        self.size_of_n = ctypes.sizeof(self.n)
        self.size_of_e = 4
        self.size_of_d = ctypes.sizeof(self.d)
        self.size_of_p = ctypes.sizeof(self.p)
        self.size_of_q = ctypes.sizeof(self.q)
        self.size_of_dP = ctypes.sizeof(self.dP)
        self.size_of_dQ = ctypes.sizeof(self.dQ)
        self.size_of_Q_inv = ctypes.sizeof(self.Q_inv)

    def _set_attribute(self, param: dict):
        """

        :param param:
        :return:
        """
        for _key in param:
            if _key == 'e':
                self.e = param[_key]
            else:
                exec(f"self.bignum_to_c_byte({param[_key]}, self.{_key}")

    @staticmethod
    def bignum_to_c_byte(src, dst):
        """Save bignumber value to byte string variable

        :param src: (int) number
        :param dst: (str) target variable
        :return: N/A
        """
        byte_length = ctypes.sizeof(dst)
        binary = binascii.unhexlify('%%0%dx' % (byte_length * 2) % src)
        struct.pack_into('%ds' % byte_length, dst, 0, binary[::-1])

    @staticmethod
    def c_byte_to_bignum(val):
        """Get bignumber value from bytes string

        :param val: (str) bytes string (source variable)
        :return: (int) bignumber value
        """
        return int(binascii.hexlify(memoryview(val).tobytes()[::-1]), 16)

    def refresh_padding(self):
        """Fill padding area with random values

        :return: N/A
        """
        length = ctypes.sizeof(self.padding)
        padding = random.SystemRandom().getrandbits(length * 8)
        padding = padding.to_bytes(length, byteorder='little')
        struct.pack_into('%ds' % length, self.padding, 0, padding)


class ECCPrivateKey(interface.Base):
    __doc__ = 'PrivateKey for Elliptic Curve'
    _fields_ = (
     (
      'size_of_key', ctypes.c_uint32),
     (
      'key', ctypes.c_ubyte * 68))

    def __init__(self):
        """Constructor"""
        interface.Base.__init__(self)
        self.size_of_key = 68