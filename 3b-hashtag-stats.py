import sys
import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from operator import itemgetter
import time
from matplotlib.lines import Line2D

df = pd.read_pickle("tweets.pkl")
df = df.drop_duplicates(subset="id_str")

tweeters = []
user_2_hashtags = {}

for i in range(0, df.shape[0]):
    tweeter_node = df.iloc[i]["user"]["screen_name"]
    tweeters.append(tweeter_node)
    
    hashtag1 = df.iloc[i]["entities"]["hashtags"]

    if(len(hashtag1) > 0):
        hashtag2 = (hashtag1[0]["text"])
        
        if (tweeter_node in user_2_hashtags.keys()):
            if(hashtag2 not in user_2_hashtags[tweeter_node]):
                user_2_hashtags[tweeter_node].append(hashtag2)
        else:
            user_2_hashtags[tweeter_node] = [hashtag2,]

hashtag_2_frequency = {}

start = time.time()

G_coocurrence = nx.Graph()

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
print(f'Time to make graph: {round(end - start)}')


# Takes 3 minutes
start = time.time()
degrees = [val for (node, val) in G_coocurrence.degree()]
print("---")
print(f"{G_coocurrence.number_of_nodes()} Nodes and {G_coocurrence.number_of_edges()} Edges")
print(f"Maximum degree: {np.max(degrees)}")   
print(f"Minimum degree: {np.min(degrees)}")
print(f"Average degree: {np.mean(degrees):.5f}")  
print(f"Most frequent degree: {stats.mode(degrees)[0][0]}")

if nx.is_connected(G_coocurrence):
    print("graph is connected")
else:
    print("graph is not connected")

print(f"Number of connected components: {nx.number_connected_components(G_coocurrence)}")
print(f"Average clustering coefficient: {nx.average_clustering(G_coocurrence):.5f}")

sorted_hashtags = sorted(hashtag_2_frequency.items(), key = itemgetter(1), reverse = True)
top = sorted_hashtags[0:10]
print("Top-shared hashtags:", sorted_hashtags[0:10])
print("TOTAL;", len(sorted_hashtags))

end = time.time()
print(f'Time to get stats: {round(end - start)}')

for i in range(0, len(top)):
    ht = str(top[i][0])
    edges = str(top[i][1])
    percentage = round(int(edges) / 782624 * 100, 2)
    percentage = str(percentage)
    print(ht, edges, "("+percentage+"%)")
