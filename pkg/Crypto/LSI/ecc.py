# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/Crypto/LSI/ecc.py
"""Elliptic Curve Cryptography implementation

This is implemented for only CodeSigner.
This module does not use logging module of python.

In this module, we does not obey PEP-8 coding rules for ECC formulas.

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import copy, math, sys
from . import curves
from . import libs
__all__ = ('ECPoint', 'ECurve', 'ECurveSPC')
__VERSION__ = '3'
__AUTHOR__ = 'Lee, Hosub <hosub7.lee@samsung.com>'

class ECPoint:
    __doc__ = 'Elliptic Curve Point class'
    x, y, z = (0, 0, 0)
    _curve = None
    _prime = None

    def __init__(self, x=0, y=1, z=0, curve=None):
        """Constructor

        set member variables

        :param x: (int) coordinate X (default: 0)
        :param y: (int) coordinate Y (default: 1)
        :param z: (int) coordinate Z (default: 0)
        :param curve: (obj) ECurve object (default: None)
        """
        self.x, self.y, self.z = x, y, z
        self._curve = curve

    def set_infinity(self):
        """Set this point as an infinity point

        :return: N/A
        """
        self.x, self.y, self.z = (0, 1, 0)

    def set_curve(self, curve):
        """Set the curve value for this point

        :param curve: (obj) ECurve object
        :return: N/A
        """
        self._curve = curve

    def is_infinity(self):
        """Check whether this point is an infinity point, or not.

        :return:
        """
        if self.x == 0:
            if self.y == 1:
                if self.z == 0:
                    return True
        return False

    def __add__(self, other):
        """Operator overloading for Addition, 'this + other'

        :param other: (obj) ECPoint object
        :return: (obj) ECPoint, the result of addition operation on Curve
        """
        if not isinstance(other, ECPoint):
            print('[ERROR] ECPoint Addition Error')
            sys.exit(-1)
        return self._curve.addition(self, other)

    def __radd__(self, other):
        """Operator overloading for Addition, 'other + this'

        :param other: (obj) ECPoint object
        :return: (obj) ECPoint, the result of addition operation  on Curve
        """
        self.__add__(other)

    def __mul__(self, other):
        """Operator overloading for Multiplication, 'this * other'

        Actually, in the formula, this operation will be expressed like '2G'.
        '2G' means 2 * G and G means an elliptic point.

        :param other: (long) multiplier
        :return: (obj) ECPoint, the result of multiplication operation on Curve
        """
        if not isinstance(other, int):
            if not isinstance(other, long):
                print('[ERROR] ECPoint Multiplication Error')
                sys.exit(-1)
        return self._curve.multiplication(other, self)

    def __rmul__(self, other):
        """Operator overloading for Multiplication, 'other * this'

        Actually, in the formula, this operation will be expressed like '2G'.
        '2G' means 2 * G and G means an elliptic point.

        In our lib., some expression like 'G * 2' is permitted.

        :param other: (long) multiplier
        :return: (obj) ECPoint, the result of multiplication operation on Curve
        """
        return self.__mul__(other)

    def __repr__(self):
        """Representation for this object

        :return: (str) represent x, y, z values
        """
        return 'x = %#x\ny = %#x\nz = %#x' % (self.x, self.y, self.z)


class ECurve:
    __doc__ = 'Elliptic Curve class\n\n    In this class, we implement elliptic curve operations.\n    '

    def __init__(self):
        """Constructor"""
        self.a, self.b, self.p, self.n = (0, 0, 0, 0)
        self.G = None
        self.bits = 0
        self.bytes = 0
        self.name = None
        self.sBits = None

    def addition(self, P, Q):
        """add operation on this curve

        :param P: (obj) ECPoint
        :param Q: (obj) ECPoint
        :return: (obj) ECPoint
        """
        R = ECPoint(0, 1, 0, self)
        if P.x == 0:
            if P.y == 0:
                R = Q
        else:
            slope = (Q.y - P.y) * libs.inverse(self.p, (Q.x - P.x) % self.p) % self.p
            R.x = (slope ** 2 - P.x - Q.x) % self.p
            R.y = (slope * (P.x - R.x) - P.y) % self.p
        return R

    def doubling(self, P):
        """doubling operation on this curve

        Calculate 2 * P.

        :param P: (obj) ECPoint
        :return: (obj) ECPoint
        """
        R = ECPoint(0, 1, 0, self)
        slope = (3 * P.x ** 2 + self.a) * libs.inverse(self.p, 2 * P.y % self.p) % self.p
        R.x = (slope ** 2 - P.x - P.x) % self.p
        R.y = (slope * (P.x - R.x) - P.y) % self.p
        return R

    def multiplication(self, k, P):
        """multiplication operation on this curve

        :param k: (long) multiplier
        :param P: (obj) ECPoint
        :return: (obj) ECPoint
        """
        Q = ECPoint(0, 1, 0, self)
        i = 1 << self.bits - 1
        while i:
            Q = self.doubling(Q)
            if k & i:
                Q = P + Q
            i >>= 1

        inv_z = libs.inverse(self.p, Q.z)
        Q.x = Q.x * inv_z % self.p
        Q.y = Q.y * inv_z % self.p
        return Q

    def set_domain_parameter(self, name='NIST', bit=521):
        """Set domain parameters for ECC

        Set domain parameters

        This class supports NIST prime curves only.

        :param name: (str) 'NIST' or 'BrainPool' (default: 'NIST')
        :param bit: (int) 192 or 224 or 256 or 384 or 521 or ...
        :return: N/A
        """
        params = curves.curve_list[name][('p' + str(bit))]
        self.a = params['a']
        self.b = params['b']
        self.n = params['n']
        self.p = params['p']
        self.G = ECPoint((params['gx']), (params['gy']), (params['gz']), curve=self)
        self.name = name
        self.bits = bit
        self.bytes = int(math.ceil(bit / 8.0))


class ECurveSPC(ECurve):
    __doc__ = 'Elliptic Curve SPC class\n\n    This class implements prime curve standard projective coordinates.\n    '

    def addition(self, P, Q):
        """SPC addition operator

        :param P: (obj) ECPoint
        :param Q: (obj) ECPoint
        :return: (obj) ECPoint
        """
        u1 = Q.y * P.z % self.p
        u2 = P.y * Q.z % self.p
        v1 = Q.x * P.z % self.p
        v2 = P.x * Q.z % self.p
        R = ECPoint(0, 1, 0, self)
        if P.is_infinity():
            R = Q
        else:
            if Q.is_infinity():
                R = P
            else:
                if v1 == v2:
                    if u1 != u2:
                        R.set_infinity()
                    else:
                        R = self.doubling(P)
                else:
                    u = (u1 - u2) % self.p
                    v = (v1 - v2) % self.p
                    w = P.z * Q.z % self.p
                    a = (u ** 2 * w - v ** 3 - 2 * v ** 2 * v2) % self.p
                    R.x = v * a % self.p
                    R.y = (u * (v ** 2 * v2 - a) - v ** 3 * u2) % self.p
                    R.z = v ** 3 * w % self.p
        return R

    def doubling(self, P):
        """Doubling using projective coordinate

        :param P: (obj) ECPoint
        :return: (obj) ECPoint
        """
        Q = ECPoint(0, 1, 0, self)
        if P.is_infinity():
            Q = P
        else:
            w = self.a * P.z ** 2 + 3 * P.x ** 2 % self.p
            s = P.y * P.z % self.p
            b = P.x * P.y * s % self.p
            h = (w ** 2 - 8 * b) % self.p
            Q.x = 2 * h * s % self.p
            Q.y = (w * (4 * b - h) - 8 * P.y ** 2 * s ** 2) % self.p
            Q.z = 8 * s ** 3 % self.p
        return Q

    def multiplication(self, k, P):
        """Multiplication (Montmery ladder version)

        :param k: (int) multiplier
        :param P: (obj) ECPoint
        :return: (obj) ECPoint
        """
        R0 = ECPoint(0, 1, 0, self)
        R1 = copy.deepcopy(P)
        R1.z = 1
        i = 1 << self.bits - 1
        while i:
            if k & i == 0:
                R1 = R0 + R1
                R0 = self.doubling(R0)
            else:
                R0 = R0 + R1
                R1 = self.doubling(R1)
            i = i >> 1

        inv_z = libs.inverse(self.p, R0.z) % self.p
        R0.x = R0.x * inv_z % self.p
        R0.y = R0.y * inv_z % self.p
        return R0