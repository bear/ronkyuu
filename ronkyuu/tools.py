#!/usr/bin/env python

"""
:copyright: (c) 2013-2015 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import os
import sys
import json
import re
from urlparse import urlsplit, urlunsplit

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

def parse_link_header(link):
    """takes the link header as a string and returns a dictionary with rel values as keys and urls as values
    :param link: link header as a string
    :rtype: dictionary {rel_name: rel_value}
    """
    rel_dict = {}
    for rels in link.split(','):
        rel_break = rels.split(';')
        try:
            rel_url = re.search('<(.+?)>', rel_break[0]).group(1)
            rel_names = re.search('rel="(.+?)"', rel_break[1]).group(1)
            for name in rel_names.split():
                rel_dict[name] = rel_url
        except (AttributeError, IndexError):
            pass

    return rel_dict

