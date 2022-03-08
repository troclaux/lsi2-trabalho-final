from fileinput import filename
from ckan import *
import pandas as pd

#read csv from local directory with pandas
dataset1 = pd.read_csv("dataset1.csv", delimiter=";")
dataset2 = pd.read_csv("dataset2.csv", delimiter=";")


#function that counts the number of identical columns in two datasets
def countIdenticalColumns(dataset1, dataset2):
	#definir o número de colunas nos 2 datasets
	#comparar as colunas

	identicalColumns = 0
	columns1 = list(dataset1)
	columns2 = list(dataset2)
	numberOfColumnsDataset1 = len(columns1)
	numberOfColumnsDataset2 = len(columns2)
	for element1 in columns1:
		for element2 in columns2:
			if element1 == element2:
				identicalColumns = identicalColumns + 1
	
	return identicalColumns / min(numberOfColumnsDataset1, numberOfColumnsDataset2)

print(countIdenticalColumns(dataset1, dataset2))
