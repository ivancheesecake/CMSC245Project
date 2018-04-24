import matplotlib.pyplot as plt
import networkx as nx
import random
import copy

G = nx.gnm_random_graph(10,30)

plt.subplot(121)
# node_colors = [coloring[x] for x in G.nodes()]
labels={}
for node in G.nodes():
	labels[node] = node

# print(node_colors)
# nx.draw(G,labels=labels,cmap=plt.cm.gist_rainbow,node_color=node_colors,vmin=0,vmax=chromatic_number)
# pos = nx.nx_agraph.graphviz_layout(G)
nx.draw(G,labels=labels)
plt.show()