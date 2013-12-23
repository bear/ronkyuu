#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import os, sys
import argparse
import ronkyuu


valid_events = ('inbound', 'outbound', 'post')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('event')
    parser.add_argument('--sourceURL', default=None)
    parser.add_argument('--targetURL', default=None)
    parser.add_argument('--eventConfigFile', default=None)

    args = parser.parse_args()

    eventType = args.event.lower()

    if eventType not in valid_events:
        print('event must be one of the following %s' % ','.join(valid_events))
    else:
        if eventType in ('inbound', 'outbound'):
            if args.sourceURL is None or args.targetURL is None:
                print('an %s event requires both sourceURL and targetURL' % eventType)
                sys.exit(2)
        else:
            if args.sourceURL is None:
                print('a post event requires the sourceURL')
                sys.exit(2)

        events = ronkyuu.Events()

        if eventType == 'inbound':
            events.inboundWebmention(args.sourceURL, args.targetURL)
        elif eventType == 'outbound':
            events.outboundWebmention(args.sourceURL, args.targetURL)
        else:
            events.postArticle(args.sourceURL)
