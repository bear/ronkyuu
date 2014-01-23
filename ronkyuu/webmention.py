#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import os
import sys

import requests
import re
from urlparse import urlparse
from bs4 import BeautifulSoup, SoupStrainer

from validators import URLValidator


# User Aaron posts a blog post on his blog
# User Barnaby writes post on his blog that links to Aaron's post.
# After publishing the post (i.e. it has a URL), Barnaby's server notices this link as part of the publishing process
# Barnaby's server does webmention discovery on Aaron's post to find its webmention endpoint (if not found, process stops)
# Barnaby's server sends a webmention to Aaron's post's webmention endpoint with
#     source set to Barnaby's post's permalink
#     target set to Aaron's post's permalink.
# Aaron's server receives the webmention
# Aaron's server verifies that target (after following redirects) in the webmention is a valid permalink on Aaron's blog (if not, processing stops)
# Aaron's server verifies that the source (when retrieved, after following
# redirects) in the webmention contains a hyperlink to the target (if not,
# processing stops)

def findMentions(sourceURL, exclude_domains=[], content=None, look_in={'name':'body'}, test_urls=True):
    """Find all <a /> elements in the given html for a post. Only scan html element matching all criteria in look_in.

    optionally the content to be scanned can be given as an argument.
       
    If any have an href attribute that is not from the
    one of the items in exclude_domains, append it to our lists.

    :param sourceURL: the URL for the post we are scanning
    :param exclude_domains: a list of domains to exclude from the search
    :param content: the content to be scanned for mentions
    :param look_in: dictionary with name, id and class_. only element matching all of these will be scanned
    :param test_urls: optional flag to test URLs for validation
    :type exclude_domains: list
    :rtype: dictionary of Mentions
    """
    if test_urls:
        URLValidator(message='invalid source URL')(sourceURL)

    if content:
        result = {'status':   requests.codes.ok,
                  'headers':  None,
                  'content':  content
                  }
    else:
        r = requests.get(sourceURL, verify=False)
        result = {'status':   r.status_code,
                  'headers':  r.headers,
                  'content':  r.text
                  }

    result.update({'refs': set(), 'post-url': sourceURL})

    if result['status'] == requests.codes.ok:
        all_links = BeautifulSoup(result['content'], parse_only=SoupStrainer(**look_in)).find_all('a')
    
        for link in all_links:
            href = link['href']
            if href is not None:
                url = urlparse(href)

                if url.scheme in ('http', 'https'):
                    if len(url.hostname) > 0 and url.hostname not in exclude_domains:
                        result['refs'].add(href)
    return result


def findEndpoint(html):
    """Search the given html content for all <link /> elements
    and return any discovered WebMention URL.

    :param html: html content
    :rtype: WebMention URL
    """
    result = None
    all_links = BeautifulSoup(html).find_all('link')
    for link in all_links:
        rel = link.get('rel')
        if rel is not None and ('webmention' in rel or 'http://webmention.org/' in rel):
            result = link.get('href')
            break
    return result


def discoverEndpoint(url, test_urls=True):
    """Discover any WebMention endpoint for a given URL.

    :param link: URL to discover WebMention endpoint
    :param test_urls: optional flag to test URLs for validation
    :rtype: tuple (status_code, URL)
    """
    if test_urls:
        URLValidator(message='invalid URL')(url)

    # status, webmention
    href = None
    r    = requests.get(url,verify=False)
    if r.status_code == requests.codes.ok:
        try:
            link = r.headers['link']
            if  'rel="webmention"' in link:
                href = re.search('<(.+?)>;', link).group(1)
        except (KeyError, AttributeError):
            href = findEndpoint(r.text)

    return (r.status_code, href)


def sendWebmention(sourceURL, targetURL, webmention=None, test_urls=True):
    """Send to the :targetURL: a WebMention for the :sourceURL:

    The WebMention will be discovered if not given in the :webmention:
    parameter.

    :param sourceURL: URL that is referencing :targetURL:
    :param targetURL: URL of mentioned post
    :param webmention: optional WebMention endpoint
    :param test_urls: optional flag to test URLs for validation
    :rtype: HTTPrequest object if WebMention endpoint was valid
    """
    if test_urls:
        v = URLValidator()
        v(sourceURL)
        v(targetURL)

    result = None
    if webmention is None:
        wStatus, wUrl = discoverEndpoint(targetURL)
    else:
        wStatus = 200
        wUrl = webmention

    if wStatus == requests.codes.ok and wUrl is not None:
        if test_urls:
            v(wUrl)

        payload = {'source': sourceURL,
                   'target': targetURL}
        result  = requests.post(wUrl, data=payload)

    return result
