# Compute Term Frequency
# $ python frequency.py <tweet_file>
# It computes the term frequency histogram of the livestream data

import sys
import json

twitterData = sys.argv[1]
trans = {":":"", ";":"","(":"", "@":"",",":"",")":"","#":"","'":"","?":"",".":"","/":"","-":"","!":"","&":"","*":"",}
term_frec = {}

def tweet_dict(twitterData):
    """ format twitter file into list of dictionaries of lists :] """
    twitter_file = open(twitterData)
    tweets = []
    for line in twitter_file:
        tweets.append(json.loads(line))
    return tweets

def clean_word(word):
    """clean the words from the characters in dict trans"""
    for key, replacement in trans.items():
        word = word.replace(key, replacement)
    return word

def update_dict(tweet):
    """add a new term or update the counter"""
    text_list = tweet["text"].split()
    for word in text_list:
        word = clean_word(word)
        if len(word)!= 0:
            if word in term_frec.keys():
                term_frec[word] += 1
            else:
                term_frec[word] = 1

def print_frec(term_frec):
    """print the term and the frequency of each term"""
    count = 0.0
    for term in term_frec.keys():
        count += term_frec[term]
    for term in term_frec.keys():
        print term + " " + str(term_frec[term]/count)
    

def main():
    tweets = tweet_dict(twitterData)
    for index, tweet in enumerate(tweets):
        #print index
        if tweet.has_key("text"):
            update_dict(tweet)
    print_frec(term_frec)
            
    
    
    
if __name__ == '__main__':
    main()