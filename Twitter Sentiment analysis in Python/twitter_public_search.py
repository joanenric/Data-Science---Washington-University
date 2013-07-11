# Query Twitter with Python

import urllib
import json

response = urllib.urlopen("http://search.twitter.com/search.json?q=microsoft")
request = json.load(response)
results = request["results"]

for i in results:
    print i["text"]
    print ""

