# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2016 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.
"""

import os
import unittest
from httmock import urlmatch, HTTMock

from ronkyuu import findMentions, findEndpoint, discoverEndpoint


post_url    = "https://bear.im/bearlog/2013/325/indiewebify-and-the-new-site.html"
tantek_url  = "http://tantek.com/2013/322/b1/homebrew-computer-club-reunion-inspiration"
post_html   = ''.join(open('./tests/data/mentions_post.html').readlines())
tantek_html = ''.join(open('./tests/data/mentions_tantek.html').readlines())

path_testdata = './tests/data/'

html = {}
for n in range(0, 4):
    f       = 'mentions_link_in_head_%02d.html' % n
    html[f] = []
    with open(os.path.join(path_testdata, f), 'r') as h:
        html[f].append(h.read())

with open(os.path.join(path_testdata, 'mentions_empty.html'), 'r') as h:
    empty_html = h.read()

@urlmatch(netloc=r'(.*\.)?ronkyuu\.io$')
def link_mock(url, request):
    return post_html

@urlmatch(netloc=r'(.*\.)?bear\.im$')
def bear_im_mock(url, request):
    return post_html

class TestParsing(unittest.TestCase):
    # test the core mention and replies link finding
    def runTest(self):
        with HTTMock(bear_im_mock):
            mentions = findMentions(post_url, exclude_domains=['bear.im'])
            assert len(mentions['refs']) > 0
            assert 'http://indiewebify.me/' in mentions['refs']
            assert tantek_url in mentions['refs']

class TestEndpoint(unittest.TestCase):
    # run the html parsing for a discoverWebmentions result using a stored
    # GET from one of Tantek's posts
    def runTest(self):
        assert findEndpoint(tantek_html) == 'http://webmention.io/tantek.com/webmention'

@urlmatch(netloc=r'(.*\.)?tantek\.com$')
def tantek_mock(url, request):
    return tantek_html

class TestDiscovery(unittest.TestCase):
    def runTest(self):
        with HTTMock(tantek_mock):
            result = discoverEndpoint(tantek_url)

            assert result[1] == 'http://webmention.io/tantek.com/webmention'
