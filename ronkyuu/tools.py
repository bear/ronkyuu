#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import os
import sys
import json

import requests


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


def getURLChain(targetURL):
    ok = False
    chain = []
    try:
        r = requests.head(targetURL, allow_redirects=True)
        ok = r.status_code == requests.codes.ok
        if ok:
            for resp in r.history:
                chain.append(r.url)
    except:
        ok = False
    return (ok, chain)


def normalizeURL(targetURL):
    result = None
    ok, chain = getURLChain(targetURL)
    if ok:
        if len(chain) > 0:
            result = chain[-1]
        else:
            result = targetURL
    return result
