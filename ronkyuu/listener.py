#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention daemon
"""

from flask import Flask, request
from werkzeug.routing import Rule

app = Flask(__name__)

cbValidation = None
cbMention    = None

@app.endpoint('handleWebmention')
def handleWebmention():
    if request.method == 'POST':
        valid  = False
        source = None
        target = None

        if 'source' in request.form:
            source = request.form['source']
        if 'target' in request.form:
            target = request.form['target']

        if cbValidation is not None:
            valid = cbValidation(target)

        if valid and cbMention is not None:
            cbMention(source, target)

        if valid:
            return 'done'
        else:
            return 'invalid post', 404
    else:
        return 'error', 404

def run(host, port, route='/webmention', validation=None, mention=None, debug=False):
    global cbValidation, cbMention

    cbValidation = validation
    cbMention    = mention

    app.url_map.add(Rule(route, endpoint='handleWebmention'))
    app.run(host=host, port=port, debug=debug)
