# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/Crypto/engines.py
"""Crypto engine module

    Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.

    Version History:
        Version 2, 2015.06.31., Lee, Hosub
            - Added configuration for logging module
"""
import logging
from . import LSI
from . import PyCrypto
from . import PKCS11
from .. import settings
__all__ = ('HSMEngine', 'LSIEngine', 'PKCS11Engine')
__version__ = '3'
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')
_conf = settings.Config()

class BaseEngine:
    __doc__ = 'Base class for Crypto engine'
    Hash = None
    HMAC = None
    RSAPSS = None
    ECDSA = None

    def __init__(self, _hash, _hmac, _rsa_pss, _ecdsa):
        """Constructor of BaseEngine

        :param _hash: class for hash
        :param _hmac: class for HMAC
        :param _rsa_pss: class for RSA-PSS-2048
        :param _ecdsa: class for ECDSA
        """
        _logger.debug('Run %s Constructor' % self.__class__.__name__)
        self._opt = _conf.opt
        self.Hash = _hash()
        self.HMAC = _hmac()
        self.RSAPSS = _rsa_pss()
        self.ECDSA = _ecdsa()


class LSIEngine(BaseEngine):
    __doc__ = 'In-house crypto engine\n\n    This class consists of follow algorithms:\n    - hash: pycrypto\n    - hmac: pycrypto\n    - rsa-pss: pycrypto\n    - ecdsa: In-house code\n    '

    def __init__(self, _hash=PyCrypto.Hash, _hmac=PyCrypto.HMAC, _rsa_pss=PyCrypto.RSAPSS, _ecdsa=LSI.ECDSA):
        BaseEngine.__init__(self, _hash, _hmac, _rsa_pss, _ecdsa)


class PKCS11Engine(BaseEngine):
    __doc__ = 'PKCS11 (cryptoki) class\n    '

    def __init__(self, _hash=PyCrypto.Hash, _hmac=PyCrypto.HMAC, _rsa_pss=PyCrypto.RSAPSS, _ecdsa=LSI.ECDSA):
        BaseEngine.__init__(self, _hash, _hmac, _rsa_pss, _ecdsa)