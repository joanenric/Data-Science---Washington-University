# Get Twitter Data
# $ python twitterstream.py > output.txt
# Let this script run for a minimum of 10 minutes.
# outut <tweetfile.txt>

import oauth2 as oauth
import urllib2 as urllib

access_token_key = "48292975-YFopiGQRCIBgJMgO4zUC1FfF42QVUWTUbGrX9WbOG"
access_token_secret = "SZ2UIXpz2P06Aok08gT0G2XT4fS39kb3vnPOigis"

consumer_key = "iHzp4YPJUg1o1jgUdnv3pA"
consumer_secret = "zOEdGeuf0DvsWCwH1UoHD8qOML6y9ypmadDSc8fHew"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://stream.twitter.com/1/statuses/sample.json"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  #f = open("output.txt", "w")
  for line in response:
    print line.strip()
    #f.write(line.strip()+"\n")

if __name__ == '__main__':
  fetchsamples()
