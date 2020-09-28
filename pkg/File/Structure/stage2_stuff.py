# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/File/Structure/stage2_stuff.py
"""CodeSigner data structures for STAGE2 Secure Images

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import ctypes, logging, struct
from . import interface
__all__ = ('Header', 'Context')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class Header(interface.Base):
    __doc__ = 'Header class'
    _fields_ = (
     (
      'num_of_sector', ctypes.c_uint32),
     (
      'checksum', ctypes.c_ubyte * 4),
     (
      'magic_key', ctypes.c_ubyte * 4),
     (
      'reserved', ctypes.c_ubyte * 4))
    _bytes_variables = [
     'checksum', 'reserved']

    def set_magic_key(self, key):
        """Set magic_key value

        <THIS METHOD WILL USE FOR ONLY EL3-MONITOR IMAGE>

        :param key: (str) magic key value
        :return: N/A
        """
        struct.pack_into('%ds' % ctypes.sizeof(self.magic_key), self.magic_key, 0, key)

    def _set_attribute(self, param: dict):
        """Set all attributes of this class

        :param param:
        :return:
        """
        self.num_of_sector = param['num_of_sector']
        self.bignum_to_c_byte(param['checksum'], self.checksum)
        self.set_magic_key(param['magic_key'])
        self.bignum_to_c_byte(param['reserved'], self.reserved)


class Context(interface.Base):
    _fields_ = (
     (
      'rb_count', ctypes.c_uint32),
     (
      'sign_type', ctypes.c_uint32),
     (
      'key_type', ctypes.c_uint32),
     (
      'key_index', ctypes.c_uint32))