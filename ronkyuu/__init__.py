#/usr/bin/env python

VERSION = (0, 2, 11, '')

__author__    = 'Mike Taylor'
__contact__   = 'bear@bear.im'
__copyright__ = 'Copyright (c) 2013-2014 by Mike Taylor and Kartik Prabhu'
__license__   = 'MIT'
__version__   = '.'.join(map(str, VERSION[0:3])) + ''.join(VERSION[3:])


from tools import discoverConfig
from webmention import findMentions, findEndpoint, discoverEndpoint, sendWebmention
from relme import findRelMe, confirmRelMe
from validators import URLValidator
