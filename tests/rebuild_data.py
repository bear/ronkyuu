# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2020 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.
"""
import json
import requests


path_testdata = './data/webmention_rocks_test'
test_data     = {}

def storePageData(pageURL, pageFilename):
    """Store the returned HTML as a file
    """
    r = requests.get(pageURL)
    with open('%s.html' % pageFilename, 'w') as h:
        h.write(r.text.encode('utf-8'))
    with open('%s.json' % pageFilename, 'w') as h:
        h.write(json.dumps(dict(r.headers), indent=2))


for n in range(1, 22):
    url   = 'https://webmention.rocks/test/%d' % n
    fname = '%s_%d' % (path_testdata, n)
    storePageData(url, fname)

storePageData('https://webmention.rocks/test/23/page', '%s_23' % path_testdata)
