# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/settings.py
"""CodeSigner Configuration

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.

Version History:
    Version 2, 2015.06.31., Lee, Hosub
        - Added configuration for logging module
    version 3, 2017.12.26., Lee, Hosub
        - Split Config class and re-define it
"""
import logging, os
__all__ = ('Config', 'Default', 'Logging', 'SignType')
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
__version__ = '3'

class Singleton(object):
    __doc__ = 'Singleton class'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = (object.__new__)(cls, *args, **kwargs)
        return cls._instance


class Config(Singleton):
    __doc__ = 'Config class\n\n    This class inherited Singleton class to use this as a global variable.\n    Singleton: refer GoF design pattern.\n    '
    pkcs11 = {'enable':False, 
     'token_label':'Default', 
     'user_pin':'', 
     'lib_path':'/opt/nfast/toolkits/pkcs11/libcknfast.so', 
     'CKNFAST_FAKE_ACCELERATOR_LOGIN':'true', 
     'CKNFAST_LOADSHARING':'1', 
     'CKNFAST_DEBUG':'6', 
     'PKCS11_TOKEN_LABEL':'exynos_codesigner', 
     'PKCS11_TOKEN_PIN':''}
    opt = None

    def is_pkcs11_enabled(self) -> bool:
        return self.pkcs11['enable']


class Default(Singleton):
    common = {'PRIVATEKEY_EXT':'.privatekey', 
     'PUBLICKEY_EXT':'.publickey', 
     'EFUSEDATA_EXT':'.efuse', 
     'PATH':'./', 
     'SIGN_TYPE':0}
    stage1 = {'SBL1_SIZE_WITHOUT_BL':2368, 
     'ENADDR':0, 
     'CODESIGNER_VER':5, 
     'APINFO':1230195795, 
     'KEY_INDEX':0, 
     'DESCRIPTION':b'\x00' * 36}
    stage2 = {'BL2_MAGIC_MARK': b'daeh'}
    aes = {'PRIVATEKEY_ENCRYPTION':{'KEY':b'\xc0\xa2\x02g\xf9\xf1\xe4F\x9f\x8e\xb7\xbfEpB\x18)4\x12\xdbJo]\xa9\xdf\xd9dB\xcd\xff\x84\xe0', 
      'INITIAL_VECTOR':b'>\xc4\xc2\x80\x03\x8fW)\x0b\xd7\xce\x97\xb7aov'}, 
     'SBL_encryption':{}}


class Logging(Singleton):
    version = 1
    formatters = {'default':{'format': '[*] %(message)s'}, 
     'debug':{'format': '[%(levelname)-8s][%(filename)s:%(lineno)s] %(funcName)s():   %(message)s'}}
    handlers = {'default':{'class':'logging.StreamHandler', 
      'formatter':'default', 
      'level':logging.INFO}, 
     'debug':{'class':'logging.StreamHandler', 
      'formatter':'debug', 
      'level':logging.DEBUG}}
    loggers = {'root':{'handlers':[
       'default'], 
      'level':logging.INFO}, 
     'debug':{'handlers':[
       'debug'], 
      'level':logging.DEBUG}}


class SignType(Singleton):
    __doc__ = 'SignType class\n\n    Map the data from sign_type parameter\n\n    RSASSA-PSS: index 0 ~ 2\n    ECDSA-NISTP: index 3 ~ 5\n    ECDSA-BRAINPOOLP: index 6 ~ 8\n    '
    algorithm_list = ('RSASSA-PSS', 'ECDSA')
    map = (
     {'algorithm':'RSASSA-PSS', 
      'bit':2048,  'byte':256},
     {'algorithm':'RSASSA-PSS', 
      'bit':3072,  'byte':384},
     {'algorithm':'RSASSA-PSS', 
      'bit':4096,  'byte':512},
     {'algorithm':'ECDSA', 
      'curve':'NIST',  'bit':256,  'byte':68},
     {'algorithm':'ECDSA', 
      'curve':'NIST',  'bit':384,  'byte':68},
     {'algorithm':'ECDSA', 
      'curve':'NIST',  'bit':521,  'byte':68},
     {'algorithm':'ECDSA', 
      'curve':'BrainPoolTwisted',  'bit':256,  'byte':68},
     {'algorithm':'ECDSA', 
      'curve':'BrainPoolTwisted',  'bit':384,  'byte':68},
     {'algorithm':'ECDSA', 
      'curve':'BrainPoolTwisted',  'bit':512,  'byte':68})
    start = {'RSASSA-PSS':0, 
     'ECDSA':3}
    end = {'RSASSA-PSS':3,  'ECDSA':12}

    def get_algorithm(self, _type):
        return self.map[_type]['algorithm']

    def get_bit(self, _type):
        return self.map[_type]['bit']

    def get_key_size(self, _type):
        return self.get_bit(_type)

    def get_curve(self, _type):
        if _type < 3:
            return
        else:
            return self.map[_type]['curve']

    def get_byte(self, _type):
        return self.map[_type]['byte']

    @staticmethod
    def is_rsa(_type):
        start = SignType.start['RSASSA-PSS']
        end = SignType.end['RSASSA-PSS']
        if start <= _type < end:
            return True
        else:
            return False

    @staticmethod
    def is_ecdsa(_type):
        start = SignType.start['ECDSA']
        end = SignType.end['ECDSA']
        if start <= _type < end:
            return True
        else:
            return False


class ColorSet(Singleton):
    _fg = {}
    _bg = {}

    def __init__(self):
        Singleton.__init__(self)
        self._set_colors()

    def _set_colors(self):
        try:
            if os.environ['TERM'].lower() in ('xterm', 'xterm-256color'):
                self._fg['gray'] = '\x1b[1;30m'
                self._fg['red'] = '\x1b[1;31m'
                self._fg['green'] = '\x1b[1;32m'
                self._fg['yellow'] = '\x1b[1;33m'
                self._fg['blue'] = '\x1b[1;34m'
                self._fg['pupple'] = '\x1b[1;35m'
                self._fg['aqua'] = '\x1b[1;36m'
                self._fg['white'] = '\x1b[1;37m'
                self._fg['default'] = '\x1b[0m'
                self._bg['dark gray'] = '\x1b[100m'
                self._bg['red'] = '\x1b[41m'
                self._bg['black'] = '\x1b[40m'
                self._bg['default'] = '\x1b[49m'
        except KeyError:
            pass

    def fg(self, color: str):
        if color not in self._fg:
            return ''
        else:
            return self._fg[color]

    def bg(self, color: str):
        if color not in self._bg:
            return ''
        else:
            return self._bg[color]