# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.5 (default, Aug 12 2020, 00:00:00) 
# [GCC 10.2.1 20200723 (Red Hat 10.2.1-1)]
# Embedded file name: /home/spyrr/dev/cslv/src/cslv.py
"""DietSigner entry point

Copyright (c) Samsung Electronics Co., Ltd. All rights reserved.
"""
import sys, pkg.diet_app
__author__ = 'Lee, Hosub <hosub7.lee@samsung.com>'
__version__ = '5'
__copyright__ = f"_________            .___       _________.__\n\\_   ___ \\  ____   __| _/____  /   _____/|__| ____   ____   ___________\n/    \\  \\/ /  _ \\ / __ |/ __ \\ \\_____  \\ |  |/ ___\\ /    \\_/ __ \\_  __ \\\n\\     \\___(  <_> ) /_/ \\  ___/ /        \\|  / /_/  >   |  \\  ___/|  | \\/\n \\______  /\\____/\\____ |\\___  >_______  /|__\\___  /|___|  /\\___  >__|\n        \\/            \\/    \\/        \\/   /_____/      \\/     \\/\n+----------------------------------------------------------------------+\n| Copyright (c) SAMSUNG Electronics Co., Ltd. All rights reserved.     |\n| This software is a confidential stuff and proprietary of             |\n| SAMSUNG Electronics Co., Ltd.                                        |\n| So you shall not disclose this software other company or persons     |\n| without permission of SAMSUNG and shall use this software only       |\n| in accordance with the license agreement of SAMSUNG.                 |\n+----------------------------------------------------------------------+\nCodeSigner Lite Version {__version__} for SAMSUNG Processors\n"

def main():
    """The entry point of DietSigner

    This function run the main

    :return: return value of application
    """
    return pkg.diet_app.App().run()


if __name__ == '__main__':
    print(__copyright__)
    sys.exit(main())