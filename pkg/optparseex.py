# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/pkg/optparseex.py
"""optparse library extension

We re-define some classes of optparse library to use long type options
formed "-option" instead of "-o".

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.

Version History:
    Version 1, 2013.10.31., Lee, Hosub
        - optparse uses '-' for CodeSigner instead of '--'
"""
import optparse
__all__ = ('Option', 'OptionParser')
__version__ = '1'
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'

class Option(optparse.Option):

    def __init__(self, *opts, **attrs):
        self._short_opts = []
        self._long_opts = []
        opts = self._check_opt_strings(opts)
        self._set_opt_strings(opts)
        self._set_attrs(attrs)
        for checker in self.CHECK_METHODS:
            checker(self)

    def _set_opt_strings(self, opts):
        for opt in opts:
            if len(opt) < 2:
                msg = 'invalid option string %r: must be at least two characters long' % opt
                raise optparse.OptionError(msg, self)
            else:
                if not (opt[0] == '-' and opt[1] != '-'):
                    msg = 'invalid long option string %r: must start with--, followed by non-dash' % opt
                    raise optparse.OptionError(msg, self)
                self._long_opts.append(opt)


class OptionParser(optparse.OptionParser):

    def __init__(self, usage=None, option_list=None, option_class=Option, version=None, conflict_handler='error', description=None, formatter=None, add_help_option=True, prog=None, epilog=None):
        optparse.OptionParser.__init__(self, usage, option_list, option_class, version, conflict_handler, description, formatter, add_help_option, prog, epilog)

    def _add_help_option(self):
        self.add_option('-h',
          '-help', action='help', help='show this help message and exit')

    def _add_version_option(self):
        self.add_option('-v',
          '-version', action='version', help='show program`s version number and exit')

    def _check_conflict(self, option):
        conflict_opts = []
        for opt in option._long_opts:
            if opt in self._long_opt:
                conflict_opts.append((opt, self._long_opt[opt]))

        if conflict_opts:
            handler = self.conflict_handler
            if handler == 'error':
                msg = 'conflicting option string(s): %s'
                msg %= ', '.join([co[0] for co in conflict_opts])
                raise optparse.OptionConflictError(msg, option)
            elif handler == 'resolve':
                for opt, c_option in conflict_opts:
                    if opt.startswith('-'):
                        c_option._long_opts.remove(opt)
                        del self._long_opt[opt]

    def _process_args(self, largs, rargs, values):
        while rargs:
            arg = rargs[0]
            if arg == '--':
                del rargs[0]
                return
            if arg[:1] == '-':
                if len(arg) > 1:
                    self._process_long_opt(rargs, values)
            if self.allow_interspersed_args:
                largs.append(arg)
                del rargs[0]
            else:
                return