# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/Crypto/LSI/ecdsa.py
"""Elliptic Curve Digital Signature Algorithm implementation

This is implemented for only CodeSigner.
This module does not use logging module of python.

IMPORTANT!! This implementation uses SHA512 HASH VALUE only for ECDSA.

In this module, we does not obey PEP-8 coding rules for ECDSA formulas.

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import hashlib, random
from . import ecc
from . import libs
__all__ = ('ECDSA', )
__VERSION__ = '2'
__AUTHOR__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
SRANDOM = random.SystemRandom()

class ECDSA:
    __doc__ = 'Elliptic Curve Digital Signature Alghorithm Class'

    def __init__(self, version, bit):
        """Constructor

        :param version: (str) 'NIST' only
        :param bit: (int) NIST prime curve
        """
        self.ec = ecc.ECurveSPC()
        self.ec.set_domain_parameter(version, bit)

    def generate_privatekey(self):
        """Generate privatekey

        :return: (long) privatekey (random number)
        """
        return SRANDOM.randint(1, self.ec.p - 1)

    def generate_publickey(self, privatekey):
        """Generate publickey

        :param privatekey: (long) privatekey
        :return: (obj) ECPoint
        """
        return privatekey * self.ec.G

    def sign(self, privatekey, e, k=0):
        """Generate signature

        IMPORTANT!! This implementation uses SHA512 HASH VALUE only.

        * DO NOT SET k value. k value exists for only testing.

        if k is 0, then this generates signature using random value
        if not, then this generate signature using K value instead of random.

        It means this will generate always same signature
        if you use FIXED 'k' value and FIXED 'e' value.

        :param privatekey: (long) privatekey
        :param e: (long) SHA512 value for plaintext
        :param k: (long) k (default: 0)
        :return: (tuple) (random, signature)
        """
        r, s = (0, 0)
        while s == 0:
            r = 0
            while r == 0:
                while k == 0:
                    k = SRANDOM.randint(1, self.ec.n - 1)

                P = k * self.ec.G
                r = P.x % self.ec.n

            e = int(e, 16)
            e = e if self.ec.bits >= 512 else e >> 512 - self.ec.bits
            inv_k = libs.inverse(self.ec.n, k)
            s = inv_k * (e + privatekey * r) % self.ec.n

        return (
         r, s)

    def verify(self, publickey, r, s, e):
        """Verify signature

        IMPORTANT!! This implementation uses SHA512 HASH VALUE only.

        :param publickey: (obj) ECPoint
        :param r: (long) random value
        :param s: (long) signature
        :param e: (long) SHA512 value for plaintext
        :return: (bool) True or False
        """
        inv_s = libs.inverse(self.ec.n, s)
        publickey.set_curve(self.ec)
        e = int(e, 16)
        e = e if self.ec.bits >= 512 else e >> 512 - self.ec.bits
        u1 = e * inv_s % self.ec.n
        u2 = r * inv_s % self.ec.n
        A = u1 * self.ec.G
        B = u2 * publickey
        ec = ecc.ECurve()
        ec.set_domain_parameter(self.ec.name, self.ec.bits)
        R = ec.addition(A, B)
        return R.x % self.ec.n == r


if __name__ == '__main__':
    ecdsa = ECDSA('BrainPoolTwisted', 384)
    prv = ecdsa.generate_privatekey()
    pub = ecdsa.generate_publickey(prv)
    msg = hashlib.sha512('aaaaaaaaaaaaaaaa').hexdigest()
    print('prv: %x' % prv)
    print('pub_x: %x' % pub.x)
    print('pub_y: %x' % pub.y)
    print('hash: %s' % msg)
    r, s = ecdsa.sign(prv, msg)
    print('sign_r %x' % r)
    print('sign_s %x' % s)
    print(ecdsa.verify(pub, r, s, msg))