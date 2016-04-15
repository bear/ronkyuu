# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2016 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.
"""

import unittest
from httmock import all_requests, HTTMock

from ronkyuu import findRelMe, confirmRelMe
from ronkyuu.tools import cleanURL


profile_url  = cleanURL("https://bear.im")
redirect_url = cleanURL("http://code-bear.com")
twitter_url  = cleanURL("https://twitter.com/bear")
t_co_url     = cleanURL('https://t.co/ZK4BFjSq66')
other_url    = cleanURL("https://tantek.com")

profile_html = ''.join(open('./tests/data/relme_bear.html').readlines())
twitter_html = ''.join(open('./tests/data/relme_twitter_bear.html').readlines())
other_html   = ''.join(open('./tests/data/relme_tantek.html').readlines())

@all_requests
def _mock(url, request):
    if 'code-bear.com' in url:
        return profile_html
    if 'bear.im' in url:
        return profile_html
    if 'twitter.com' in url:
        return twitter_html
    return other_html

class TestProfileURLParsing(unittest.TestCase):
    def runTest(self):
        with HTTMock(_mock):
            relme = findRelMe(profile_url)
            assert len(relme['relme']) > 0
            assert profile_url in relme['relme']

class TestTargetURLParsing(unittest.TestCase):
    def runTest(self):
        with HTTMock(_mock):
            relme = findRelMe(twitter_url)
            assert len(relme['relme']) > 0
            assert t_co_url in relme['relme']

class TestInvalidRelMeSimple(unittest.TestCase):
    def runTest(self):
        with HTTMock(_mock):
            relmeProfile = findRelMe(profile_url)
            relmeOtherProfile = findRelMe(other_url)
            assert not confirmRelMe(profile_url, other_url, relmeProfile['relme'], relmeOtherProfile['relme'])

# class TestConfirmRelMeSimple(unittest.TestCase):
#     """Test a relme case where the resource URL directly maps
#     to the profile URL's relme list
#     """
#     def runTest(self):
#         with HTTMock(_mock):
#             relmeProfile = findRelMe(profile_url)
#             relmeTarget  = findRelMe(twitter_url)

#             assert confirmRelMe(profile_url, twitter_url, relmeProfile['relme'], relmeTarget['relme'])

# class TestConfirmRelMeRedirect(unittest.TestCase):
#     """Test a relme case where the resource URL in-directly maps
#     to the profile URL's relme list because the profile URL itself
#     is a redirect.
#     """
#     def runTest(self):
#         with HTTMock(_mock):
#             relmeProfile = findRelMe(redirect_url)
#             relmeTarget  = findRelMe(twitter_url)

#             assert confirmRelMe(profile_url, twitter_url, relmeProfile['relme'], relmeTarget['relme'])
