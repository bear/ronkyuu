#!/usr/bin/env python

"""
:copyright: (c) 2013 by Mike Taylor and Kartik Prabhu
:license: MIT, see LICENSE for more details.

IndieWeb Webmention Tools
"""

import os
import sys
import imp
import json

from . import discoverConfig


class Events(object):

    def __init__(self, config=None, cfgFilename=None):
        self.handlers = {}
        if config is None:
            self.config = discoverConfig(cfgFilename)
        else:
            self.config = config

        self.loadHandlers()

    def loadHandlers(self):
        if 'handler_path' in self.config:
            handlerPath = os.path.abspath(
                os.path.expanduser(self.config['handler_path']))

            for (dirpath, dirnames, filenames) in os.walk(handlerPath):
                for filename in filenames:
                    moduleName, moduleExt = os.path.splitext(
                        os.path.basename(filename))
                    if moduleExt == '.py':
                        module = imp.load_source(
                            moduleName, os.path.join(handlerPath, filename))
                        if hasattr(module, 'setup'):
                            self.handlers[moduleName] = module

    def inboundWebmention(self, sourceURL, targetURL):
        for moduleName in self.handlers:
            module = self.handlers[moduleName]
            try:
                if hasattr(module, 'inboundWebmention'):
                    module.inboundWebmention(sourceURL, targetURL)
            except Exception, e:
                raise Exception(
                    'error during module event call inboundWebmention(%s, %s)' %
                    (sourceURL, targetURL))

    def outboundWebmention(self, sourceURL, targetURL):
        for moduleName in self.handlers:
            module = self.handlers[moduleName]
            try:
                if hasattr(module, 'outboundWebmention'):
                    module.outboundWebmention(sourceURL, targetURL)
            except:
                raise Exception(
                    'error during module event call outboundWebmention(%s, %s)' %
                    (sourceURL, targetURL))

    def postArticle(self, postURL):
        for moduleName in self.handlers:
            module = self.handlers[moduleName]
            try:
                if hasattr(module, 'postArticle'):
                    module.postArticle(postURL)
            except:
                raise Exception(
                    'error during module event call: postArticle(%s)' % (postURL))
