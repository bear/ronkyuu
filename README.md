[![Downloads](https://img.shields.io/pypi/v/ronkyuu.svg)](https://pypi.python.org/pypi/ronkyuu/)
[![Circle CI](https://circleci.com/gh/bear/ronkyuu.svg?style=svg)](https://circleci.com/gh/bear/ronkyuu)
[![CodeCov](http://codecov.io/github/bear/ronkyuu/coverage.svg?branch=master)](http://codecov.io/github/bear/ronkyuu)
[![Requirements Status](https://requires.io/github/bear/ronkyuu/requirements.svg?branch=master)](https://requires.io/github/bear/ronkyuu/requirements/?branch=master)

論及 ronkyuu - mention, reference to, touching upon

Python package to help with parsing, handling and other manipulations of the IndieWeb Toolkit items, such as:
* [Webmention](http://indiewebcamp.com/webmention)
 * Discovery of mentions in a publisher's post, the handling of finding what the Webmention callback is for the reference and also handling of incoming Webmention requests are handled.
* [RelMe](http://microformats.org/wiki/rel-me)
 * Take a source URL and a resource URL that is supposed to be a rel=me for the source and verify that it is.

See the examples/ directory for sample command line tools.

Because Ronkyuu uses BeautifulSoup4 for it's amazing HTML wrangling ability, you have the option of enabling faster parsing via the `lxml` package instead of the default `html5lib` package. This is done by having `lxml` installed and...

```
import ronkyuu

ronkyuu.webmention.setParser('lxml')
```

Contributors
============
* bear (Mike Taylor)
* kartikprabhu (Kartik Prabhu)

WebMentions
===========
findMentions()
--------------
Find all <a /> elements in the html returned for a post.
If any have an href attribute that is not from the one of the items in domains, append it to our lists.

findEndpoint()
--------------
Search the given html content for all <link /> elements and return any discovered WebMention URL.

discoverEndpoint()
------------------
Discover any WebMention endpoint for a given URL.

sendWebmention(sourceURL, targetURL, webmention=None)
-----------------------------------------------------
Send to the targetURL a WebMention for the sourceURL.
The WebMention will be discovered if not given in the optional webmention parameter.

RelMe
=====
findRelMe()
-----------
Find all <a /> elements in the given html for a post.
If any have an href attribute that is rel="me" then include it in the result.

confirmRelMe()
--------------
Determine if a given resourceURL is authoritative for the profileURL.
The list of rel="me" links will be discovered if not provided in the optional profileRelMes parameter or the resourceRelMes paramter.

Validators
==========
URLValidator class

TODO: fill in details of how to use

Requires
========
Python v2.6+ but see requirements.txt for a full list

For testing we use [httmock](https://pypi.python.org/pypi/httmock/) to mock the web calls.
