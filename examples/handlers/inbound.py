
def setup():
    pass

def inboundWebmention(sourceURL, targetURL):
    #base, article = targetURL.split('https://bear.im/bearlog/')

    #articlePath = os.path.join('/')

    #add code here to look at targetURL, figure out the path to the markdown


    open('/tmp/webmentions.txt', 'a+').write('%s %s\n' % (sourceURL, targetURL))
