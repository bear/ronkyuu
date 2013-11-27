#/usr/bin/env python

VERSION = (0, 1, 0, "alpha")

__author__    = 'Mike Taylor'
__contact__   = 'bear@bear.im'
__copyright__ = 'Copyright (c) by Mike Taylor'
__license__   = 'MIT'
__version__   = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])

from webmention import iwPost