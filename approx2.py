import matplotlib.pyplot as plt
import networkx as nx
import random
import copy
import math
import time

def visualizeBasic(G):

	plt.subplot(121)
	labels={}
	for node in G.nodes():
		labels[node] = node

	# pos = nx.nx_agraph.graphviz_layout(GCopy)

	nx.draw(G,labels=labels)
	plt.show()


def loadGraph(inputfile):

	G = nx.Graph();

	with open("input/"+inputfile) as fp:

		line = fp.readline()

		while line:

			if line[0] == 'e':
				tokens = line.strip().split(" ")
				G.add_edge(tokens[1],tokens[2])

			line = fp.readline()

	return G



def ramsey(G):

	if len(list(G.nodes())) == 0:
		return (nx.Graph(),nx.Graph())
	else:
		nodes = list(G.nodes())
		v = nodes[random.randint(0,len(nodes)-1)]

		# all_neighbors_iter = nx.all_neighbors(G,v)
		# non_neighbors_iter = nx.non_neighbors(G,v)

		all_neighbors = copy.deepcopy(G)
		non_neighbors = copy.deepcopy(G)

		# Non-neighbor graph
		for neighbor in nx.all_neighbors(G,v):
			non_neighbors.remove_node(neighbor)
		non_neighbors.remove_node(v)

		# Neighbor graph
		for nonneighbor in nx.non_neighbors(G,v):
			all_neighbors.remove_node(nonneighbor)
		all_neighbors.remove_node(v)

		c1,i1 = ramsey(all_neighbors)
		c2,i2 = ramsey(non_neighbors)

		if len(list(c1.nodes()))+1 >= len(list(c2.nodes())):
			c1.add_node(v)
			c = copy.deepcopy(c1)
		else:
			c = copy.deepcopy(c2)

		if len(list(i1.nodes())) >= len(list(i2.nodes()))+1:
			i = copy.deepcopy(i1)
		else:
			i2.add_node(v)
			i = copy.deepcopy(i2)

		return (c,i)

def ramsey2(G):

	if len(list(G.nodes())) == 0:
		return (nx.Graph(),nx.Graph())
	else:
		nodes = list(G.nodes())
		v = nodes[random.randint(0,len(nodes)-1)]

		# all_neighbors = copy.deepcopy(G)
		# non_neighbors = copy.deepcopy(G)

		all_neighbors_list = []
		non_neighbors_list = []

		# for neighbor in nx.all_neighbors(G,v):
		# 	all_neighbors_list.append(neighbor)
		# all_neighbors_list.append(v)

		# for neighbor in nx.non_neighbors(G,v):
		# 	non_neighbors_list.append(neighbor)
		# non_neighbors_list.append(v)

		# Non-neighbor graph
		all_neighbors = G.subgraph(list(nx.all_neighbors(G,v)))
		non_neighbors = G.subgraph(list(nx.non_neighbors(G,v)))


		# print(v)
		# print((list(nx.all_neighbors(G,v)).append(v)))
		# print(all_neighbors.nodes())
		# print(non_neighbors.nodes())
		# print(G.subgraph(list(nx.all_neighbors(G,v))).nodes())
		# print(all_neighbors.nodes())
		# print(list(nx.all_neighbors(G,v)).append(v))
		# Neighbor graph
		# for nonneighbor in nx.non_neighbors(G,v):
		# 	all_neighbors.remove_node(nonneighbor)
		# all_neighbors.remove_node(v)


		c1,i1 = ramsey2(all_neighbors)
		c2,i2 = ramsey2(non_neighbors)

		if len(list(c1.nodes()))+1 >= len(list(c2.nodes())):
			c1.add_node(v)
			c = copy.deepcopy(c1)
		else:
			c = copy.deepcopy(c2)

		if len(list(i1.nodes())) >= len(list(i2.nodes()))+1:
			i = copy.deepcopy(i1)
		else:
			i2.add_node(v)
			i = copy.deepcopy(i2)

		return (c,i)

def CliqueRemoval(G):

	GCopy = copy.deepcopy(G)
	idx = 1;

	c,i = ramsey(GCopy)

	c_set = [c]
	i_set = [i]

	while len(list(GCopy.nodes())) > 0:
		# print(len(list(GCopy.nodes())))

		for node in c.nodes():
			GCopy.remove_node(node)
		# print(G.nodes())

		idx += 1

		c,i = ramsey(GCopy)

		c_set.append(c)
		i_set.append(i)

	max_i = nx.Graph()
	# print(i_set)

	for out_i in i_set:
		print("ITERATING, BITCH!")
		print(out_i.nodes())
		if len(max_i.nodes()) < len(out_i.nodes()):
			max_i = copy.deepcopy(out_i)
			# print("HEY",max_i.nodes())
		# print(len(out_i.nodes()))
		# print(max_i)
	return max_i;


