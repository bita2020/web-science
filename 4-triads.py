import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from operator import itemgetter
import time
import math
from matplotlib.lines import Line2D

df = pd.read_pickle("tweets.pkl")
df = df.drop_duplicates(subset="id_str")
print(df.shape)

start = time.time()

G_replies = nx.DiGraph()

for i in range(0, df.shape[0]):
    tweeter_node = df.iloc[i]["user"]["screen_name"]
    reply_to_node = df.iloc[i]["in_reply_to_screen_name"]
    if (reply_to_node != None):
        #print(tweeter_node, "replies to", reply_to_node)
        if (G_replies.has_edge(tweeter_node, reply_to_node)):
            G_replies[tweeter_node][reply_to_node]['weight'] += 1
        else:
            G_replies.add_edge(tweeter_node, reply_to_node, weight=1)

triad_dict = nx.triadic_census(G_replies)
num_triads = triad_dict["021C"] + triad_dict["111D"] + triad_dict["111U"] + triad_dict["030T"] + triad_dict["030C"] + triad_dict["201"] + triad_dict["120D"] + triad_dict["120U"] + triad_dict["120C"] + triad_dict["210"] + triad_dict["300"]
print("Triads Replies:", num_triads)

G_retweets = nx.DiGraph()

for i in range(0, df.shape[0]):
    tweeter_node = df.iloc[i]["user"]["screen_name"]
    rs = df.iloc[i]["retweeted_status"]
    if not (isinstance(rs, float)):
        retweeted_node = rs["user"]["screen_name"]
        #print(tweeter_node, "retweets", retweeted_node)
        if (G_retweets.has_edge(tweeter_node, retweeted_node)):
            G_retweets[tweeter_node][retweeted_node]['weight'] += 1
        else:
            G_retweets.add_edge(tweeter_node, retweeted_node, weight=1)

triad_dict = nx.triadic_census(G_retweets)
num_triads = triad_dict["021C"] + triad_dict["111D"] + triad_dict["111U"] + triad_dict["030T"] + triad_dict["030C"] + triad_dict["201"] + triad_dict["120D"] + triad_dict["120U"] + triad_dict["120C"] + triad_dict["210"] + triad_dict["300"]
print("Triads Retweets:", num_triads)

G_mentions = nx.DiGraph()

for i in range(0, df.shape[0]):
    tweeter_node = df.iloc[i]["user"]["screen_name"]
    
    e = df.iloc[i]["entities"]
    if (len(e["user_mentions"]) > 0):
        for i in range(0, len(e["user_mentions"])):
            mentioned_node = (e["user_mentions"][i]["screen_name"])
            if (G_mentions.has_edge(tweeter_node, mentioned_node)):
                G_mentions[tweeter_node][mentioned_node]['weight'] += 1
            else:
                G_mentions.add_edge(tweeter_node, mentioned_node, weight=1)
tweeters = []
user_2_hashtags = {}

for i in range(0, df.shape[0]):
    tweeter_node = df.iloc[i]["user"]["screen_name"]
    tweeters.append(tweeter_node)
    
    hashtag1 = df.iloc[i]["entities"]["hashtags"]

    if(len(hashtag1) > 0):
        hashtag2 = (hashtag1[0]["text"])
        #print(tweeter_node, "uses #"+(hashtag2))
        
        if (tweeter_node in user_2_hashtags.keys()):
            if(hashtag2 not in user_2_hashtags[tweeter_node]):
                user_2_hashtags[tweeter_node].append(hashtag2)
        else:
            user_2_hashtags[tweeter_node] = [hashtag2,]

triad_dict = nx.triadic_census(G_mentions)
num_triads = triad_dict["021C"] + triad_dict["111D"] + triad_dict["111U"] + triad_dict["030T"] + triad_dict["030C"] + triad_dict["201"] + triad_dict["120D"] + triad_dict["120U"] + triad_dict["120C"] + triad_dict["210"] + triad_dict["300"]
print("Triads Mentions:", num_triads)

hashtag_2_frequency = {}

start = time.time()

G_coocurrence = nx.DiGraph()

for user1 in user_2_hashtags.keys():
    for user2 in user_2_hashtags.keys():
        if (user1 == user2):
            continue
        else:
            ht1 = user_2_hashtags[user1]
            ht2 = user_2_hashtags[user2]
            
            for ht in ht1:
                if ht in ht2:
                    if (G_coocurrence.has_edge(user1, user2)):
                        G_coocurrence[user1][user2]['weight'] += 1
                    else:
                        G_coocurrence.add_edge(user1, user2, weight=1)
                        if (ht in hashtag_2_frequency.keys()):
                            hashtag_2_frequency[ht] += 1
                        else:
                            hashtag_2_frequency[ht] = 1

end = time.time()


triad_dict = nx.triadic_census(G_coocurrence)
num_triads = triad_dict["021C"] + triad_dict["111D"] + triad_dict["111U"] + triad_dict["030T"] + triad_dict["030C"] + triad_dict["201"] + triad_dict["120D"] + triad_dict["120U"] + triad_dict["120C"] + triad_dict["210"] + triad_dict["300"]
print("Triads Hashtag co-occurence:", num_triads)
