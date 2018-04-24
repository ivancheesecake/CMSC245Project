import matplotlib.pyplot as plt
import networkx as nx

# inputfile = 'dsjc500.1.col.txt'
inputfile = 'toy1.txt'

G = nx.Graph();

with open("input/"+inputfile) as fp:

	line = fp.readline()

	while line:
		# print(line);

		if line[0] == 'e':
			tokens = line.strip().split(" ")
			G.add_edge(tokens[1],tokens[2])

		line = fp.readline()

coloring = nx.greedy_color(G,'largest_first');
# print(coloring)
chromatic_number = max(coloring.values())
plt.subplot(121)
# nx.draw(G, node_color=range(chromatic_number), cmap=plt.cm.Blues)

# print(G.nodes()
node_colors = [coloring[x] for x in G.nodes()]
labels={}
for node in G.nodes():
	labels[node] = node

print(node_colors)
nx.draw(G,labels=labels,cmap=plt.cm.gist_rainbow,node_color=node_colors,vmin=0,vmax=chromatic_number)
plt.show()


