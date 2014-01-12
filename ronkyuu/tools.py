#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import os, sys
import json


cfgFilenames = ('ronkyuu.cfg', '.ronkyuu.cfg')
cfgFilepaths = (os.getcwd(), '~/', '~/.ronkyuu/')

possibleConfigFiles = []

for p in cfgFilepaths:
    for f in cfgFilenames:
        possibleConfigFiles.append(os.path.join(p, f))

def discoverConfig(cfgFilename=None):
    result = {}

    if cfgFilename is None:
        for possibleFile in possibleConfigFiles:
            possibleFile = os.path.expanduser(possibleFile)
            if os.path.exists(possibleFile):
                result = json.load(open(possibleFile, 'r'))
                break
    else:
        possibleFile = os.path.expanduser(cfgFilename)
        if os.path.exists(possibleFile):
            result = json.load(open(possibleFile, 'r'))

    return result
