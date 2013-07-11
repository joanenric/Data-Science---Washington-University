# Which State is happiest?
# returns the name of the happiest state as a string.
# $ python happiest_state.py <sentiment_file> <tweet_file>
 


import sys
import json
import types

sentimentData = sys.argv[1] #AFIN-111.txt
twitterData = sys.argv[2] #output.txt

states = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GE","HI","ID","IL","IN","IO","KN","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","PR","RI","SC","SD","TE","TX","UT","VT","VI","WA","WV","WI","WY"]

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
        sentiment[word] = score
    return sentiment

def filter_tweets(tweets):
    tweets_filtered=[]
    """select only the tweets that have"""
    for tweet in tweets:
        if "text" in tweet and "place" in tweet:
            #print tweet["place"]
            if type(tweet["place"]) != type(None):
                tweets_filtered.append(tweet)
    return tweets_filtered

def tweets_score(tweets, sentiment):
    sent = []
    for tweet in tweets:
        score_tweet = 0.0
        tweet_text = tweet["text"].split()
        for word in tweet_text:
            if word.encode("utf-8",'ignore') in sentiment.keys():
                score_tweet += float(sentiment[word])
        sent.append(score_tweet)
    return sent
        
def map_tweets(tweets, score):
    tweet_map = {}
    for index, tweet in enumerate(tweets):
        #print tweet["place"]["country_code"]
        code = tweet["place"]["country_code"]
        if code in states:        
            if code in tweet_map:
                tweet_map[code] += score[index]
            else:
                tweet_map[code] = score[index]
    return tweet_map

def max_state(tweet_map):
    state_max = max(tweet_map.iterkeys(), key=lambda k: tweet_map[k]) #selects de max value in a dictionary
    return state_max

def main():
    tweets = tweet_dict(twitterData)
    tweets_ = filter_tweets(tweets)
    sentiment = sent_dict(sentimentData)
    score = tweets_score(tweets_,sentiment)
    tweet_maps = map_tweets(tweets_,score)
    print (max_state(tweet_maps))
    
    
    
if __name__ == '__main__':
    main()