def isIndependent(I):
	if len(I.edges())>0:
		return False
	return True

def pickMe(G,ISize):
	# print("Pick Me")
	GCopy = G.copy()
	# print(GCopy.nodes())
	INodes = []

	# GCopy2 = copy.deepcopy(G)
	nodes = list(GCopy.nodes())

	# if len(INodes) == 0:

	for i in range(ISize):
		x = random.randint(0,len(nodes)-1)
		# print(x)
		pick = nodes[x]
		INodes.append(pick)
		nodes.remove(pick)


	return GCopy.subgraph(INodes)

def nayana(G,I):

	GCopy = copy.deepcopy(G)
	INodes = list(I.nodes())

	neighbors = []

	for node in INodes:

		neighbors += list(GCopy.neighbors(node))
		GCopy.remove_node(node)
	GCopy.remove_nodes_from(neighbors)

	return GCopy



def SampleIS(G,n,k):
	# print(n,k)
	GSize = G.number_of_nodes()
	# n = GSize
	# n = G.number_of_nodes()
	if GSize <= 1:
		return G, True
	else:
		while True:
			ISize = int(math.log(n,k))
			I = pickMe(G,ISize)
			# print("Pick me, pick me", I.nodes())

			if isIndependent(I):
				NBar = nayana(G,I)
				# print("IsIndepentent",NBar.nodes())
				# print(n)
				if NBar.number_of_nodes() >= int((n/k) * (math.log(n/2,2) * (math.log(math.log(n,2),2)))):

					sampleis, go =  SampleIS(NBar,n,k)

					if go:

						return nx.union(I, sampleis), True
					else:
						break

					# else:
					# 	break
						# return nx.Graph(),False


				else:
					I2 = nx.union(CliqueRemoval(NBar),I)
					# print(I2.nodes())
					# print((math.log(n,2)**3)/(6*math.log(math.log(n,2),2)))
					if I2.number_of_nodes() >= int((math.log(n/6,2)**3)*(math.log(math.log(n,2),2))):

						# I2_2 = I2.copy()

						# intersect = nx.intersection(I,I2)
						# for node in list(intersect.nodes()):
							# I2_2.remove_node(node)

						nodesI = list(I.nodes())
						nodesI2 = list(I2.nodes())
						intersection = set(nodesI) & set(nodesI2)

						I2_2 = copy.deepcopy(I2)
						for node in list(intersection):
							I2_2.remove_node(node)

						return nx.union(I,I2_2), True
					else:
						print("NOT GOOD.")
						return nx.Graph(),False
			# else:
				# print("DI MAKAMOVEON")
	return nx.Graph(),False

def coloring(G,k):

	GCopy = G.copy()
	output = {}
	i = 0

	while GCopy.number_of_nodes() > 0:
		print("Nodes",GCopy.nodes())
		# print("Number",GCopy.number_of_nodes())
		j = 1
		valid = False

		# while j<1000:
		# print("Trial", j)
		IS,valid = SampleIS(GCopy,GCopy.number_of_nodes(),k)
		j+=1

		if not valid:
			return ouput
		# print("IS",IS.nodes())
		# if not valid:
		# 	break

		for node in list(IS.nodes()):
			output[node] = i
			GCopy.remove_node(node)

		i += 1

	return output



# G = loadGraph('toy1.txt')
G = loadGraph('dsjc500.1.col.txt')
# G = nx.gnm_random_graph(50,100,seed=10)
GCopy = copy.deepcopy(G)
GViz = list(G.nodes())

# while True:
t0 =  time.time()
# print(list(nx.non_neighbors(G,'1')))
# print(ramsey(G)[0].nodes())
# print(SampleIS(G,G.number_of_nodes(),20)[0].nodes())
print(CliqueRemoval(G).nodes())
t1 = time.time()

print("Time Elapsed", t1-t0)

# print(G.edges())
# print(G.subgraph(['1','2','3']).edges())



# print(len(G.edges()))

# visualizeBasic(G)
# print(SampleIS(G,2)[0].nodes())
# coloring_output = coloring(G,3)
# print(coloring_output)

# colors =[]
# for node in GCopy:
# 	colors.append(coloring_output[node])

# # print(GViz)
# # print(independentSetList)
# print(colors)

# # Graph Visualization

# plt.subplot(121)
# labels={}
# for node in GCopy.nodes():
# 	labels[node] = node

# pos = nx.nx_agraph.graphviz_layout(GCopy)

# nx.draw(GCopy,pos=pos,node_color=colors)
# plt.show()