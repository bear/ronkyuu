#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import sys, os

import requests
from urlparse import urlparse
from bs4 import BeautifulSoup


# User Aaron posts a blog post on his blog
# User Barnaby writes post on his blog that links to Aaron's post.
# After publishing the post (i.e. it has a URL), Barnaby's server notices this link as part of the publishing process
# Barnaby's server does webmention discovery on Aaron's post to find its webmention endpoint (if not found, process stops)
# Barnaby's server sends a webmention to Aaron's post's webmention endpoint with
#     source set to Barnaby's post's permalink
#     target set to Aaron's post's permalink. 
# Aaron's server receives the webmention
# Aaron's server verifies that target (after following redirects) in the webmention is a valid permalink on Aaron's blog (if not, processing stops)
# Aaron's server verifies that the source (when retrieved, after following redirects) in the webmention contains a hyperlink to the target (if not, processing stops) 

def findMentions(html, domains=[]):
    """Find all <a /> elements in the given html for a post.
       
    If any have an href attribute that is not from the
    one of the items in domains, append it to our lists.

    :param html: html text from a GET request
    :param domains: a list of domains to exclude from the search
    :type domains: list
    :rtype: dictionary of Mentions
    """
    dom    = BeautifulSoup(html)
    result = {}

    for link in dom.body.find_all('a'):
        href = link.get('href')
        url  = urlparse(href)

        if url.scheme in ('http', 'https'):
            if len(url.hostname) > 0 and url.hostname not in domains:
                result[href] = { 'reply':      False,
                                 'status':      0,
                                 'headers':    {},
                                 'content':    '',
                                 'webmention': ''
                               }
                item = link.get('class')
                if item is not None and 'u-in-reply-to' in item:
                    result[href]['reply'] = True
                item = link.get('rel')
                if item is not None and 'in-reply-to' in item:
                    result[href]['reply'] = True
    return result

def findEndpoint(html):
    """Find all <link /> elements in the html content returned
       from a GET request from a URL listed as a reply or mention
       and return the discovered webmention href.

    :param html: html text from a GET request
    :rtype: URL string
    """
    result = None
    dom    = BeautifulSoup(content)
    for link in dom.find_all('link'):
        rel = link.get('rel')
        if 'webmention' in rel or 'http://webmention.org/' in rel:
            result = link.get('href')
            break
    return result

def discoverWebmention(link):
    """Make a GET request for the given link.

    If the status code is ok, return any Webmention callback

    :param link: URL to discover Webmention data for
    :rtype: URL string
    """
    # status, webmention
    href = None
    r    = requests.get(link)

    if r.status_code == requests.codes.ok:
        href = findEndpoint(r.text)

    return (r.status_code, href)
