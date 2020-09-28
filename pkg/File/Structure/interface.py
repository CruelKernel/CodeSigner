# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/File/Structure/interface.py
"""Definition of an interface for all data structures for CodeSigner

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import binascii, ctypes, logging, struct
__all__ = ('Base', )
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class Base(ctypes.LittleEndianStructure):
    _pack_ = 4
    space = 0
    _bytes_variables = []

    def set_attribute(self, param: dict):
        """Set values for all attributes of this class.

        :param param: (dict) attribute parameter
        :return: N/A
        """
        for _name, _type in self._fields_:
            if issubclass(_type, Base) and _name in param:
                exec(f'self.{_name}.set_attribute(param["{_name}"])')

        self._set_attribute(param)
        self._debug_set_attribute()

    def _set_attribute(self, param: dict):
        """Set value for all attributes

        :param param: (dict) additional attributes value
        :return: N/A
        """
        for _name in param:
            value = param[_name]
            if isinstance(value, dict):
                pass
            else:
                if _name in self._bytes_variables:
                    self.set_bytes(_name, value)
                else:
                    setattr(self, _name, value)

    def __repr__(self):
        """Re-define representation for this class

        :return: (str) representation for this class
        """
        msg = ''
        for _name, _type in self._fields_:
            val = eval(f"self.{_name}")
            msg += ' ' * Base.space
            if isinstance(val, ctypes.Union):
                msg += f"{_name} (Length: {ctypes.sizeof(val)} bytes)\n"
            elif issubclass(_type, Base):
                Base.space += 4
                msg += f"{_name.upper()}\n{val.__repr__()}"
                Base.space -= 4
            elif isinstance(val, str):
                msg += f"{_name} = {val}\n"
            else:
                if isinstance(val, int):
                    msg += f"{_name} = {val} ({hex(val)})\n"
                else:
                    if _name in ('func_ptr', 'reserved'):
                        msg += f"{_name} (Length: {ctypes.sizeof(val)} bytes)\n"
                    else:
                        if _name != 'image':
                            msg += f"{_name} = 0x{bytes(val).hex()}\n"

        return msg

    def _debug_set_attribute(self):
        """Print debug message for all attributes of this class

        :return: N/A
        """
        _logger.debug(f"Set attribute of {self.__class__.__name__} class")
        msg_list = self.__repr__().split('\n')
        for msg in msg_list:
            _logger.debug(msg)

    def get_binary(self):
        """Get binary formed string

        :return: (str) binary formed string
        """
        return memoryview(self).tobytes()

    def set_from_binary(self, binary):
        """Set all attributes from the binary

        :param binary: (str) binary string
        :return: N/A
        """
        fit = min(len(binary), ctypes.sizeof(self))
        ctypes.memmove(ctypes.addressof(self), binary, fit)

    def save(self, filename: str):
        """Save this class to a file

        :param str filename: file name
        :return: N/A
        """
        with open(filename, 'wb') as (f):
            f.write(self.get_binary())
            length = ctypes.sizeof(self)
            _logger.debug(f'"{filename}" was saved. ({length} byte)')

    def load(self, filename: str):
        """Load all attributes from a file

        :param str filename: file name
        :return: N/A
        """
        with open(filename, 'rb') as (f):
            self.set_from_binary(f.read())
            length = ctypes.sizeof(self)
            _logger.debug(f'"{filename}" was loaded. ({length} byte)')

    @staticmethod
    def c_byte_to_bignum(val):
        """Transform the number from bytes string to bignumber type

        :param val: (str) byte string
        :return: (ing) bignumber
        """
        hexstring = memoryview(val).hex()
        if len(hexstring) != 0:
            return int(hexstring, 16)
        else:
            return 0

    def set_bytes(self, field_name: str, value: any, _byteorder='little'):
        """

        :param field_name:
        :param int or bytes value:
        :param _byteorder:
        :return:
        """
        dst = getattr(self, field_name)
        length = ctypes.sizeof(dst)
        if isinstance(value, int):
            value = value.to_bytes(length, byteorder=_byteorder)
        struct.pack_into(f"{length}s", dst, 0, value[:length])

    @staticmethod
    def bignum_to_c_byte(src, dst, byteorder='little'):
        """Set dst with src value (bignumber)

        :param src: (str) value (bignumber type)
        :param dst: (str) target memory area (variable, bytes string type)
        :return: N/A
        """
        byte_length = ctypes.sizeof(dst)
        binary = binascii.unhexlify('%%0%dx' % (byte_length * 2) % src)
        struct.pack_into(f"{byte_length}s", dst, 0, binary)

    @staticmethod
    def str_to_c_byte(src, dst):
        """Set dst with src value (string)

        :param src: (str) source data
        :param dst: (str) destination
        :return: N/A
        """
        byte_length = ctypes.sizeof(dst)
        struct.pack_into('%ds' % byte_length, dst, 0, src)

    @staticmethod
    def flip(src_bytes):
        """Change byte order

        :param src_bytes: (str) target
        :return: N/A
        """
        _logger.debug('flip from 0x%s' % binascii.hexlify(src_bytes))
        tmp = src_bytes[:]
        tmp = tmp[::-1]
        tmp = ''.join(chr(e) for e in tmp)
        struct.pack_into('%ds' % ctypes.sizeof(src_bytes), src_bytes, 0, tmp)
        _logger.debug('flip to 0x%0x' % src_bytes)