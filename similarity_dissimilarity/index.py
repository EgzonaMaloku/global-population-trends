import pandas as pd
from scipy.spatial.distance import euclidean, minkowski
from sklearn.metrics import jaccard_score
import numpy as np


data = pd.read_csv('../data/dataset_05.csv')

# Eucledian
def euclidean_distance(point1, point2):
    return euclidean([point1], [point2])
    

# Minkowski
def minkowski_distance(point1, point2, p):
    return minkowski([point1], [point2], p)


# SMC Function
def simple_matching_coefficient(data1, data2):
    binary_data1 = (data1 > 0).astype(int)
    binary_data2 = (data2 > 0).astype(int)

    matches = sum(binary_data1 == binary_data2)
    total = len(data1)
    return matches / total


# Jaccard Index Function
def jaccard_index(data1, data2):
    binary_data1 = (data1 > 0).astype(int)
    binary_data2 = (data2 > 0).astype(int)

    intersection = sum((binary_data1 & binary_data2))
    union = sum((binary_data1 | binary_data2))
    return intersection / union if union != 0 else 0





euclidean_ = euclidean_distance(data['Population'].iloc[0], data['Population'].iloc[1])

minkowski_ = minkowski_distance(data['Median Age'].iloc[0], data['Median Age'].iloc[1], 3)


smc = simple_matching_coefficient(data['Annual_Population_Growth'], data['Migrants (net)'])

jaccard = jaccard_index(data['Annual_Population_Growth'], data['Migrants (net)'])

jaccard_dissimilarity = 1 - jaccard


print('Euclidean Distance for Population: ' + str(euclidean_))

print('Minkowski Distance for Median Age: ' + str(minkowski_))

print('Jaccard Index(Similarity) for Annual_Population_Growth and Migrants (net): ' + str(jaccard))

print('Jaccard Dissimilarity for Annual_Population_Growth and Migrants (net): ' + str(jaccard_dissimilarity))

print('SMC for Annual_Population_Growth and Migrants (net): ' + str(smc))

