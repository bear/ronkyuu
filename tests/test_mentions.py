# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2016 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.
"""

import json
import unittest
from urlparse import urlparse
from httmock import all_requests, response, HTTMock

from ronkyuu import findMentions, findEndpoint, discoverEndpoint

post_url  = "https://bear.im/bearlog/2013/325/indiewebify-and-the-new-site.html"
post_html = ''.join(open('./tests/data/mentions_post.html').readlines())

path_testdata = './tests/data/webmention_rocks_test_'
max_testdata  = 14
test_data     = {}
for n in range(1, max_testdata + 1):
    urlpath = 'webmention.rocks/test/%d' % n
    with open('%s%0d.html' % (path_testdata, n), 'r') as h:
        html = h.read()
    with open('%s%0d.json' % (path_testdata, n), 'r') as h:
        headers = json.load(h)
    test_data[urlpath] = { 'headers': headers, 'html': html }

# this dict only contains those items that have endpoints
# specified in the html and not in headers
endpoint_data = { 'webmention.rocks/test/3': '/test/3/webmention',
                  'webmention.rocks/test/4': 'https://webmention.rocks/test/4/webmention',
                  'webmention.rocks/test/5': '/test/5/webmention',
                  'webmention.rocks/test/6': 'https://webmention.rocks/test/6/webmention',
                }

@all_requests
def mock_response(url, request):
    if url.netloc == 'webmention.rocks':
        key = '%s%s' % (url.netloc, url.path)
        if key in test_data.keys():
            d = test_data[key]
            return response(200, d['html'], d['headers'])
    elif url.netloc == 'bear.im' and url.path == '/bearlog/2013/325/indiewebify-and-the-new-site.html':
        return response(200, post_html)
    else:
        return response(500)

class TestParsing(unittest.TestCase):
    # test the core mention and replies link finding
    def runTest(self):
        with HTTMock(mock_response):
            mentions = findMentions(post_url, exclude_domains=['bear.im'])
            assert len(mentions['refs']) > 0
            assert 'http://indiewebify.me/' in mentions['refs']

class TestEndpoint(unittest.TestCase):
    # run the html parsing for a discoverWebmentions result
    def runTest(self):
        for urlpath in test_data.keys():
            if urlpath in endpoint_data:
                endpoint = endpoint_data[urlpath]
                html     = test_data[urlpath]['html']

                href = findEndpoint(html)
                assert href == endpoint

class TestDiscovery(unittest.TestCase):
    def runTest(self):
        with HTTMock(mock_response):
            for urlpath in test_data.keys():
                url      = 'http://%s' % urlpath
                endpoint = urlparse('%s/webmention' % url).path

                rc, href, debug = discoverEndpoint(url, debug=True)

                wmUrl = urlparse(href)
                assert wmUrl.netloc == 'webmention.rocks'
                assert wmUrl.path   == endpoint
