###  COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis ###
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is for crawling real-time tweets by initializing a stream listener. The API is provided by Twitter that requiring authentication written in "twitter_auth.py"
## The query term and track users are separately defined in track list and follow list.
## The tweets are stored into the database "tweets_new" into Couchdb

import time
from twitter_auth import TwitterAuth
import tweepy
from tweepy import OAuthHandler
from datetime import datetime
import json
from twitter_data import Tweet
import string
import couchdb

class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
       i=1

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Stream connection times out! Snoozing Zzzzzz'

     #This function gets called every time a new tweet is received on the stream
    def on_data(self, data):
        try:
            _tweet = json.loads(data)  
            _tweet['_id'] = _tweet['id_str']

            if(_tweet['entities']['user_mentions']):
                _user_mentions = _tweet['entities']['user_mentions'][0]['screen_name']
            else:
                _user_mentions = _tweet['entities']['user_mentions']

            if(_tweet['entities']['hashtags']):
                _hashtags = _tweet['entities']['hashtags'][0]['text']
            else:
                _hashtags = _tweet['entities']['hashtags']

            tweet_obj = Tweet(
                    _id = _tweet['id_str'],
                    processed_text = "", 
                    texts = _tweet['text'],
                    coordinates = _tweet['coordinates'],
                    user_mentions = _user_mentions,
                    hashtags = _hashtags,
                    user_id = _tweet['user']['id_str'],
                    user_name = _tweet['user']['screen_name'],
                    user_location =_tweet['user']['location'],
                    created_at = _tweet['created_at'],
                    favorite_count = _tweet['favorite_count'],
                    retweet_count = _tweet['retweet_count'])

            tweet_obj.store(db)
            print("saved")
            
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

if __name__ == '__main__':

    couch = couchdb.Server('http://130.220.209.37:5984/')
    USER_NAME = 'admin'
    USER_PASSWORDS = '940123'
    couch.resource.credentials = (USER_NAME, USER_PASSWORDS)

    db = couch['tweets_new']

	 #Create the listener
    listener = MyStreamListener()
    auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
    auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

    follow_list = []
    with open("../Dic/follow_list.txt") as f:
    	line = f.readline()
        while line:
            follow_list.append(line.strip())
            line = f.readline()

    track_list = []
    with open("../Dic/track_list.txt") as f:
        line = f.readline()
        while line:
            track_list.append(line.strip())
            line = f.readline()
    f.close()

    stream = tweepy.Stream(auth, listener)
    while True:
        try:
            stream.filter(languages=["en"], follow=follow_list,track=track_list)
        except (KeyboardInterrupt, SystemExit):
            print("KeyboardInterrupt,goodbye!")
            stream.disconnect()
            raise
