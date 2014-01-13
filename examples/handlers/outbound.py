
import requests

from ronkyuu import sendWebmention


def setup():
    pass

def outboundWebmention(sourceURL, targetURL):
    sendWebmention(sourceURL, targetURL)
