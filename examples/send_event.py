#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import argparse
import ronkyuu


valid_events = ('inbound', 'outbound', 'post')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('event')
    parser.add_argument('--sourceURL')
    parser.add_argument('--targetURL')

    args = parser.parse_args()

    eventType = args.event.lower()

    if eventType not in valid_events:
        print('event must be one of the following %s' % ','.join(valid_events))
    else:
        events = ronkyuu.Events()

        if eventType == 'inbound':
            events.inboundWebmention(args.sourceURL, args.targetURL)
        elif eventType == 'outbound':
            events.outboundWebmention(args.sourceURL, args.targetURL)
        else:
            events.postArticle(args.sourceURL)

        print('%s event triggered' % eventType)