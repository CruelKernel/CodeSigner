# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/admin/spyrr/dev/dietsigner/src/pkg/diet_app.py
"""CodeSigner application module

This file defines CodeSigner application class.

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import logging, optparse as OPT, os, sys
from . import optparseex as OPTEX
from . import diet_stage as Stage
from . import settings
from . import testkeys
__version__ = '1'
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
__all__ = ('App', )
_conf = settings.Config()
_default = settings.Default()
_logger = logging.getLogger('CodeSigner')

class App:
    __doc__ = 'CodeSigner application class\n\n    This class is a super class for CodeSigner application class\n    '
    _OPTIONS = (
     ('key_id', 'store', '', 'string', '<key_id>', 'Lower case alphabet or number string only'),
     ('infile', 'store', None, 'string', '<filename>', 'Boot Loader(IMGMAKE Case), Signed Boot Loader(VERIFY Case)'),
     ('outfile', 'store', None, 'string', '<filename>', 'Signed Boot Loader(IMGMAKE Case), Boot Loader(VERIFY Case)'),
     (
      'sign_type', 'store', _default.common['SIGN_TYPE'], 'int', '<0-8>',
      '0~2: RSASSA-PSS 2048/3072/4096\n3~5: ECDSA NIST-P Curve 256/384/521\n6~8: ECDSA BrainPool Curve 256/384/512'),
     ('rb_count', 'store', 0, 'int', '<0-9000>', 'Rollback Count (default: 0)'),
     ('key_type', 'store', 0, 'int', '<0-9000>', 'Key type (default: 0)'),
     ('key_index', 'store', 0, 'int', '<0-9000>', 'Key Index (default: 0)'),
     ('dynamic_length', 'store', 'no', 'string', '<yes|no>', 'el3 image (yes), the others (no)'),
     ('export_pub', 'store', None, 'string', '<filename>', 'Export publickey for testing (ex: testkey)'),
     (
      'debug', 'store_true', False, '', '', OPT.SUPPRESS_HELP))

    def __init__(self):
        """Constructor of App class

        :return: N/A
        """
        _logger.debug('Run constructor of %s' % self)
        argv = sys.argv
        program_path = argv[0].split('\\' if os.name == 'nt' else '/')
        self.pname = program_path[(-1)]
        self._stage = None
        _conf.opt = self._option_parse(argv)
        _conf.opt.path = './'
        self._init_logger()

    def _init_logger(self):
        """Initialize logger

        :return: N/A
        """
        log = settings.Logging()
        fmt_name = 'debug' if _conf.opt.debug is True else 'default'
        level = logging.DEBUG if _conf.opt.debug is True else logging.INFO
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(logging.Formatter(fmt=(log.formatters[fmt_name]['format'])))
        _logger.addHandler(handler)
        _logger.setLevel(level)
        _logger.debug('Logger initialization was done.')
        _logger.debug(f"Logger: {fmt_name} mode")

    def run(self):
        """Run CodeSigner

        :return: program status
        """
        opt = _conf.opt
        if opt.infile is None or opt.outfile is None:
            if opt.export_pub is None:
                self.usage()
            else:
                filename = opt.export_pub + _default.common['PUBLICKEY_EXT']
                with open(filename, 'wb') as (f):
                    f.write(testkeys.publickey[opt.sign_type])
                    _logger.info(f"sign_type: {opt.sign_type}")
                    _logger.info(f"Publickey was saved. Check {filename}.")
                    return 0
        else:
            if opt.infile is None or opt.outfile is None:
                _logger.error('Please enter -infile and -outfile parameters.')
                self.usage()
            else:
                if opt.sign_type > 8 or opt.sign_type < 0:
                    _logger.error(f"Wrong sign_type: {opt.sign_type}")
                    self.usage()
                _logger.debug(f"Running parameter list: {sys.argv}")
                ret = -1
                self._print_input_options()
                if _conf.opt.dynamic_length == 'no':
                    stage = Stage.Stage2Static()
                else:
                    stage = Stage.Stage2Dynamic()
            ret = stage.imgmake()
            ret = ret if ret != 0 else stage.verify()
            if ret < 0:
                self.usage()
            else:
                _logger.info('All process was well done.')
        return ret

    def usage(self):
        self.parser.print_help()
        self._print_example(self.pname)
        sys.exit(-1)

    def _option_parse(self, args):
        """Register program options

        :param args: program arguments (not used)
        :return: opt data
        """
        usage = f"{self.pname} <OPTIONS>"
        pgm = self.pname
        self.parser = OPTEX.OptionParser(usage=usage,
          option_class=(OPTEX.Option),
          formatter=OPT.IndentedHelpFormatter(max_help_position=84,
          width=100))
        group = OPT.OptionGroup(self.parser, 'Options', pgm)
        for _dest, _action, _default, _type, _metavar, _help in self._OPTIONS:
            if _type == '':
                group.add_option('',
                  ('-' + _dest), action=_action, default=_default, dest=_dest,
                  help=_help)
            else:
                group.add_option('',
                  ('-' + _dest), action=_action, default=_default, dest=_dest,
                  help=_help,
                  type=_type,
                  metavar=_metavar)

        self.parser.add_option_group(group)
        return self.parser.parse_args()[0]

    def _print_input_options(self):
        """Print entered options

        :return: N/A
        """
        opt = _conf.opt
        _logger.info(f"sign_type: {opt.sign_type}")
        _logger.info(f"key_id: {opt.key_id}")
        _logger.info(f"infile: {opt.infile}")
        _logger.info(f"outfile: {opt.outfile}")
        _logger.info(f"rb_count: {opt.rb_count}")
        _logger.info(f"key_index: {opt.key_index}")
        _logger.info(f"key_type: {opt.key_type}")
        _logger.info(f"dynamic_length: {opt.dynamic_length}")

    def _print_example(self, pname):
        """Pring example usage of this program

        :param pname: program name
        :return: N/A
        """
        sys.stderr.write(f"\n            \r* sign_type option:\n            \r  0~2: RSASSA-PSS 2048/3072/4096\n            \r  3~5: ECDSA NIST 256/384/521\n            \r  6~8: ECDSA BRAINPOOL 256/384/512\n\n            \rExamples:\n            \r  {pname} -infile bl2.img -outfile sbl2.img -sign_type 0 -key_type 0 -key_index 11 -rb_count 0 -dynamic_length no (-path ./)\n            \r")