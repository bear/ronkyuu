# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2016 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.
"""

__author__       = 'Mike Taylor and Kartik Prabhu'
__email__        = 'bear@bear.im'
__copyright__    = 'Copyright (c) 2013-2016 by Mike Taylor and Kartik Prabhu'
__license__      = 'MIT'
__version__      = '0.6'
__url__          = 'https://github.com/bear/ronkyuu'
__download_url__ = 'https://pypi.python.org/pypi/ronkyuu'
__description__  = 'Webmention Manager'

from .tools import discoverConfig                                                                # noqa
from .webmention import setParser, findMentions, findEndpoint, discoverEndpoint, sendWebmention  # noqa
from .relme import findRelMe, confirmRelMe                                                       # noqa
from .validators import URLValidator                                                             # noqa
