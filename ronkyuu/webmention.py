# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2020 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
from .validators import URLValidator
from .tools import parse_link_header


_html_parser = 'html5lib'   # 'html.parser', 'lxml', 'lxml-xml'

def setParser(htmlParser='html5lib'):
    """Allow consumers of Ronkyuu to change the default
    HTML parser BeautifulSoup will use to parse the returned HTML
    """
    global _html_parser  # pylint: disable=global-statement
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


def findMentions(sourceURL, targetURL=None, exclude_domains=None, content=None, test_urls=True, headers=None, timeout=None):
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
    __doc__ = None  # pylint: disable=redefined-builtin

    if exclude_domains is None:
        exclude_domains = []
    if headers is None:
        headers = {}
    if test_urls:
        URLValidator(message='invalid source URL')(sourceURL)

    if content:
        result = {'status':   requests.codes.ok,  # pylint: disable=no-member
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

    if result['status'] == requests.codes.ok:  #pylint: disable=no-member
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


def discoverEndpoint(url, test_urls=True, headers=None, timeout=None, request=None, debug=False):
    """Discover any WebMention endpoint for a given URL.

    :param link: URL to discover WebMention endpoint
    :param test_urls: optional flag to test URLs for validation
    :param headers: optional headers to send with any web requests
    :type headers dict
    :param timeout: optional timeout for web requests
    :type timeout float
    :param request: optional Requests request object to avoid another GET
    :rtype: tuple (status_code, URL, [debug])
    """
    if headers is None:
        headers = {}
    if test_urls:
        URLValidator(message='invalid URL')(url)

    # status, webmention
    endpointURL = None
    debugOutput = []
    try:
        if request is not None:
            targetRequest = request
        else:
            targetRequest = requests.get(url, verify=False, headers=headers, timeout=timeout)
        returnCode = targetRequest.status_code
        debugOutput.append('%s %s' % (returnCode, url))
        if returnCode == requests.codes.ok:  #pylint: disable=no-member
            try:
                linkHeader  = parse_link_header(targetRequest.headers['link'])
                endpointURL = linkHeader.get('webmention', '') or \
                              linkHeader.get('http://webmention.org', '') or \
                              linkHeader.get('http://webmention.org/', '') or \
                              linkHeader.get('https://webmention.org', '') or \
                              linkHeader.get('https://webmention.org/', '')
                # force searching in the HTML if not found
                if not endpointURL:
                    raise AttributeError
                debugOutput.append('found in link headers')
            except (KeyError, AttributeError):
                endpointURL = findEndpoint(targetRequest.text)
                debugOutput.append('found in body')
            if endpointURL is not None:
                endpointURL = urljoin(url, endpointURL)
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError, requests.exceptions.URLRequired,
            requests.exceptions.TooManyRedirects, requests.exceptions.Timeout):
        debugOutput.append('exception during GET request')
        returnCode = 500
    debugOutput.append('endpointURL: %s %s' % (returnCode, endpointURL))
    if debug:
        return (returnCode, endpointURL, debugOutput)
    return (returnCode, endpointURL)

def sendWebmention(sourceURL, targetURL, webmention=None, test_urls=True, vouchDomain=None,
                   headers=None, timeout=None, debug=False):
    """Send to the :targetURL: a WebMention for the :sourceURL:

    The WebMention will be discovered if not given in the :webmention:
    parameter.

    :param sourceURL: URL that is referencing :targetURL:
    :param targetURL: URL of mentioned post
    :param webmention: optional WebMention endpoint
    :param test_urls: optional flag to test URLs for validation
    :param headers: optional headers to send with any web requests
    :type headers dict
    :param timeout: optional timeout for web requests
    :type timeout float

    :rtype: HTTPrequest object if WebMention endpoint was valid
    """
    if headers is None:
        headers = {}
    if test_urls:
        v = URLValidator()
        v(sourceURL)
        v(targetURL)

    debugOutput = []
    originalURL = targetURL
    try:
        targetRequest = requests.get(targetURL)

        if targetRequest.status_code == requests.codes.ok:  #pylint: disable=no-member
            if len(targetRequest.history) > 0:
                redirect = targetRequest.history[-1]
                if (redirect.status_code == 301 or redirect.status_code == 302) and 'Location' in redirect.headers:
                    targetURL = urljoin(targetURL, redirect.headers['Location'])
                    debugOutput.append('targetURL redirected: %s' % targetURL)
        if webmention is None:
            wStatus, wUrl = discoverEndpoint(targetURL, headers=headers, timeout=timeout, request=targetRequest)
        else:
            wStatus = 200
            wUrl = webmention
        debugOutput.append('endpointURL: %s %s' % (wStatus, wUrl))
        if wStatus == requests.codes.ok and wUrl is not None:  #pylint: disable=no-member
            if test_urls:
                v(wUrl)
            payload = {'source': sourceURL,
                       'target': originalURL}
            if vouchDomain is not None:
                payload['vouch'] = vouchDomain
            try:
                result = requests.post(wUrl, data=payload, headers=headers, timeout=timeout)
                debugOutput.append('POST %s -- %s' % (wUrl, result.status_code))
                if result.status_code == 405 and len(result.history) > 0:
                    redirect = result.history[-1]
                    if redirect.status_code == 301 and 'Location' in redirect.headers:
                        result = requests.post(redirect.headers['Location'], data=payload, headers=headers, timeout=timeout)
                        debugOutput.append('redirected POST %s -- %s' % (redirect.headers['Location'], result.status_code))
            except Exception:  # pylint: disable=broad-except
                result = None
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError, requests.exceptions.URLRequired,
            requests.exceptions.TooManyRedirects, requests.exceptions.Timeout):
        debugOutput.append('exception during GET request')
        result = None

    if debug:
        return result, debugOutput
    return result
