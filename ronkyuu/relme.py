# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2016 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Rel=Me Tools
"""

from .tools import normalizeURL, cleanURL

import requests
from bs4 import BeautifulSoup

try:  # Python v3
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


_html_parser = 'html5lib'   # 'html.parser', 'lxml', 'lxml-xml'


# see http://microformats.org/wiki/rel-me for the spec
#
# With a profile URL http://bear.im and a resource URL http://twitter.com/bear
# is the resource an authoritative relme of the profile?
#
#   within the profile URL the following rel="me" links appear
#     <a href="http://twitter.com/bear" rel="me">@bear</a>
#     <a href="https://github.com/bear" rel="me" class="u-url">GitHub</a>
#
#   within the resource URL the following rel="me" links appear
#     <a target="_blank" rel="me nofollow" href="https://t.co/ZK4BFjSq66" class="js-tooltip" title="https://bear.im">bear.im</a>
#   and redirects
#     https://t.co/ZK4BFjSq66 -> [301] -> https://bear.im
#
#   The answer would be yes because the normalized resource relme link matches our profile URL
#
# With a profile URL http://dreev.es and a resource URL https://twitter.com/dreev
# is the resource an authoritative relme of the profile?
#
#   The profile URL itself redirects:
#       http://dreev.es -> [301] -> http://ai.eecs.umich.edu/people/dreeves/
#     and contains the following rel="me" links:
#       <a href="https://twitter.com/dreev" rel="me"/>
#
#   The resource URL has the following rel="me" links
#       <a target="_blank" rel="me nofollow" href="https://t.co/PlBCqLVndT" class="js-tooltip" title="http://dreev.es</a>
#     and redirects
#       http://t.co/PlBCqLVndT -> [301] -> http://dreev.es -> [301] -> http://ai.eecs.umich.edu/people/dreeves/
#
#   The answer would be yes because the normalized profile URL matches the normalized resource relme link
#
#   Other questions:
#     would it also be yes because the given profile URL matches one of the resource relme link's redirect chain urls?
#     do we then consider it as authorative if the chain segments match for the redirect?
#     i.e.
#                                                                              http://dreev.es -> [301] -> http://ai.eecs.umich.edu/people/dreeves/
#  https://twitter.com/dreev -> [rel-me] -> http://t.co/PlBCqLVndT -> [301] -> http://dreev.es -> [301] -> http://ai.eecs.umich.edu/people/dreeves/
#


def findRelMe(sourceURL):
    """Find all <a /> elements in the given html for a post.

    If any have an href attribute that is rel="me" then include
    it in the result.

    :param sourceURL: the URL for the post we are scanning
    :rtype: dictionary of RelMe references
    """
    r = requests.get(sourceURL)
    result = {'status':  r.status_code,
              'headers': r.headers,
              'history': r.history,
              'content': r.text,
              'relme':   [],
              'url':     sourceURL
              }
    if r.status_code == requests.codes.ok:
        dom = BeautifulSoup(r.text, _html_parser)
        for link in dom.find_all('a', rel='me'):
            rel  = link.get('rel')
            href = link.get('href')
            if rel is not None and href is not None:
                url = urlparse(href)
                if url is not None and url.scheme in ('http', 'https'):
                    result['relme'].append(cleanURL(href))
    return result


def confirmRelMe(profileURL, resourceURL, profileRelMes=None, resourceRelMes=None):
    """Determine if a given :resourceURL: is authoritative for the :profileURL:

    TODO add https/http filtering for those who wish to limit/restrict urls to match fully
    TODO add code to ensure that each item in the redirect chain is authoritative

    :param profileURL: URL of the user
    :param resourceURL: URL of the resource to validate
    :param profileRelMes: optional list of rel="me" links within the profile URL
    :param resourceRelMes: optional list of rel="me" links found within resource URL
    :rtype: True if confirmed
    """
    result  = False
    profile = normalizeURL(profileURL)

    if profileRelMes is None:
        profileRelMe = findRelMe(profileURL)
        profileRelMes = profileRelMe['relme']
    if resourceRelMes is None:
        resourceRelMe = findRelMe(resourceURL)
        resourceRelMes = resourceRelMe['relme']

    for url in resourceRelMes:
        if profile in (url, normalizeURL(url)):
            result = True
            break

    return result
