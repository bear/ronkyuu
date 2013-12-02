#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import argparse
import requests
import ronkyuu

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('sourceURL')

    args = parser.parse_args()

    print('Scanning %s for mentions' % args.sourceURL)

    mentions = ronkyuu.findMentions(args.sourceURL)
    for href in mentions:
        if sourceURL <> href:
            wmStatus, wmUrl = ronkyuu.discoverWebmention(href)
            if wmUrl is not None and wmStatus == 200:
                print('    mention found with webmention endpoint: %s' % href)
                r = ronkyuu.webMention(sourceURL, href, wmUrl)

                if r.status_code == requests.codes.ok:
                    print('   webmention sent successfully')
                else:
                    print('   webmention send returned a status code of %s' % r.status_code)
