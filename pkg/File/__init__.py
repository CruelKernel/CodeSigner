# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/File/__init__.py
"""CodeSigner file structures

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import logging
from . import boot_loader
from . import privatekey
from . import publickey
__all__ = ('boot_loader', 'Factory', 'Structure', 'privatekey', 'publickey')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
_logger = logging.getLogger('CodeSigner')

class Factory:
    __doc__ = 'Factory class for Secure Boot Data Structures'

    @staticmethod
    def create_sbl1(filename, mode='imgmake', version='lastest'):
        """Generate Secure Boot Image for STAGE1

        :param filename: (str) Filename
        :param mode: (str) 'imgmake' or 'verify'
        :param version: (str) <NOT USED>
        :return: (obj) SBL1 object
        """
        _logger.debug('[FACTORY] SBL1 was generated')
        return boot_loader.Factory.create_sbl1(filename, mode, version)

    @staticmethod
    def create_sbl2(filename, version='latest'):
        """Generate Secure Boot Image for STAGE2 (Fixed length image)

        :param filename: (str) filename
        :param version: (str) <NOT USED>
        :return: (obj) SBL2
        """
        _logger.debug('[FACTORY] SBL2 was generated')
        return boot_loader.Factory.create_sbl2(filename, version)

    @staticmethod
    def create_el3(filename, version='latest'):
        """Generate Secure EL3-monitor Image for STAGE2 (Fixed length image)

        :param filename: (str) filename
        :param version: (str) <NOT USED>
        :return: (obj) SEL3
        """
        _logger.debug('[FACTORY] SEL3 was generated')
        return boot_loader.Factory.create_el3(filename, version)

    @staticmethod
    def create_ecc_privatekey_file(version='latest'):
        """Generate ECC private key file image

        :param version: (str) <NOT USED>
        :return: (obj) ECC object (pkg/structure/file/privatekey)
        """
        _logger.debug('[FACTORY] ECC PrivateKey File was generated')
        return privatekey.Factory.create('ecc')

    @staticmethod
    def create_rsa_privatekey_file(version='latest'):
        """Generate RSA private key file image

        :param version: (str) <NOT USED>
        :return: (obj) RSA object (pkg/structure/file/privatekey)
        """
        _logger.debug('[FACTORY] RSA PrivateKey File was generated')
        return privatekey.Factory.create('rsa')

    @staticmethod
    def create_ecc_publickey_file(version='latest'):
        """Generate ECC public key file image

        :param version: (str) <NOT USED>
        :return: (obj) ECC object (pkg/structure/file/publickey)
        """
        _logger.debug('[FACTORY] ECC PublicKey File was generated')
        return publickey.Factory.create('ecc')

    @staticmethod
    def create_rsa_publickey_file(version='latest'):
        """Generate RSA public key file image

        :param version: (str) <NOT USED>
        :return: (obj) RSA object (pkg/structure/file/publickey)
        """
        _logger.debug('[FACTORY] RSA PublicKey File was generated')
        return publickey.Factory.create('rsa')


if __name__ == '__main__':
    f = open('tes.sbl', 'r')
    img = f.read()
    f.close()
    bl = Factory.create_sbl1(len(img) - 1040)
    binary = bl.load('tes.sbl')
    print('done')