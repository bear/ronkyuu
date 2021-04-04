# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2020 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.
"""
import json
import unittest
from urllib.parse import urlparse
from httmock import all_requests, response, HTTMock
from ronkyuu import findMentions, findEndpoint, discoverEndpoint, sendWebmention


post_url  = "https://bear.im/bearlog/2013/325/indiewebify-and-the-new-site.html"
post_html = ''.join(open('./tests/data/mentions_post.html').readlines())

path_testdata = './tests/data/webmention_rocks_test_'
max_testdata  = 22
test_data     = {}
for n in range(1, max_testdata + 1):
    with open('%s%0d.html' % (path_testdata, n), 'r') as h:
        html = h.read()
    with open('%s%0d.json' % (path_testdata, n), 'r') as h:
        headers = json.load(h)
    test_data['webmention.rocks/test/%d' % n] = {'headers': headers, 'html': html}

# this dict only contains those items that have endpoints
# specified in the html and not in headers
html_endpoints = {
    'webmention.rocks/test/3': '/test/3/webmention',
    'webmention.rocks/test/4': 'https://webmention.rocks/test/4/webmention',
    'webmention.rocks/test/5': '/test/5/webmention',
    'webmention.rocks/test/6': 'https://webmention.rocks/test/6/webmention',
}
odd_endpoints = {
    'webmention.rocks/test/15': 'https://webmention.rocks/test/15',
    'webmention.rocks/test/21': 'https://webmention.rocks/test/21/webmention?query=yes',
}


@all_requests
def mock_response(url, request):  # pylint: disable=unused-argument
    if url.netloc == 'webmention.rocks':
        key = '%s%s' % (url.netloc, url.path)
        if key in test_data.keys():
            d = test_data[key]
            return response(200, d['html'], d['headers'])
    elif url.netloc == 'bear.im' and url.path == '/bearlog/2013/325/indiewebify-and-the-new-site.html':
        return response(200, post_html)
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
        for urlpath in test_data:
            if urlpath in html_endpoints:
                endpoint = html_endpoints[urlpath]
                pagedata = test_data[urlpath]['html']

                href = findEndpoint(pagedata)
                assert href == endpoint


class TestDiscovery(unittest.TestCase):
    def runTest(self):
        with HTTMock(mock_response):
            for urlpath in test_data:
                url = 'http://%s' % urlpath
                if urlpath in odd_endpoints:
                    endpoint = odd_endpoints.get(urlpath)
                else:
                    endpoint = '%s/webmention' % url

                retCode, href  = discoverEndpoint(url)

                wmUrl = urlparse(href)
                endpoint = urlparse(endpoint)

                assert retCode      == 200
                assert wmUrl.netloc == 'webmention.rocks'
                assert wmUrl.path   == endpoint.path
                assert wmUrl.query  == endpoint.query


class TestDiscoveryRedirect(unittest.TestCase):
    def runTest(self):
        retCode, href = discoverEndpoint('https://webmention.rocks/test/23/page')
        wmUrl = urlparse(href)

        assert retCode      == 200
        assert wmUrl.netloc == 'webmention.rocks'
        assert wmUrl.path.startswith('/test/23/webmention-endpoint/')


class TestSendMention(unittest.TestCase):
    def runTest(self):
        source = 'https://bear.im/bearlog/2017/245/checking-indieweb-code'
        target = 'https://webmention.rocks/test/23/page'

        resp = sendWebmention(source, target, test_urls=False)

        assert resp.status_code == 200
