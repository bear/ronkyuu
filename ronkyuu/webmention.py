#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.
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

class iwPost(object):
    """IndieWeb Post Webmention Handler

    Parse the HTML for a given post, discover replies and mentions and then
    discover if any of the found links have a Webmention callback.

    Usage
        iw = iwPost(['foo.com', 'blog.foo.com'])

        iw.parse(htmlContent)

        for link in iw.mentions:
            print 'Link %s' % link

        iw.discoverMentions()

        for link in iw.mentions:
            if 'webmention' in iw.mentions[link]:
                print 'Webmention callback for %s is %s' % (link, iw.mentions[link]['webmention'])
    """
    def __init__(self, ourHosts):
        self.ourHosts = ourHosts
        self.html     = None
        self.dom      = None
        self.mentions = {}

    def parse(self, html):
        self.html     = html
        self.mentions = {}
        self.dom      = BeautifulSoup(self.html)

        self.findMentions()

    def findMentions(self):
        """Find all <a /> elements in the given html for a post.
           If any have an href attribute that is not from the
           domains listed in ourHosts, append it to our lists.
        """
        if self.dom is not None:
            for link in self.dom.body.find_all('a'):
                href = link.get('href')
                url  = urlparse(href)

                if url.scheme in ('http', 'https'):
                    if len(url.hostname) > 0 and url.hostname not in self.ourHosts: 
                        self.mentions[href] = { 'reply':      False,
                                                'status':      0,
                                                'headers':    {},
                                                'content':    '',
                                                'webmention': ''
                                              }
                        item = link.get('class')
                        if item is not None and 'u-in-reply-to' in item:
                            self.mentions[href]['reply'] = True
                        item = link.get('rel')
                        if item is not None and 'in-reply-to' in item:
                            self.mentions[href]['reply'] = True

    def discoverMentions(self):
        for href in self.mentions:
            self.discoverWebmention(href)

    def findEndpoint(self, content):
        """Find all <link /> elements in the html content returned
           from a reply or mention and return the href if it's 
           webmention rel.
        """
        result = None
        dom    = BeautifulSoup(content)
        for link in dom.find_all('link'):
            rel = link.get('rel')
            if 'webmention' in rel or 'http://webmention.org/' in rel:
                result = link.get('href')
                break
        return result

    def discoverWebmention(self, link):
        """Make a GET request for the given link 
           If the status code is ok, return any Webmention callback
        """
        item = self.mention[link]
        try:
            r = requests.get(link)
            item['status']     = r.status_code
            item['headers']    = r.headers
            item['content']    = r.text
            item['webmention'] = None

            if r.status_code == requests.codes.ok:
                href = self.findEndpoint(r.text)
                if href is not None:
                    item['webmention'] = href
        except:
            item['status'] = 0
