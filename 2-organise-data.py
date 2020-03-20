import sys
import time
from pymongo import MongoClient
import json
from bson import json_util
import pandas as pd
from sklearn.externals import joblib

MONGO_HOST = "localhost"
DATABASE = "twitter"
COLLECTION = "trendsCrawl"

try:
    client = MongoClient(MONGO_HOST)
    db = client[DATABASE]
    print("Database connection: OK")
except:
    print("Error: Loading DB")
    sys.exit(1)

try:   
    data_count = count = db[COLLECTION].count()
    data_l = list(db[COLLECTION].find({}))
    if (len(data_l) == data_count):
        print(data_count, "Data documents loaded OK")
    else:
        print("Data documents loaded ERROR")
except:
    print("Error: load entire DB incorrectly")

df = pd.DataFrame(data_l)
size_0 = df.shape[0]

df = df.drop_duplicates(subset="id_str")
size_1 = df.shape[0]
num_duplicates = size_0 - size_1
print(num_duplicates, " duplicates removed")

print(df.shape)
print(df.columns.values)

#serialize
df.to_pickle("tweets.pkl")
print("tweets.pkl saved")