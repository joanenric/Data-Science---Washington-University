# Derive the sentiment of new terms
# python term_sentiment.py <sentiment_file> <tweet_file>
# In this part you will be creating a script that computes the sentiment for the terms that do not appear in the file AFINN-111.txt.

import sys
import json   

sentimentData = sys.argv[1] #AFIN-111.txt
twitterData = sys.argv[2] #output.txt
new_terms = {}
def tweet_dict(twitterData):
    """ format twitter file into list of dictionaries of lists :] """
    twitter_file = open(twitterData)
    tweets = []
    for line in twitter_file:
        tweets.append(json.loads(line))
    return tweets

def sent_dict(sentimentData):
    """format the sentiment data into a dictionary"""
    sentiment_file = open(sentimentData)
    sentiment = {}
    for line in sentiment_file:
        word, score = line.split("\t")
        sentiment[word] = float(score)
    return sentiment

def filter_tweets(tweets):
    tweets_filtered=[]
    """select only the tweets that have"""
    for tweet in tweets:
        if "text" in tweet:
            tweets_filtered.append(tweet)
    return tweets_filtered

def new_dict(tweets, sentiment):
    global new_terms
    for tweet in tweets:
        score = 0
        text = tweet["text"].split()
        for word in text:
            if word in sentiment:
                score += sentiment[word]
        for word in text:
            if word in sentiment and word not in new_terms:
                new_terms[word] = sentiment[word]
            elif word not in sentiment and word in new_terms:
                new_terms[word] += score
            elif word not in new_terms and word not in sentiment:
                new_terms[word] = score
def print_terms():
    for i in new_terms:
        print i, new_terms[i]

def main():
    tweets = tweet_dict(twitterData)
    tweets_ = filter_tweets(tweets)
    sentiment = sent_dict(sentimentData)
    new_dict(tweets_, sentiment)
    print_terms()
    
if __name__ == '__main__':
    main()