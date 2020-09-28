# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/Crypto/PKCS11/__init__.py
"""PyCrypto Interface packages

    Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import logging, os, pkcs11
from ... import settings
_conf = settings.Config()
_logger = logging.getLogger('CodeSigner')
__version__ = '1'
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'

class Base:

    def __init__(self, lib_path=None):
        """Constructor

        :param str lib:
        """
        _logger.debug(f"Run constructor of {self}")
        _logger.debug(f"Loading PKCS11 lib. from {lib_path}")
        self.lib = None
        self.token = None
        self.session = None
        self.load_lib(lib_path)

    def _init_nfast_softkey_env(self, env: dict):
        os.environ.update(env)

    def load_lib(self, lib_path: str) -> bool:
        self.lib = pkcs11.lib(lib_path)
        return self.lib is not None

    def _get_token(self, label: str) -> pkcs11.Token:
        return self.lib.get_token(token_label=label)

    def _get_slots(self) -> list:
        return self.lib.get_slots()

    def _open_session(self, pin: str, writable: bool) -> pkcs11.Session:
        return self.token.open(user_pin=pin, rw=writable)

    def _close_session(self):
        self.session.close()


class Hash(Base):
    __doc__ = 'Never use this class\n\n    We never use hash algorithms using PKCS11/HSM.\n    '


class HMAC(Base):
    pass


class RSAPSS(Base):
    pass


class ECDSA(Base):
    pass