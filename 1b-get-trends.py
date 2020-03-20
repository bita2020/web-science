import tweepy
import sys
import csv
import json

access_key = "1234605077396148225-WdFI38JeKRDwvvSXUutBcSDFDrYmGg"
access_secret = "w918L6UXeDI71AsluQsAw73fGeqKDoBX9dV3T8tuqaKdT"
consumer_key = "3VRYiLHwpgFDAcu2VNOGtEVd2"
consumer_secret = "MKWEr4mQjvCuytmnXUr9M8LjwgpFctQEv9NvcsTCju2ULlVkYA"
WOEID_UK = 23424975

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error: authentication")

trends_JSON = api.trends_place(WOEID_UK)

trends = []

for i in range(0, len(trends_JSON[0]['trends'])):
    trends.append(trends_JSON[0]['trends'][i]['name'])


with open('trends.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["name"])

    for trend in trends:
        writer.writerow([trend])