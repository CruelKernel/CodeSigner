# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/Crypto/PyCrypto/__init__.py
"""PyCrypto Interface packages

    Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
from . import hash
from . import publickey_cipher
__all__ = ('hash', 'publickey_cipher')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'

class Hash(hash.Hash):
    pass


class HMAC(hash.HMAC):
    pass


class RSAPSS(publickey_cipher.RSAPSS):
    pass


class ECDSA:
    pass