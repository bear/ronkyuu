#!/usr/bin/env python

import unittest

from ronkyuu import Events


post_url     = "https://bear.im/bearlog/2013/325/indiewebify-and-the-new-site.html"
tantek_url   = "http://tantek.com/2013/322/b1/homebrew-computer-club-reunion-inspiration"
event_config = { "handler_path": "./tests/test_event_handlers",
                    
               }

class TestEventConfig(unittest.TestCase):
    def runTest(self):
        events = Events(config=event_config)

        assert events is not None
        assert len(events.handlers) > 0
        assert 'event_test_handler' in events.handlers

class TestEvents(unittest.TestCase):
    def runTest(self):
        events = Events(config=event_config)

        events.inboundWebmention(tantek_url, post_url)
        assert events.handlers['event_test_handler'].test_results['inbound'] == post_url

        events.outboundWebmention(tantek_url, post_url)
        assert events.handlers['event_test_handler'].test_results['outbound'] == post_url

        events.postArticle(post_url)
        assert events.handlers['event_test_handler'].test_results['post'] == post_url
