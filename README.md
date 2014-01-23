ronkyuu
=======

論及 ronkyuu - mention, reference to, touching upon

Python package to help with parsing, handling and other manipulations
of the IndieWeb Toolkit items, such as:
* [Webmention](http://indiewebcamp.com/webmention)
 * Discovery of mentions in a publisher's post, the handling of finding what the Webmention callback is for the reference and also handling of incoming Webmention requests are handled.
* [RelMe](http://microformats.org/wiki/rel-me)
 * Take a source URL and a resource URL that is supposed to be a rel=me for the source and verify that it is.


Roadmap
=======
Working
* Mention discovery in a post
* Discovery of Webmention callback for a link
* POST of Webmention to discovered callback
* Receipt of a Webmention POST
* command line tool to trigger an event
* examples for event handling
* support for RelMe verification

Pending
* Flask app to allow test sending of webmentions
* WebHook listener to trigger events
* ...

See the examples/ directory for sample command line tools.

Contributors
============
* bear (Mike Taylor)
* kartikprabhu (Kartik Prabhu)


WebMentions
===========
findMentions(sourceURL, domains=[])
-----------------------------------
Find all <a /> elements in the html returned for a post.
If any have an href attribute that is not from the one of the items in domains, append it to our lists.

findEndpoint(html)
------------------
Search the given html content for all <link /> elements and return any discovered WebMention URL.

discoverEndpoint(url)
---------------------
Discover any WebMention endpoint for a given URL.

sendWebmention(sourceURL, targetURL, webmention=None)
-----------------------------------------------------
Send to the targetURL a WebMention for the sourceURL.
The WebMention will be discovered if not given in the optional webmention parameter.

RelMe
=====
findRelMe(sourceURL)
--------------------
Find all <a /> elements in the given html for a post.
If any have an href attribute that is rel="me" then include it in the result.

confirmRelMe(profileURL, resourceURL, profileRelMes=None, resourceRelMes=None)
------------------------------------------------------------------------------
Determine if a given resourceURL is authoritative for the profileURL.
The list of rel="me" links will be discovered if not provided in the optional
profileRelMes parameter or the resourceRelMes paramter.

Validators
==========
URLValidator class

TODO: fill in details of how to use

Events
======
During the processing each task, be it an incoming webmention, reply or even a new
post - a new event will be generated and any event handlers found will be given a
chance to process the event.

This is done to allow for external scripts or calls to be made to update the static
site and/or data files.

Right now I'm going to use a very simple "plugin" style for inbound, outbound and posts
where any .py file found in a directory is imported as a module. This will, I think, let
me use the event plugins via the command line, but also via WebHooks because I can create 
a Flask listener for WebHook urls and then call the event plugins.

Events consist of the event type and a payload - not much else is really needed.

* webmention inbound
 * source url, target url
* webmention outbound
 * source url, target url
* article post
 * source url or file

Requires
========
Python v2.6+ but see requirements.txt for a full list

For testing I use [httmock](https://pypi.python.org/pypi/httmock/) to stub the web calls

The Webmention daemon requires [Flask](http://flask.pocoo.org/docs/)
