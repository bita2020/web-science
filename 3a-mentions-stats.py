import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from operator import itemgetter
import time
from matplotlib.lines import Line2D

df = pd.read_pickle("tweets.pkl")
print(df.shape)

G_mentions = nx.Graph()

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

degrees = [val for (node, val) in G_mentions.degree()]
print("---")
print(f"{G_mentions.number_of_nodes()} Nodes and {G_mentions.number_of_edges()} Edges")
print(f"Maximum degree: {np.max(degrees)}")   
print(f"Minimum degree: {np.min(degrees)}")
print(f"Average degree: {np.mean(degrees):.5f}")  
print(f"Most frequent degree: {stats.mode(degrees)[0][0]}")

if nx.is_connected(G_mentions):
    print("graph is connected")
else:
    print("graph is not connected")

print(f"Number of connected components: {nx.number_connected_components(G_mentions)}")
print(f"Average clustering coefficient: {nx.average_clustering(G_mentions):.5f}")
print(f"Transitivity: {nx.transitivity(G_mentions):.5f}")

# Takes 7 minutes
start = time.time()
graph_centrality = nx.degree_centrality(G_mentions)
max_de = max(graph_centrality.items(), key=itemgetter(1))
sorted_centrality = sorted(graph_centrality.items(), key = itemgetter(1), reverse = True)
graph_closeness = nx.closeness_centrality(G_mentions)
sorted_closeness = sorted(graph_closeness.items(), key = itemgetter(1), reverse = True)
max_clo = max(graph_closeness.items(), key=itemgetter(1))
graph_betweenness = nx.betweenness_centrality(G_mentions, normalized=True, endpoints=False)
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


# Takes  minutes
start = time.time()
node_and_degree = G_mentions.degree()
colors_central_nodes = ['red', 'green', 'yellow', 'blue', 'brown']
central_nodes = ['sidetolaufer', 'SkyBet', 'protectyrbubble', 'RobBiddulph', 'sainsburys']
pos = nx.spring_layout(G_mentions, k=0.05)
plt.figure(figsize = (20,20))
nx.draw(G_mentions, pos=pos, node_color=range(9979), cmap=plt.get_cmap('Spectral'), edge_color="black", linewidths=0.3, node_size=60, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(G_mentions, pos=pos, nodelist=central_nodes, node_size=300, node_color=colors_central_nodes, label=central_nodes)

legend_ele = [
    Line2D([0], [0], marker='o', color='w', label='sidetolaufer', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='SkyBet', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='protectyrbubble', markerfacecolor='yellow', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='RobBiddulph', markerfacecolor='blue', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='sainsburys', markerfacecolor='brown', markersize=10),
]
plt.legend(title="Central Accounts", title_fontsize=20 ,loc="upper right", handles=legend_ele, prop={'size':20})

plt.savefig('graph_mentions.png')
end = time.time()
print(f'Time to draw graph: {round(end - start)}')