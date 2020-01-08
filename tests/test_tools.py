# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2020 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.
"""

import unittest

from ronkyuu.tools import parse_link_header

class TestParseLinkRels(unittest.TestCase):
    def runTest(self):
        headers = ['</test/1/webmention>; rel=webmention',
                   '</test/1/webmention>; rel="webmention"',
                  ]
        for s in headers:
            d = parse_link_header(s)

        assert 'webmention' in d.keys()
