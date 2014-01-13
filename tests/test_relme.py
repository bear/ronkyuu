#!/usr/bin/env python

import unittest
from httmock import urlmatch, HTTMock

from ronkyuu import findRelMe, confirmRelMe


profile_url = "https://bear.im"
twitter_url = "https://twitter.com/bear"
other_url   = "https://tantek.com"

profile_html = ''.join(open('./tests/data/relme_bear.html').readlines())
twitter_html = ''.join(open('./tests/data/relme_twitter_bear.html').readlines())
other_html   = ''.join(open('./tests/data/relme_tantek.html').readlines())

@urlmatch(netloc=r'(.*\.)?bear\.im$')
def bear_im_mock(url, request):
    return profile_html

@urlmatch(netloc=r'(.*\.)?twitter\.com$')
def twitter_mock(url, request):
    return twitter_html

@urlmatch(netloc=r'(.*\.)?tantek\.com$')
def other_mock(url, request):
    return other_html

class TestProfileURLParsing(unittest.TestCase):
    def runTest(self):
        with HTTMock(bear_im_mock):
            relme = findRelMe(profile_url)
            assert len(relme['relme']) > 0
            assert 'https://bear.im' in relme['relme']

class TestTargetURLParsing(unittest.TestCase):
    def runTest(self):
        with HTTMock(twitter_mock):
            relme = findRelMe(twitter_url)
            assert len(relme['relme']) > 0
            assert 'https://t.co/ZK4BFjSq66' in relme['relme']

class TestConfirmRelMe(unittest.TestCase):
    def runTest(self):
        with HTTMock(bear_im_mock):
            relmeProfile = findRelMe(profile_url)
            assert len(relmeProfile['relme']) > 0
            assert 'https://bear.im' in relmeProfile['relme']

        with HTTMock(twitter_mock):
            relmeTarget = findRelMe(twitter_url)
            assert len(relmeTarget['relme']) > 0
            assert 'https://t.co/ZK4BFjSq66' in relmeTarget['relme']

        with HTTMock(other_mock):
            relmeOtherProfile = findRelMe(other_url)
            assert len(relmeOtherProfile['relme']) > 0
            assert 'https://twitter.com/t' in relmeOtherProfile['relme']

        assert confirmRelMe(profile_url, twitter_url, relmeProfile['relme'], relmeTarget['relme'])
        assert not confirmRelMe(profile_url, other_url, relmeProfile['relme'], relmeOtherProfile['relme'])