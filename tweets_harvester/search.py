###COMP90019 Master Project - Formula 1 Event Detection based on Sentiment Analysis
###  Student No. 732329       ###
###  Login Name: Jinghanl2    ###
###  Name: Jinghan Liang      ###

## Description ##
## This is for crawling historical tweets based on specified tweetsID or date. The API is provided by Twitter that requiring authentication written in "twitter_auth.py"
## The query term and track users are separately defined in track list and follow list.
## The tweets are stored into the database "tweets_new" into Couchdb

import tweepy
from tweepy import AppAuthHandler
import json
import datetime as dt
import time
from twitter_auth import TwitterAuth
import couchdb
from twitter_data import Tweet
 
''' Function that takes in a search string 'query', the maximum
    number of tweets 'max_tweets', and the minimum (i.e., starting)
     tweet id. It returns a list of tweepy.models.Status objects. '''   
def tweet_search(api, query, max_tweets, max_id, since_id):
    searched_tweets = []
    while len(searched_tweets) < max_tweets:
        remaining_tweets = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=remaining_tweets,
                                    since_id=since_id,
				                    max_id=max_id,languages=["en"])
            print('found',len(new_tweets),'tweets')
            if not new_tweets:
                print('no tweets found')
                break
            searched_tweets.extend(new_tweets)
            max_id = new_tweets[-1].id
        except tweepy.TweepError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
            time.sleep(15*60)
            break # stop the loop
    return searched_tweets, max_id

''' Function that gets the ID of a tweet. This ID can then be
        used as a 'starting point' from which to search. The query is
        required and has been set to a commonly used word by default.
        The variable 'days_ago' has been initialized to the maximum
        amount we are able to search back in time (9).'''
def get_tweet_id(api, date='', days_ago=9, query='a'):
    if date:
        # return an ID from the start of the given day
        td = date + dt.timedelta(days=1)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        tweet = api.search(q=query, count=1, until=tweet_date,languages=["en"])
    else:
        # return an ID from __ days ago
        td = dt.datetime.now() - dt.timedelta(days=days_ago)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        # get list of up to 10 tweets
        tweet = api.search(q=query, count=10, until=tweet_date,languages=["en"])
        print("search limit (start/stop):" + str(tweet[0].created_at))
        # return the id of the first tweet in the list
        return tweet[0].id

''' This is a script that continuously searches for tweets
    that were created over a given number of days. The search
    dates and search phrase can be changed below. '''
def main():
    #read search keywords from pre-defined file'''
    search_phrases = []
    with open("../Dic/track_list.txt") as f:
        line = f.readline()
        while line:
            search_phrases.append(line.strip())
            line = f.readline()
    f.close()

    time_limit = 0.5                           # runtime limit in hours
    max_tweets = 100                           # number of tweets per search (will be iterated over) - maximum is 100
    maximum = 5000000                          # total number of tweets aims to search (ending point of gathering loop)
    min_days_old, max_days_old = 0, 8          # search limits e.g., from 7 to 8
                                               # gives current weekday from last week,
                                               # min_days_old=0 will search from right now


    # authorize and load the twitter API
    auth = tweepy.AppAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

    couch = couchdb.Server('http://130.220.209.37:5984/')
    USER_NAME = 'admin'
    USER_PASSWORDS = '940123'
    couch.resource.credentials = (USER_NAME, USER_PASSWORDS)
    
    db = couch['tweets_new']

    print("Downloading max {0} tweets".format(maximum))

    tweetCount =0
    for search_phrase in search_phrases:
        print('Search phrase =', search_phrase)

        # get the ID of a tweet that is min_days_old
        if min_days_old == 0:
            max_id = -1
        else:
            max_id = get_tweet_id(api, days_ago=(min_days_old-1))
        # set the smallest ID to search for
        since_id = get_tweet_id(api, days_ago=(max_days_old-1))
        print("max id (starting point) =" + str(max_id))
        print("since id (ending point) =" + str(since_id))
        

        ''' tweet gathering loop  '''
        start = dt.datetime.now()
        end = start + dt.timedelta(hours=time_limit)
        
        count, exitcount = 0, 0
        while dt.datetime.now() < end:
            count += 1
            print("count =" + str(count))
            # collect tweets and update max_id
            new_tweets, max_id = tweet_search(api, search_phrase, max_tweets,
                                          max_id=max_id, since_id=since_id)

            try:
                # write tweets to file in JSON format
                if new_tweets:
                    for tweet in new_tweets:
                        _tweet = tweet._json
                        if 'RT @' not in _tweet['text']:
                            if(_tweet['id_str'] not in db):
                                _tweet['_id'] = _tweet['id_str']
                                
                                tweet_obj = Tweet(
                                    _id = _tweet['id_str'],
                                    processed_text = "", 
                                    texts = _tweet['text'],
                                    coordinates = _tweet['coordinates'],
                                    user_id = _tweet['user']['id_str'],
                                    user_name = _tweet['user']['screen_name'],
                                    user_location =_tweet['user']['location'],
                                    created_at = _tweet['created_at'],
                                    favorite_count = _tweet['favorite_count'],
                                    retweet_count = _tweet['retweet_count'])

                                tweet_obj.store(db)
                        exitcount = 0
                        tweetCount += len(new_tweets)
                else:
                    exitcount += 1
                    if exitcount == 3:
                        if search_phrase == search_phrases[-1]:
                            sys.exit('Maximum number of empty tweet strings reached - exiting')
                        else:
                            print('Maximum number of empty tweet strings reached - breaking')
                            break
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                break

if __name__ == "__main__":
    main()
