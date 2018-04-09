#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:28:18 2018

@author: junshuaizhang
"""
from datetime import datetime
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class simi_matcher:

    def simi_matching(self, uploaded_file, existed_files, neighbors=20):
        start=datetime.now()
        
        #print(X)
        
        uploaded_file = np.array(uploaded_file).reshape(1, -1)
        nbrs = NearestNeighbors(n_neighbors=neighbors, algorithm='auto').fit(existed_files)
        distances, indices = nbrs.kneighbors(uploaded_file)
        
        neighbor_list = [existed_files[i] for i in indices][0]
        
        similarity = cosine_similarity(uploaded_file, neighbor_list)
        #similarity = sorted(similarity)
        #print(X)
        #print(x)
        #print(indices)
        #print(distances)
        #print(similarity)
        end = datetime.now()
        #print(end-start)
        return distances, indices, similarity
    
    
    def combine_fname_sim(self, all_filenames, similarity,indices):
        all_filenames_pd = pd.DataFrame(all_filenames,columns=["filename","title"])
        similarity_pd = pd.DataFrame(similarity[0],columns=["similarity"])
        result_filenames = all_filenames_pd.iloc[indices[0]]
        result_filenames = result_filenames.reset_index(drop=True)
        result = result_filenames.join(similarity_pd)
        result.sort_values("similarity", inplace=True, ascending=False)
        result_array = np.array(result)
        return result_array