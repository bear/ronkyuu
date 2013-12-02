#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import sys, os
import json


class Events(object):
    def __init__(self, cfgFile=None):
        self.config   = {}
        self.handlers = None

        if cfgFile is None:
            cwd = os.getcwd()
            f   = os.path.join(cwd, 'ronkyuu.cfg')

            if os.exists(f):
                cfgFile = f
            else:
                f = os.path.expanduser('~/.ronkyuu.cfg')
                if os.exists(f):
                    cfgFile = f

        if cfgFile is not None:
            cfgFile = os.path.abspath(cfgFile)
            if os.exists(cfgFile):
                self.config = json.loads(' '.join(open(cfgFile, 'r').readlines())

    def loadHandlers(self):
        if self.handlers is None:
             for (dirpath, dirnames, filenames) in os.walk(self.config['handler_path']):
                for filename in filenames:
                    moduleName = os.path.basename(filename)[:-3]
                    try:
                        module = imp.load_source(moduleName, filename)

                        if hasattr(module, 'handlerSetup'):
                            self.handlers[moduleName] = module
                    except:
                        module = None

    def inboundWebmention(self, sourceURL, targetURL):
        pass

    def outboundWebmention(self, sourceURL, targetURL):
        pass

    def Post(self, sourceURL):
        pass

