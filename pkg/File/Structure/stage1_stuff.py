# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/File/Structure/stage1_stuff.py
"""CodeSigner data structures for STAGE1 Secure Images

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import ctypes, logging
from .interface import Base
from .publickey import PublicKey
__all__ = ('Header', 'ContextInfo', 'Context')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class DebugCertificate(Base):
    __doc__ = 'DebugCertificate Class'
    _fields_ = (
     (
      'debug_version', ctypes.c_uint32),
     (
      'priv_level', ctypes.c_uint32),
     (
      'chip_id', ctypes.c_uint64),
     (
      'reserved', ctypes.c_ubyte * 12))
    _bytes_variables = [
     'reserved']


class Header(Base):
    __doc__ = 'Header class for STAGE1 Secure Images'
    _fields_ = (
     (
      'num_of_sector', ctypes.c_uint32),
     (
      'checksum', ctypes.c_ubyte * 4),
     (
      'en_addr', ctypes.c_uint32),
     (
      'en_size', ctypes.c_uint32))
    _bytes_variables = [
     'checksum']


class ContextInfo(Base):
    __doc__ = 'ContextInfo class for STAGE1 Secure Images'
    _fields_ = (
     (
      'codesigner_version', ctypes.c_uint32),
     (
      'ap_info', ctypes.c_uint32),
     (
      'time', ctypes.c_uint64),
     (
      'rb_count', ctypes.c_uint32),
     (
      'signing_type', ctypes.c_uint32),
     (
      'description', ctypes.c_char * 36),
     (
      'key_index', ctypes.c_uint32))

    def _set_attribute(self, param: dict):
        """Set all attributes of this class

        :param param: <NOT USED>
        :return: N/A
        """
        for _name in param:
            value = param[_name]
            if _name == 'description':
                value = value[:35] + b'\x00'
            exec(f"self.{_name} = value")


class Context(Base):
    __doc__ = 'Context class'
    _fields_ = (
     (
      'info', ContextInfo),
     (
      'debug_certificate', DebugCertificate),
     (
      'st2_key_tee', PublicKey),
     (
      'st2_key_ree', PublicKey),
     (
      'func_ptr', ctypes.c_ubyte * 128),
     (
      'major_id', ctypes.c_ushort),
     (
      'minor_id', ctypes.c_ushort),
     (
      'reserved', ctypes.c_ubyte * 8),
     (
      'st1_publickey', PublicKey),
     (
      'hmac', ctypes.c_ubyte * 32))
    _bytes_variables = [
     'func_ptr', 'reserved']