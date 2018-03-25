#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 12:13:22 2018

@author: junshuaizhang
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
#X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
#pca = PCA(n_components=1)
#pca.fit(X)
#
#
#print(pca.explained_variance_ratio_)  
#reduced_x = pca.transform(X)
#print(X)
#print(reduced_x)
#
#np.savetxt("test.csv", reduced_x, delimiter=",")
#print(pca.singular_values_) 

 
start=datetime.now()
X = np.random.random((10, 5))
#print(X)
x = np.random.random((1,5))
x = np.array(x).reshape(1, -1)
nbrs = NearestNeighbors(n_neighbors=3, algorithm='auto').fit(X)
distances, indices = nbrs.kneighbors(x)

neighbor_list = [X[i] for i in indices][0]

similarity = cosine_similarity(x,neighbor_list)
similarity = sorted(similarity)
print(X)
print(x)
print(indices)
print(distances)
end = datetime.now()
print(end-start)