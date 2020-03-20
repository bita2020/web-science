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
print(df.shape)

G_replies = nx.Graph()

for i in range(0, df.shape[0]):
    tweeter_node = df.iloc[i]["user"]["screen_name"]
    reply_to_node = df.iloc[i]["in_reply_to_screen_name"]
    if (reply_to_node != None):
        print(tweeter_node, "replies to", reply_to_node)
        if (G_replies.has_edge(tweeter_node, reply_to_node)):
            G_replies[reply_to_node][tweeter_node]['weight'] += 1
        else:
            G_replies.add_edge(reply_to_node, tweeter_node, weight=1)

degrees = [val for (node, val) in G_replies.degree()]
print("---")
print(f"{G_replies.number_of_nodes()} Nodes and {G_replies.number_of_edges()} Edges")
print(f"Maximum degree: {np.max(degrees)}")   
print(f"Minimum degree: {np.min(degrees)}")
print(f"Average degree: {np.mean(degrees):.2f}")  
print(f"Most frequent degree: {stats.mode(degrees)[0][0]}")

if nx.is_connected(G_replies):
    print("graph is connected")
else:
    print("graph is not connected")

print(f"Number of connected components: {nx.number_connected_components(G_replies)}")
print(f"Average clustering coefficient: {nx.average_clustering(G_replies):.5f}")
print(f"Transitivity: {nx.transitivity(G_replies):.3f}")

# Takes 1 second
start = time.time()
graph_centrality = nx.degree_centrality(G_replies)
max_de = max(graph_centrality.items(), key=itemgetter(1))
sorted_centrality = sorted(graph_centrality.items(), key = itemgetter(1), reverse = True)
graph_closeness = nx.closeness_centrality(G_replies)
sorted_closeness = sorted(graph_closeness.items(), key = itemgetter(1), reverse = True)
max_clo = max(graph_closeness.items(), key=itemgetter(1))
graph_betweenness = nx.betweenness_centrality(G_replies, normalized=True, endpoints=False)
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


# Takes 15 seconds
start = time.time()
node_and_degree = G_replies.degree()
colors_central_nodes = ['red', 'green', 'yellow', 'blue', 'brown']
central_nodes = ['SkyBet', 'mrdanwalker', 'louiseminchin', 'RobBiddulph', 'BizBuzzHertford']
pos = nx.spring_layout(G_replies, k=0.05)
plt.figure(figsize = (20,20))
nx.draw(G_replies, pos=pos, node_color=range(1280), cmap=plt.get_cmap('Spectral'), edge_color="black", linewidths=0.5, node_size=100, alpha=0.6, with_labels=False)
nx.draw_networkx_nodes(G_replies, pos=pos, nodelist=central_nodes, node_size=600, node_color=colors_central_nodes, label=central_nodes)

legend_ele = [
    Line2D([0], [0], marker='o', color='w', label='SkyBet', markerfacecolor='red', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='mrdanwalker', markerfacecolor='green', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='louiseminchin', markerfacecolor='yellow', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='RobBiddulph', markerfacecolor='blue', markersize=10),
    Line2D([0], [0], marker='o', color='w', label='BizBuzzHertford', markerfacecolor='brown', markersize=10),
]
plt.legend(title="Highest centrality degree accounts", title_fontsize=20 ,loc="upper right", handles=legend_ele, prop={'size':20})
plt.savefig('graph_replies.png')
end = time.time()
print(f'Time to draw graph: {round(end - start)}')