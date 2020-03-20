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

df["retweeted_status"].replace(float('nan'), 0)

G_retweets = nx.Graph()

for i in range(0, df.shape[0]):
    tweeter_node = df.iloc[i]["user"]["screen_name"]
    rs = df.iloc[i]["retweeted_status"]
    if not (isinstance(rs, float)):
        retweeted_node = rs["user"]["screen_name"]
        print(tweeter_node, "retweets", retweeted_node)
        if (G_retweets.has_edge(tweeter_node, retweeted_node)):
            G_retweets[retweeted_node][tweeter_node]['weight'] += 1
        else:
            G_retweets.add_edge(retweeted_node, tweeter_node, weight=1)

degrees = [val for (node, val) in G_retweets.degree()]
print("---")
print(f"{G_retweets.number_of_nodes()} Nodes and {G_retweets.number_of_edges()} Edges")
print(f"Maximum degree: {np.max(degrees)}")   
print(f"Minimum degree: {np.min(degrees)}")
print(f"Average degree: {np.mean(degrees):.5f}")  
print(f"Most frequent degree: {stats.mode(degrees)[0][0]}")

if nx.is_connected(G_retweets):
    print("graph is connected")
else:
    print("graph is not connected")

print(f"Number of connected components: {nx.number_connected_components(G_retweets)}")
print(f"Average clustering coefficient: {nx.average_clustering(G_retweets):.5f}")
print(f"Transitivity: {nx.transitivity(G_retweets):.5f}")

# Takes 7 minutes
start = time.time()
graph_centrality = nx.degree_centrality(G_retweets)
max_de = max(graph_centrality.items(), key=itemgetter(1))
sorted_centrality = sorted(graph_centrality.items(), key = itemgetter(1), reverse = True)
graph_closeness = nx.closeness_centrality(G_retweets)
sorted_closeness = sorted(graph_closeness.items(), key = itemgetter(1), reverse = True)
max_clo = max(graph_closeness.items(), key=itemgetter(1))
graph_betweenness = nx.betweenness_centrality(G_retweets, normalized=True, endpoints=False)
sorted_betweeness = sorted(graph_betweenness.items(), key = itemgetter(1), reverse = True)
max_bet = max(graph_betweenness.items(), key=itemgetter(1))
print(f"the node with id {max_de[0]} has a degree centrality of {max_de[1]:.5f} which is the maximum of the Graph")
print(f"the node with id {max_clo[0]} has a closeness centrality of {max_clo[1]:.5f} which is the maximum of the Graph")
print(f"the node with id {max_bet[0]} has a betweenness centrality of {max_bet[1]:.5f} which is the maximum of the Graph")
print("Top-5 degree centrality:", sorted_centrality[0:5])
print("Top-5 degree closeness:", sorted_closeness[0:5])
print("Top-5 degree betweeness:", sorted_betweeness[0:5])
end = time.time()
print(f'Time to get centrality stats: {round(end - start)}')


# Takes 5 minutes
start = time.time()
node_and_degree = G_retweets.degree()
colors_central_nodes = ['red', 'green', 'yellow', 'blue', 'brown']
central_nodes = ['sidetolaufer', 'protectyrbubble', 'Smayphotography', 'gsc1', 'earlofbeverley']
pos = nx.spring_layout(G_retweets, k=0.05)
plt.figure(figsize = (20,20))
nx.draw(G_retweets, pos=pos, node_color=range(7804), cmap=plt.get_cmap('Spectral'), edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(G_retweets, pos=pos, nodelist=central_nodes, node_size=300, node_color=colors_central_nodes, label=central_nodes)

legend_ele = [
    Line2D([0], [0], marker='o', color='w', label='sidetolaufer', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='protectyrbubble', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='Smayphotography', markerfacecolor='yellow', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='gsc1', markerfacecolor='blue', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='earlofbeverley', markerfacecolor='brown', markersize=10),
]
plt.legend(title="Highest centrality degree accounts", title_fontsize=20 ,loc="upper right", handles=legend_ele, prop={'size':20})

plt.savefig('graph_retweets.png')
end = time.time()
print(f'Time to draw graph: {round(end - start)}')