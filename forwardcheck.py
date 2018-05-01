import matplotlib.pyplot as plt
import networkx as nx
import random
import copy
import math

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

def UVERTEX(U,domains):

	candidates = []
	for node in U:
		if len(domains[node]) > 1:
			candidates.append(node)

	if len(candidates) >0:
		return candidates[random.randint(0,len(candidates)-1)]
	else:
		return U[random.randint(0,len(U)-1)]
	# print(candidates)

def CVERTEX(C,domains):

	candidates = []
	for node in C:
		if len(domains[node]) > 1:
			candidates.append(node)

	if len(candidates) >0:
		return candidates[random.randint(0,len(candidates)-1)]
	else:
		return C[random.randint(0,len(C)-1)]

# def CVERTEX(C,domains):

# 	candidates = []
# 	for node in C:
# 		# if len(domains[node]) > 1:
# 		candidates.append((node,len(domains[node])))

# 	max_domain = 0
# 	top_candidate = candidates[0]
# 	for candidate in candidates:
# 		if max_domain < candidate[1]:
# 			top_candidate = candidate
# 			max_domain = candidate[1]

# 	return top_candidate[0]
	# candidates_sorted = candidates.sort(lambda x: x[2])

	# if len(candidates) >0:
	# 	return candidates[random.randint(0,len(candidates)-1)]
	# else:
	# 	return C[random.randint(0,len(C)-1)]


def COLOR(D):

	return D[random.randint(0,len(D)-1)]

def wipesOut(G,u,domains,color,coloration):
	# print("color =",color)
	# print("domain",domains[u])
	domainsCopy = copy.deepcopy(domains)
	neighbors = list(G.neighbors(u))

	# if coloration[u] == 0:
	# 	return True
	# print(neighbors)
	for neighbor in neighbors:
		# print(neighbor,domainsCopy[neighbor])
		# if coloration[neighbor]!=0:
			# return True
		try:
			domainsCopy[neighbor].remove(color)
		except:
			print("Except")

		if(len(domainsCopy[neighbor])==0 and coloration[neighbor]==0):
			# print("TRUE")
			return True
	# print("FALSE")
	return False

def getD(G,u,domains,coloration):

	D = []
	# print("Domains u",domains[u])
	neighbor_colors = []

	for neighbor in G.neighbors(u):
		neighbor_colors.append(coloration[neighbor])

	for color in domains[u]:
		if not wipesOut(G,u,domains,color,coloration) and color not in neighbor_colors:
			D.append(color)

	return D


def FCNS(G,B,k):

	C = []
	U = list(G.nodes())
	domains = {}
	coloration = {}

	for node in U:
		domains[node] = list(range(1,k+1))
		coloration[node] = 0


	while len(U)!=0:
		print("ITERATE")

		u = UVERTEX(U,domains)
		D = getD(G,u,domains,coloration)
		# print("u",u)
		# print("D",D)

		print("u",u)
		print("C",C)
		print("U",U)
		print("Domains: ",domains)
		print("Coloration: ",coloration)

		if len(D) == 0:
			# Do shit
			print("No D ===================")
			for i in range(min(B,len(C))):
				print(C)
				print(U)
				print(domains)
				c = CVERTEX(C,domains)
				print(c)
				# uncolor c, update domains
				past_color = coloration[c]
				coloration[c] = 0

				neighbor_colors = []

				for neighbor in G.neighbors(c):

					neighbor_colors.append(coloration[neighbor])

					neighbor_colors2 = []

					for neighbor2 in G.neighbors(neighbor):
						neighbor_colors2.append(coloration[neighbor2])

						if past_color not in neighbor_colors2 and past_color not in domains[neighbor]:
							domains[neighbor].append(past_color)

				if past_color not in neighbor_colors:
					domains[c].append(past_color)

				C.remove(c)
				U.append(c)
				print("C",C)
				print("U",U)
			print("=======================")

		else:
			# color u to COLOR(D),update domains
			print("May D===================")
			print("D",D)
			color = COLOR(D)
			print("Color",color)
			coloration[u] = color
			# print()
			for neighbor in G.neighbors(u):
				try:
					domains[neighbor].remove(color)
				except:
					print("Except")
			domains[u].remove(color)

			C.append(u)
			U.remove(u)

			# Do Other Shit


	return coloration

def isValidColoring(G,coloring):

	# for color in coloring:

	for node in G.nodes():

		for neighbor in G.neighbors(node):

			if coloring[node] == coloring[neighbor]:
				print(node)
				print(neighbor)
				print(coloring[node])
				print(coloring[neighbor])
				return False

	return True

# G = loadGraph('toy1.txt')
# G = nx.Graph()
# G.add_edge(1,2)
# G.add_edge(1,3)
# G.add_edge(2,3)
# G.add_edge(2,4)
# G.add_edge(3,4)
# G.add_edge(1,5)
# G.add_edge(2,5)
# G.add_edge(3,5)
# G = loadGraph('dsjc500.1.col.txt')
G = loadGraph('le450_5a.col.txt')
# G = nx.gnm_random_graph(100,300,seed=10)
# G = nx.gnm_random_graph(8,18,seed=10)

GCopy = copy.deepcopy(G)
GViz = list(G.nodes())

# visualizeBasic(G)

# while True:
# 	print("===================================================================")
coloration = FCNS(G,1,5)
print(coloration)
	# if not isValidColoring(G,coloration):
		# break


# print("===================================================================")


color_vals = []

for key, value in coloration.items():
	print(key,value)
	color_vals.append(value)

chromatic_number = len(list(set(color_vals)))

print("Chromatic Number:",chromatic_number)

print("Valid coloring?",isValidColoring(G,coloration))
# # Graph Visualization


colors =[]
for node in GCopy:
	colors.append(coloration[node])

# # print(GViz)
# # print(independentSetList)
# print(colors)

plt.subplot(121)
labels={}
for node in GCopy.nodes():
	labels[node] = node

pos = nx.nx_agraph.graphviz_layout(GCopy)

nx.draw(GCopy,pos=pos,node_color=colors,labels=labels)
plt.show()