import tweepy
import sys
import csv
import pandas

access_key = "USE YOUR OWN"
access_secret = "USE YOUR OWN"
consumer_key = "USE YOUR OWN"
consumer_secret = "USE YOUR OWN"
WOEID_UK = 23424975

# Authorisation and API endpoint
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error: authentication")

import time

def change_timestamp(tweet):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
    tweet['created_at'] = ts
    return tweet

df = pandas.read_csv("trends.csv")
trends_names = df["name"].tolist()

from pymongo import MongoClient
import json
import tweepy

MONGO_HOST = "localhost"
DATABASE = "twitter"
COLLECTION = "trendsCrawl"

try:
    client = MongoClient(MONGO_HOST)
    db = client[DATABASE]
except:
    print("Error Loading DB")
    sys.exit(1)

i = 1

for trend in trends_names:
    for tweet in tweepy.Cursor(api.search, q=trend, lang='en', tweet_mode='extended').items(20):
        tweet = tweet._json
        tweet = change_timestamp(tweet)
        db[COLLECTION].insert(tweet)
        print(i, "Tweet saved: ", trend)
        time.sleep(0.2)
        i += 1
