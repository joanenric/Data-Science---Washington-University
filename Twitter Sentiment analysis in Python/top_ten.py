# Top ten hash tags
# computes the ten most frequently occurring hash tags from the data
# $ python top_ten.py <tweet_file>

import sys
import json

twitterData = sys.argv[1] #output.txt
hash_dic = {}
def tweet_dict(twitterData):
    """ format twitter file into list of dictionaries of lists :] """
    twitter_file = open(twitterData)
    tweets = []
    for line in twitter_file:
        tweets.append(json.loads(line))
    return tweets

def find_hash(tweet):
    global hash_dic
    hash_list = tweet["entities"]["hashtags"]
    #print hash_list[0]["indices"]
    if len(hash_list) > 0:
        for hashtag in hash_list:
            hash_text = hashtag["text"]
            if hash_text in hash_dic:
                hash_dic[hash_text] += 1
            else:
                hash_dic[hash_text] = 1

def sort_dic():
    return sorted(hash_dic.items(), key=lambda x: x[1])

def print_top_ten(a):
    for i in range(1,11):
        print a[-i][0], int(a[-i][1])

def main():
    tweets = tweet_dict(twitterData)
    for tweet in tweets:
        if "entities" in tweet:
            if "hashtags" in tweet["entities"].keys():
                #print len(tweet["entities"]["hashtags"])            
                find_hash(tweet)
    #print hash_dic
    ordered_hash = sort_dic()
    print_top_ten(ordered_hash)
    
     


            
    
    
    
if __name__ == '__main__':
    main()