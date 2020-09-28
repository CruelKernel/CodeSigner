# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/Crypto/LSI/libs.py
"""Crypto lib. implementation

This is implemented for only CodeSigner.

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
__all__ = ('inverse', )
__version__ = '2.0'
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'

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