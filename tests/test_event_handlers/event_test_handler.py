"""Test Event Handler
"""

import requests

test_results = { 'inbound': None,
                 'outbound': None,
                 'post': None
               }

def setup():
    pass

def inboundWebmention(sourceURL, targetURL):
    test_results['inbound'] = targetURL
    return targetURL

def outboundWebmention(sourceURL, targetURL):
    test_results['outbound'] = targetURL

def postArticle(postURL):
    test_results['post'] = postURL
