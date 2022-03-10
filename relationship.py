from fileinput import filename
from ckan import *
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import networkx as nx

#read csv from local directory with pandas
dataset1 = pd.read_csv("dataset1.csv", delimiter=";")
dataset2 = pd.read_csv("dataset2.csv", delimiter=";")
dataset3 = pd.read_csv("dataset3.csv", delimiter=";")

lista = [dataset1, dataset2, dataset3]

datasetQueryResults = [{"name": "dataset1", "csv": dataset1}, {
	"name": "dataset2", "csv": dataset2}, {"name": "dataset3", "csv": dataset3}]

#function that counts the number of identical columns in two datasets


def countIdenticalColumns(dataset1, dataset2):
	#definir o número de colunas nos 2 datasets
	#comparar as colunas
	identicalColumns = 0
	#print(dataset1)
	columns1 = list(dataset1)
	columns2 = list(dataset2)
	for element1 in columns1:
		for element2 in columns2:
			if element1 == element2:
				identicalColumns = identicalColumns + 1
	return identicalColumns


def getRelationshipPercentage(dataset1, dataset2):
	columns1 = list(dataset1)
	columns2 = list(dataset2)
	razao = countIdenticalColumns(dataset1, dataset2) / min(len(columns1), len(columns2))
	arredondamento = round(razao, 2)
	return arredondamento

#print(countIdenticalColumns(dataset1, dataset2))
#print(getRelationshipPercentage(dataset1, dataset2))



#print(datasetQueryResults)
#create graph


def createGraph(datasets):

	G = nx.Graph()
	i = 0

	#TODO: nomear os nos com os nomes dos datasets

	for dataset in datasets:
		G.add_node(dataset["name"]) #, pos = (i,i)
		i = i+1

	#for node in G:
	#	for neighbor in G:
	#		if node == neighbor:
	#			continue
	#		weight = countIdenticalColumns(node, neighbor)
	#		if weight > 0:
	#			G.add_edge(node, neighbor, weight=weight)

	for node in datasets:
		for neighbor in datasets:
			if node == neighbor:
				continue
			weight = getRelationshipPercentage(node["csv"], neighbor["csv"])
			if weight > 0:
				G.add_edge(node["name"], neighbor["name"], weight=weight)

	return G

#declaracao do grafo
G = createGraph(datasetQueryResults)
#define posicao dos nos em um grafo circular
pos=nx.circular_layout(G, scale=1, center=None, dim=2)
#constroi conexoes entre os nos
nx.draw(G, pos)
#atribui pesos nas arestas
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
#mostra o grafo na janela
plt.show()

print(G.nodes)
print(G.edges)

print(G.number_of_nodes())
print(G.number_of_edges())
