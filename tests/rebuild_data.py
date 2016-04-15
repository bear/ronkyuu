import os
import json
import requests


path_testdata = './data/webmention_rocks_test'
test_data     = {}

for n in range(1, 22):
    url   = 'https://webmention.rocks/test/%d' % n
    hfile = '%s_%d.html' % (path_testdata, n)
    jfile = '%s_%d.json' % (path_testdata, n)
    if not os.path.exists(hfile):
        r = requests.get(url)

        with open(hfile, 'w') as h:
          h.write(r.text.encode('utf-8'))
        with open(jfile, 'w') as h:
          h.write(json.dumps(dict(r.headers), indent=2))
