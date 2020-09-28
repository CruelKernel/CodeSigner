# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/File/boot_loader.py
"""Secure Boot Loader structures

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import ctypes, sys, logging
from .Structure import interface
from .Structure import stage1_stuff
from .Structure import stage2_stuff
from .Structure import signature
__all__ = ('Factory', )
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class Factory:
    __doc__ = 'Secure Boot Loader Image Generator'

    @staticmethod
    def create_sbl1(filename, mode='imgmake', version='lastest'):
        """Generate Secure Boot Image for STAGE1

        if mode == 'imgmake', the file (from filename) will be used
        as a part of full structured Image, BL1 image.

        if mode == 'verify', the file (from filename) will be used
        as a full structured Image, SBL1 image. And checksum must be valid.

        :param filename: (str) Filename
        :param mode: (str) 'imgmake' or 'verify'
        :param version: (str) <NOT USED>
        :return: (obj) SBL1 object
        """
        with open(filename, 'rb') as (f):
            contents = f.read()
        img_len = len(contents)
        _logger.debug(f'"{filename}" was loaded. ({img_len} byte)')
        if mode == 'verify':
            hdr_len = ctypes.sizeof(stage1_stuff.Header)
            ctx_len = ctypes.sizeof(stage1_stuff.Context)
            sign_size_len = 4
            sign_len = ctypes.sizeof(signature.Signature)
            img_len -= hdr_len + ctx_len + sign_size_len + sign_len
        else:

            class SBL1(interface.Base):
                __doc__ = 'Secure Boot Loader for STAGE1\n\n            SBL1 size must be a multiple of 512\n            < (sizeof(BL1) + 1040) %512 == 0 is True>\n            '
                _fields_ = (
                 (
                  'header', stage1_stuff.Header),
                 (
                  'image', ctypes.c_ubyte * img_len),
                 (
                  'context', stage1_stuff.Context),
                 (
                  'signature_size', ctypes.c_uint32),
                 (
                  'signature', signature.Signature))

                def get_image(self, length=0):
                    """Get Boot Loader image only

                if you know already the image size,
                pass the value through the parameter named 'length'.

                :param length: (int) Boot Loader Size (default: 0)
                :return: (str) bytes string (binary image)
                """
                    img = self.get_binary()
                    start = ctypes.sizeof(self.header)
                    if length != 0:
                        end = start + length
                    else:
                        end = len(img) - ctypes.sizeof(self.context) - 4 - ctypes.sizeof(self.signature)
                    return img[start:end]

            bl1 = SBL1()
            if 'imgmake' == mode:
                length = ctypes.sizeof(bl1)
                if length % 512 == 0:
                    bl1.header.num_of_sector = length / 512
                else:
                    _logger.error('BL1 size error')
                    _logger.error(f"{length} %% 512 != 0 (value: {length % 512})")
                    sys.exit(-1)
                bl1.str_to_c_byte(contents, bl1.image)
            else:
                bl1.set_from_binary(contents)
        return bl1

    @staticmethod
    def create_sbl2(filename, mode='imgmake', version='latest'):
        """Generate Secure Boot Image for STAGE2 (FIXED LENGTH)

        if mode == 'imgmake', the file (from filename) will be used
        as a part of full structured Image, BL2 image.

        if mode == 'verify', the file (from filename) will be used
        as a full structured Image, SBL2 image. And checksum must be valid.

        :param filename: (str) Filename
        :param mode: (str) 'imgmake' or 'verify'
        :param version: (str) <NOT USED>
        :return: (obj) SBL2 object
        """
        with open(filename, 'rb') as (f):
            contents = f.read()
        ctx_length = ctypes.sizeof(stage2_stuff.Context)
        sign_length = ctypes.sizeof(signature.Signature)
        img_length = len(contents) - ctx_length - sign_length

        class SBL2(interface.Base):
            __doc__ = 'Secure Boot Loader for STAGE2 <FIXED LENGTH TYPE>'
            _fields_ = (
             (
              'image', ctypes.c_ubyte * img_length),
             (
              'context', stage2_stuff.Context),
             (
              'signature', signature.Signature))

        bl2 = SBL2()
        bl2.set_from_binary(contents)
        return bl2

    @staticmethod
    def create_el3(filename, mode='imgmake', version='latest'):
        """Generate Secure EL3-monitor Image for STAGE2 (DYNAMIC LENGTH)

        if mode == 'imgmake', the file (from filename) will be used
        as a part of full structured Image, EL3 image.

        if mode == 'verify', the file (from filename) will be used
        as a full structured Image, SEL3 image. And checksum must be valid.

        :param filename: (str) Filename
        :param mode: (str) 'imgmake' or 'verify'
        :param version: (str) <NOT USED>
        :return: (obj) SEL3 object
        """
        with open(filename, 'rb') as (f):
            contents = f.read()
        hdr_length = ctypes.sizeof(stage2_stuff.Header)
        ctx_length = ctypes.sizeof(stage2_stuff.Context)
        sign_length = ctypes.sizeof(signature.Signature)
        img_length = len(contents) - hdr_length - ctx_length - sign_length

        class EL3(interface.Base):
            __doc__ = 'Secure EL3-monitor for STAGE2 <DYNAMIC LENGTH TYPE>\n\n            SEL3 size must be a multiple of 512\n            < (sizeof(SEL3) + 32) % 512 == 0 is True>\n            '
            _fields_ = (
             (
              'header', stage2_stuff.Header),
             (
              'image', ctypes.c_ubyte * img_length),
             (
              'context', stage2_stuff.Context),
             (
              'signature', signature.Signature))

        el3 = EL3()
        el3.set_from_binary(contents)
        if mode == 'imgmake':
            el3.header.num_of_sector = int(ctypes.sizeof(el3) / 512)
        return el3


if __name__ == '__main__':
    f = open('tes.sbl', 'r')
    img = f.read()
    f.close()
    bl = Factory.create_sbl1(len(img) - 1040)
    binary = bl.load('tes.sbl')
    print('done')