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
* POST of Webmention to discovered callback
* Receipt of a Webmention POST

Pending
* daemon to scan article collections for new and/or changed articles

See the examples/ directory for sample command line tools.

Events
======
During the processing each task, be it an incoming webmention, reply or even a new
post - a new event will be generated and any event handlers listed will be given a
chance to process the event.

This is done to allow for external scripts or calls to be made to update the static
site and/or data files.

Events consist of the event type and a payload - not much else is really needed.

* webmention inbound
** source url, target url
* webmention outbound
** source url, target url
* article post
** source url or file

Requires
========
Python v2.6+ but see requirements.txt for a full list

For testing I use [httmock](https://pypi.python.org/pypi/httmock/) to stub the web calls

The Webmention daemon requires [Flask](http://flask.pocoo.org/docs/)
