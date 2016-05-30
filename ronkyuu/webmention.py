# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2016 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import requests
from bs4 import BeautifulSoup
from .validators import URLValidator
from .tools import parse_link_header

try:  # Python v3
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin


_html_parser = 'html5lib'   # 'html.parser', 'lxml', 'lxml-xml'

def setParser(htmlParser='html5lib'):
    global _html_parser
    _html_parser = htmlParser


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


def findMentions(sourceURL, targetURL=None, exclude_domains=[], content=None, test_urls=True, headers={}, timeout=None):
    """Find all <a /> elements in the given html for a post. Only scan html element matching all criteria in look_in.

    optionally the content to be scanned can be given as an argument.

    If any have an href attribute that is not from the
    one of the items in exclude_domains, append it to our lists.

    :param sourceURL: the URL for the post we are scanning
    :param exclude_domains: a list of domains to exclude from the search
    :type exclude_domains: list
    :param content: the content to be scanned for mentions
    :param look_in: dictionary with name, id and class_. only element matching all of these will be scanned
    :param test_urls: optional flag to test URLs for validation
    :param headers: optional headers to send with any web requests
    :type headers: dict
    :param timeout: optional timeout for web requests
    :type timeout float
    :rtype: dictionary of Mentions
    """

    __doc__ = None

    if test_urls:
        URLValidator(message='invalid source URL')(sourceURL)

    if content:
        result = {'status':   requests.codes.ok,
                  'headers':  None,
                  }
    else:
        r = requests.get(sourceURL, verify=True, headers=headers, timeout=timeout)
        result = {'status':   r.status_code,
                  'headers':  r.headers
                  }
        # Check for character encodings and use 'correct' data
        if 'charset' in r.headers.get('content-type', ''):
            content = r.text
        else:
            content = r.content

    result.update({'refs': set(), 'post-url': sourceURL})

    if result['status'] == requests.codes.ok:
        # Allow passing BS doc as content
        if isinstance(content, BeautifulSoup):
            __doc__ = content
            # result.update({'content': unicode(__doc__)})
            result.update({'content': str(__doc__)})
        else:
            __doc__ = BeautifulSoup(content, _html_parser)
            result.update({'content': content})

        # try to find first h-entry else use full document
        entry = __doc__.find(class_="h-entry") or __doc__

        # Allow finding particular URL
        if targetURL:
            # find only targetURL
            all_links = entry.find_all('a', href=targetURL)
        else:
            # find all links with a href
            all_links = entry.find_all('a', href=True)
        for link in all_links:
            href = link.get('href', None)
            if href:
                url = urlparse(href)

                if url.scheme in ('http', 'https'):
                    if url.hostname and url.hostname not in exclude_domains:
                        result['refs'].add(href)
    return result


def findEndpoint(html):
    """Search the given html content for all <link /> elements
    and return any discovered WebMention URL.

    :param html: html content
    :rtype: WebMention URL
    """
    poss_rels = ['webmention', 'http://webmention.org', 'http://webmention.org/', 'https://webmention.org', 'https://webmention.org/']

    # find elements with correct rels and a href value
    all_links = BeautifulSoup(html, _html_parser).find_all(rel=poss_rels, href=True)
    for link in all_links:
        s = link.get('href', None)
        if s is not None:
            return s

    return None


def discoverEndpoint(url, test_urls=True, debug=False, headers={}, timeout=None):
    """Discover any WebMention endpoint for a given URL.

    :param link: URL to discover WebMention endpoint
    :param test_urls: optional flag to test URLs for validation
    :param debug: if true, then include in the returned tuple
                  a list of debug entries
    :param headers: optional headers to send with any web requests
    :type headers dict
    :param timeout: optional timeout for web requests
    :type timeout float
    :rtype: tuple (status_code, URL, [debug])
    """
    if test_urls:
        URLValidator(message='invalid URL')(url)

    # status, webmention
    href = None
    d    = []
    try:
        r  = requests.get(url, verify=False, headers=headers, timeout=timeout)
        rc = r.status_code
        d.append('is url [%s] retrievable? [%s]' % (url, rc))
        if rc == requests.codes.ok:
            try:
                link = parse_link_header(r.headers['link'])
                href = link.get('webmention', '') or link.get('http://webmention.org', '') or link.get('http://webmention.org/', '') or link.get('https://webmention.org', '') or link.get('https://webmention.org/', '')

                # force searching in the HTML if not found
                if not href:
                    d.append('link header not found, forcing html scan')
                    raise AttributeError
            except (KeyError, AttributeError):
                href = findEndpoint(r.text)

            if href is not None:
                href = urljoin(url, href)
            d.append('discovered href [%s]' % href)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError, requests.exceptions.URLRequired,
            requests.exceptions.TooManyRedirects, requests.exceptions.Timeout):
        rc = 500
    if debug:
        return (rc, href, d)
    else:
        return (rc, href)

def sendWebmention(sourceURL, targetURL, webmention=None, test_urls=True, vouchDomain=None,
                   debug=False, headers={}, timeout=None):
    """Send to the :targetURL: a WebMention for the :sourceURL:

    The WebMention will be discovered if not given in the :webmention:
    parameter.

    :param sourceURL: URL that is referencing :targetURL:
    :param targetURL: URL of mentioned post
    :param webmention: optional WebMention endpoint
    :param test_urls: optional flag to test URLs for validation
    :param debug: if true, then include in the returned tuple
                  a list of debug entries
    :param headers: optional headers to send with any web requests
    :type headers dict
    :param timeout: optional timeout for web requests
    :type timeout float

    :rtype: HTTPrequest object if WebMention endpoint was valid
    """
    if test_urls:
        v = URLValidator()
        v(sourceURL)
        v(targetURL)

    result = None
    d      = []
    if webmention is None:
        wStatus, wUrl = discoverEndpoint(targetURL, debug=False, headers=headers, timeout=timeout)
    else:
        wStatus = 200
        wUrl = webmention

    if wStatus == requests.codes.ok and wUrl is not None:
        if test_urls:
            v(wUrl)

        payload = {'source': sourceURL,
                   'target': targetURL}
        if vouchDomain is not None:
            payload['vouch'] = vouchDomain

        d.append('sending to [%s] %s' % (wUrl, payload))
        try:
            result = requests.post(wUrl, data=payload, headers=headers, timeout=timeout)
            d.append('POST returned %d' % result.status_code)

            if result.status_code == 405 and len(result.history) > 0:
                d.append('status code was 405, looking for redirect location')
                o = result.history[-1]
                if o.status_code == 301 and 'Location' in o.headers:
                    d.append('redirected to [%s]' % o.headers['Location'])
                    result = requests.post(o.headers['Location'], data=payload, headers=headers, timeout=timeout)
            elif result.status_code not in (200, 201, 202):
                d.append('status code was not 200, 201, 202')
        except:
            d.append('exception during request post')
            result = None
    if debug:
        return result, d
    else:
        return result
