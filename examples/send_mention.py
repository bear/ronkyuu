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
    parser.add_argument('--eventConfigFile', default=None)

    args = parser.parse_args()
    cfg  = ronkyuu.discoverConfig(args.eventConfigFile)

    domains   = [] #cfg.get('domains', [])
    sourceURL = args.sourceURL

    print('Scanning %s for mentions' % sourceURL)

    mentions = ronkyuu.findMentions(sourceURL, domains)

    print(mentions['refs'])

    for href in mentions['refs']:
        if sourceURL <> href:
            print href
            wmStatus, wmUrl = ronkyuu.discoverEndpoint(href, test_urls=False)
            if wmUrl is not None and wmStatus == 200:
                print('\tfound webmention endpoint %s for %s' % (wmUrl, href))
                status_code = ronkyuu.sendWebmention(sourceURL, href, wmUrl)

                if status_code == requests.codes.ok:
                    print('\twebmention sent successfully')
                else:
                    print('\twebmention send returned a status code of %s' % status_code)
