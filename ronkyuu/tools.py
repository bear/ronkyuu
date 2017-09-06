# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2016 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import os
import re
import json
import shlex

try:  # Python v3
    from urllib.parse import urlsplit, urlunsplit
except ImportError:
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
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError, requests.exceptions.URLRequired,
            requests.exceptions.TooManyRedirects, requests.exceptions.Timeout):
        ok = False
    return (ok, chain)

def cleanURL(targetURL):
    scheme, netloc, path, query, fragment = urlsplit(targetURL)
    if len(path) == 0:
        path = '/'
    return urlunsplit((scheme, netloc, path, query, fragment))

def normalizeURL(targetURL):
    result = None
    ok, chain = getURLChain(targetURL)
    if ok:
        if len(chain) > 0:
            result = chain[-1]
        else:
            result = targetURL
    return result

def quoted_split(text, boundary):
    o = shlex.shlex(text)
    o.whitespace = boundary
    o.whitespace_split = True
    return list(o)

def parse_link_header(link):
    """takes the link header as a string and returns a dictionary with rel values as keys and urls as values
    :param link: link header as a string
    :rtype: dictionary {rel_name: rel_value}
    """
    rel_dict = {}
    for rels in link.split(','):
        rel_break = quoted_split(rels, ';')
        try:
            rel_url = re.search('<(.+?)>', rel_break[0]).group(1)
            rel_names = quoted_split(rel_break[1], '=')[-1]
            if rel_names.startswith('"') and rel_names.endswith('"'):
                    rel_names = rel_names[1:-1]
            for name in rel_names.split():
                rel_dict[name] = rel_url
        except (AttributeError, IndexError):
            pass

    return rel_dict
