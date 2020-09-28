# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/Crypto/__init__.py
"""Crypto Engine module

    Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import logging, sys
from . import engines
from .. import settings
__all__ = ('Factory', 'LSI', 'HSM', 'PyCrypto', 'PKCS11')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')
_conf = settings.Config()

class Factory:
    __doc__ = 'Crypto Engine Factory class'

    def __init__(self):
        pass

    @staticmethod
    def create_engine(_type=None) -> engines.BaseEngine:
        """Return Crypto engine object

        :param str _type: 'HSM' or 'LSI' (default: None)
        :return: engines.BaseEngine Crypto engine (LSI or HSM)
        """
        interfaces = engines.LSIEngine
        return interfaces()

    @staticmethod
    def _is_pkcs11_mode() -> bool:
        return _conf.pkcs11['enable'] is True