# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/File/Structure/publickey.py
"""CodeSigner PublicKey structure

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import binascii, ctypes, struct
from . import interface
import pkg.settings
__all__ = ('PublicKey', 'RSAPublickey', 'ECCPublickey')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'

class ECCPublickey(interface.Base):
    __doc__ = 'PublickKey for Elliptic Curve'
    _fields_ = (
     (
      'x', ctypes.c_ubyte * 68),
     (
      'y', ctypes.c_ubyte * 68),
     (
      'padding', ctypes.c_ubyte * 388))

    def __init__(self, x=None, y=None):
        """Constructor

        :param x: (int) coordinate x
        :param y: (int) coordinate y
        """
        interface.Base.__init__(self)
        if x is not None:
            self.bignum_to_c_byte(x, self.x)
        if y is not None:
            self.bignum_to_c_byte(y, self.y)


class RSAPublickey(interface.Base):
    __doc__ = 'PublicKey for RSA algorithm'
    _fields_ = (
     (
      'size_of_n', ctypes.c_uint32),
     (
      'n', ctypes.c_ubyte * 512),
     (
      'size_of_e', ctypes.c_uint32),
     (
      'e', ctypes.c_uint32))

    def __init__(self, size_of_n=512, n=None, size_of_e=4, e=0):
        """Constructor

        :param size_of_n: (int) memory size of the variable, n (default: 256)
        :param n: (int) n value (default: None)
        :param size_of_e: (int) memory size of the variable, e (default: 4)
        :param e: (int) e value (default: None)
        """
        interface.Base.__init__(self)
        self.size_of_e = size_of_e
        self.size_of_n = size_of_n
        self.n = n
        self.e = e

    @staticmethod
    def bignum_to_c_byte(src, dst):
        """Set dst with src value (string)

        This method is different from Interface's bignum_to_c_byte() method.

        :param src: (str) source data
        :param dst: (str) destination
        :return: N/A
        """
        byte_length = ctypes.sizeof(dst)
        binary = binascii.unhexlify('%%0%dx' % (byte_length * 2) % src)
        struct.pack_into('%ds' % byte_length, dst, 0, binary[::-1])

    @staticmethod
    def c_byte_to_bignum(val):
        """Transform the number from bytes string to bignumber type

        This method is different from Interface's c_byte_to_bignum() method.

        :param val: (str) byte string
        :return: (ing) bignumber
        """
        return int(memoryview(val).tobytes()[::-1].hex(), 16)


class PublicKey(ctypes.Union):
    __doc__ = 'PublicKey union structure'
    _fields_ = (
     (
      'ecc', ECCPublickey),
     (
      'rsa', RSAPublickey))