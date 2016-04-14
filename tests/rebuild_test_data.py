import os
import json
import requests


path_testdata = './tests/data/webmention_rocks_test_'
test_data     = {}

for n in range(1, 15):
    url = 'webmention.rocks/test/%d' % n
    if not os.fileexists('%s%0d.html' % (path_testdata, n)):
        r = requests.get('https://%s' % url)
        with open('%s%0d.html' % (path_testdata, n), 'w') as h:
          h.write(r.text.encode('utf-8'))
        with open('%s%0d.json' % (path_testdata, n), 'w') as h:
          h.write(json.dumps(dict(r.headers), indent=2))
