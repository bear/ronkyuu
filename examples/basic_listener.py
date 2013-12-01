#!/usr/bin/env python

import argparse
import requests
import ronkyuu

from flask import Flask, request

app = Flask(__name__)

def validator(targetURL):
    """Validate the target URL exists just by making
    a HEAD request for it
    """
    r = requests.head(targetURL)
    return r.status_code == requests.codes.ok

def mention(sourceURL, targetURL):
    """Process the Webmention of the targetURL from the sourceURL.

    To verify that the sourceURL has indeed referenced our targetURL
    we just point findMentions() at it and scan the resulting href list.
    """
    mentions = ronkyuu.findMentions(sourceURL)
    found    = False

    for href in mentions:
        if href <> sourceURL and href == targetURL:
            update(sourceURL, targetURL)

def update(sourceURL, targetURL):
    """Do something with the Webmention
    """
    print "Our post at %s was referenced by %s" % (targetURL, sourceURL)


@app.route('/webmention')
def handleWebmention():
    if request.method == 'POST':
        valid  = False
        source = None
        target = None

        if 'source' in request.form:
            source = request.form['source']
        if 'target' in request.form:
            target = request.form['target']

        valid = validator(target)

        if valid:
            mention(source, target)

        if valid:
            return 'done'
        else:
            return 'invalid post', 404
    else:
        return 'webmention', 200


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',  default='0.0.0.0')
    parser.add_argument('--port',  default=5000, type=int)

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)
