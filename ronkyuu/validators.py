# -*- coding: utf-8 -*-
"""
:copyright: (c) 2013-2020 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb URL Validation

Regex and URL validators borrowed from django.core.validators
https://github.com/django/django/blob/master/django/core/validators.py

    Copyright (c) Django Software Foundation and individual contributors.
    All rights reserved.
    BSD Licensed
"""
import re

from urllib.parse import urlsplit, urlunsplit


class RegexValidator(object):  # pylint: disable=R0205
    """Abstract Class to validate URLs using given regular expressions
    """
    regex = ''
    message = 'Enter a valid value.'

    def __init__(self, regex=None, message=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message

        # Compile the regex if it was not passed pre-compiled.
        if isinstance(self.regex, str):
            self.regex = re.compile(self.regex)

    def __call__(self, value):
        """
        Validates that the input matches the regular expression.
        """
        if not self.regex.search(value):
            raise ValueError(self.message)

    def __eq__(self, other):
        return isinstance(other, RegexValidator) and (self.regex == other.regex) and (self.message == other.message)


class URLValidator(RegexValidator):  # pylint: disable=R0903
    """URL Validation using a regular expression
    """
    regex = re.compile(
        r'^(?:[a-z0-9\.\-]*)://'  # scheme is validated separately
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    message = 'Enter a valid URL.'
    # check only http and https
    schemes = ['http', 'https']

    def __init__(self, schemes=None, **kwargs):
        super(URLValidator, self).__init__(**kwargs)
        if schemes is not None:
            self.schemes = schemes

    def __call__(self, value):
        e = ValueError(self.message)
        # Check for None, and empty string
        if value in (None, ''):
            raise e
        value = str(value)
        # Check first if the scheme is valid
        scheme = value.split('://')[0].lower()
        if scheme not in self.schemes:
            raise e

        # Then check full URL
        try:
            super(URLValidator, self).__call__(value)
        except ValueError:
            # Trivial case failed. Try for possible IDN domain
            if value:
                scheme, netloc, path, query, fragment = urlsplit(value)
                try:
                    netloc = netloc.encode('idna').decode('ascii')  # IDN -> ACE
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(URLValidator, self).__call__(url)
            else:
                raise e
        else:
            url = value
