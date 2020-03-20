import tweepy
import sys
from pymongo import MongoClient
import json
import tweepy
import time

access_key = "USE YOUR OWN"
access_secret = "USE YOUR OWN"
consumer_key = "USE YOUR OWN"
consumer_secret = "USE YOUR OWN"
MONGO_HOST = "localhost"
DATABASE = "twitter"
COLLECTION = "simpleCrawler"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error: authentication")

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
    
    def on_connect(self):
        print("Connected to the Twitter streaming API.")

    def on_data(self, data):
        try:
            client = MongoClient(MONGO_HOST)
            db = client[DATABASE]
            datajson = json.loads(data)
            tweet = change_timestamp(datajson)
            db[COLLECTION].insert(tweet)
            
        except Exception as e:
           print("Exception:", e)

    def on_error(self, status_code):
        if status_code == 420:
            return False

def change_timestamp(tweet):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
    tweet['created_at'] = ts
    return tweet

tweets_listener = MyStreamListener(api)
stream = tweepy.Stream(api.auth, tweets_listener)
stream.sample(languages=["en"])
