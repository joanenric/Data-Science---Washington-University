# Derive the sentiment of each tweet
# $ python tweet_sentiment.py <sentiment_file> <tweet_file>

import sys
import json
import unicodedata


tweet_satis = []
def hw(sent_file, tweet_file):
    sentiment = sent_file.readlines()
    tweets = tweet_file.readlines()
    for index, i in enumerate(sentiment):
        sentiment[index] = i.split("\t")
        sentiment[index][0] = sentiment[index][0].decode("ascii", "ignore")
    
    for index, i in enumerate(tweets):
        tweets[index] = json.loads(i)
        if "text" in tweets[index]:
            tweet_satis.append(sentence_sentiment(tweets[index]["text"],sentiment))
        else:
            tweet_satis.append(0.00)
        print tweet_satis[index]
    
    for i in tweet_satis:
        print i

def sentence_sentiment(s,l):
    a = [0]*len(l)
    for i in range(len(l)):
        a[i] = s.count(l[i][0]) * float(l[i][1])
    return sum(a)

def lines(fp):
    pass #print str(len(fp.readlines()))

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw(sent_file, tweet_file)
    lines(sent_file)
    lines(tweet_file)

if __name__ == '__main__':
    main()
