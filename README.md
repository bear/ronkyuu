ronkyuu
=======

論及 ronkyuu - mention, reference to, touching upon

Python package to help with parsing, handling and other manipulations
of the IndieWeb [Webmention](http://indiewebcamp.com/webmention)

Discovery of mentions in a publisher's post, the handling of finding what the
Webmention callback is for the reference and also handling of incoming Webmention
requests are handled.

Roadmap
=======
Working
* Mention discovery in a post
* Discovery of Webmention callback for a link

Pending
* POST of Webmention to discovered callback
* Receipt of a Webmention POST
* daemon to scan article collections for new and/or changed articles

Usage

Requires
========
Python v2.7+ but see requirements.txt for a full list

For testing I use [httmock](https://pypi.python.org/pypi/httmock/) to stub the web calls
