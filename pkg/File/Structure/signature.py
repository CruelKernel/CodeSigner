# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/File/Structure/signature.py
"""
    Filename: src/pkg/Structure/signature.py

    Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.

    Version History:
"""
import binascii, ctypes, logging, random, struct
from . import interface
__all__ = ('Signature', 'ECCSignature', 'RSASignature')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class ECCSignature(interface.Base):
    __doc__ = 'Signature structure for Elliptic Curve'
    _fields_ = (
     (
      'r', ctypes.c_ubyte * 68),
     (
      's', ctypes.c_ubyte * 68),
     (
      'padding', ctypes.c_ubyte * 376))

    def refresh_padding(self):
        """Re-fill padding area with random values

        This uses system random function instead of python's random function.

        :return: N/A
        """
        rand = random.SystemRandom()
        length = ctypes.sizeof(self.padding)
        padding = rand.getrandbits(length * 8)
        padding = padding.to_bytes(length, byteorder='little')
        struct.pack_into(f"{length}s", self.padding, 0, padding)


class RSASignature(interface.Base):
    __doc__ = 'Signature structure for RSA algorithm'
    _fields_ = (
     (
      'sign', ctypes.c_ubyte * 512),)

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


class Signature(ctypes.Union):
    __doc__ = 'Signature union structure'
    _fields_ = (
     (
      'ecc', ECCSignature),
     (
      'rsa', RSASignature))