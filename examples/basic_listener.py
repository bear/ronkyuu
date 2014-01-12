#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import logging
from logging.handlers import RotatingFileHandler

import argparse
import requests
import ronkyuu

from flask import Flask, request

app = Flask(__name__)

events = ronkyuu.Events(config={ "handler_path": "/srv/webmention/handlers" })


def initLogging(logger, logfilename='/var/log/webmentions/webmentions.log'):
    _log_formatter = logging.Formatter("%(asctime)s %(levelname)-9s %(message)s", "%Y-%m-%d %H:%M:%S")
    _log_handler   = logging.handlers.RotatingFileHandler(logfilename, maxBytes=1024 * 1024 * 100, backupCount=7)
    _log_handler.setFormatter(_log_formatter)

    logger.addHandler(_log_handler)
    logger.setLevel(logging.INFO)
    logger.info('starting Webmention App')

def validURL(targetURL):
    """Validate the target URL exists by making a HEAD request for it
    """
    r = requests.head(targetURL)
    return r.status_code == requests.codes.ok

def mention(sourceURL, targetURL):
    """Process the Webmention of the targetURL from the sourceURL.

    To verify that the sourceURL has indeed referenced our targetURL
    we run findMentions() at it and scan the resulting href list.
    """

    app.logger.info('discovering Webmention endpoint for %s' % sourceURL)

    mentions = ronkyuu.findMentions(sourceURL)

    for href in mentions['refs']:
        if href <> sourceURL and href == targetURL:
            app.logger.info('post at %s was referenced by %s' % (targetURL, sourceURL))
            events.inboundWebmention(sourceURL, targetURL, mentions=mentions)

@app.route('/webmention', methods=['GET', 'POST'])
def handleWebmention():
    app.logger.info('handleWebmention [%s]' % request.method)
    if request.method == 'POST':
        valid  = False
        source = None
        target = None

        if 'source' in request.form:
            source = request.form['source']
        if 'target' in request.form:
            target = request.form['target']

        valid = validURL(target)

        app.logger.info('source: %s target: %s valid? %s' % (source, target, valid))

        if valid:
            mention(source, target)

        if valid:
            return 'done'
        else:
            return 'invalid post', 404
    else:
        return 'GET invalid', 404


#
# Note - I run this app using uwsgi under nginx so it skips the entire
#        if __name__ section below, this means I have to setup logging
#        manually and have hard-coded the host and ports
initLogging(app.logger)

#
# None of the below will be run for nginx + uwsgi
#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host',    default='0.0.0.0')
    parser.add_argument('--port',    default=5000, type=int)

    args = parser.parse_args()

    initLogging(app.logger, './webmentions.log')

    app.run(host=args.host, port=args.port)
