#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:26:52 2018

@author: junshuaizhang
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import modules.utilities as utilities
class vector_operator():
        
    def vectorize(self, outfile, path ='static/vectorizer'):
        vectorizer = TfidfVectorizer(max_df=0.5,ngram_range=(1, 1),
                                         min_df=2, stop_words='english',max_features=10000)
        vectorizer.fit(outfile)
#        with open('static/vectorizer', 'wb') as fp:
#            pickle.dump(vectorizer, fp)
        utilities.write_file(vectorizer, path)
        return vectorizer
    
    
    def load_vectorizer(self, path="static/vectorizer"):
#        with open (filename, 'rb') as fp:
#            vectorizer = pickle.load(fp)
        vectorizer = utilities.load_file(path)
        return vectorizer
    
    
    def transform_text_first_time(self, vectorizer, file_list, path = 'static/vectors'):
        
        vectors = vectorizer.transform(file_list)
#        with open('static/vectors', 'wb') as fp:
#            pickle.dump(vectors, fp)
        utilities.write_file(vectors, path)
        return vectors
    
    def transform_text_not_first_time(self, vectorizer, text):
        vector = vectorizer.transform(text)
        return vector

    
    def load_vector(self, path='static/vectors'):
#        with open (vec_path, 'rb') as fp:
#            vectors = pickle.load(fp)
        vectors = utilities.load_file(path)
        return vectors
    
    def dim_reduction_first_time(self, vectors, n_components = 1000, \
                                 path_svd = 'static/TruncatedSVD',\
                                 path_red = 'static/reduced_vectors'):
        svd = TruncatedSVD(n_components=n_components)
        svd.fit(vectors)
#        with open('static/TruncatedSVD', 'wb') as fp:
#            pickle.dump(svd, fp)
        utilities.write_file(svd, path_svd)
        reduced_vectors = svd.transform(vectors) 
#        with open('static/reduced_vectors', 'wb') as fp:
#            pickle.dump(reduced_vectors, fp)
        utilities.write_file(reduced_vectors, path_red)
        return reduced_vectors
    
    
    def load_dim_red_model(self, path = 'static/TruncatedSVD'):
#        with open (path, 'rb') as fp:
#            reducer = pickle.load(fp)
        reducer = utilities.load_file(path)
        return reducer
    
     
    def dim_reduction_not_first(self, vector,reducer, path = 'static/reduced_vector'):
        reduced_vector = reducer.transform(vector)
#        with open('static/reduced_vector', 'wb') as fp:
#            pickle.dump(reduced_vector, fp)
        utilities.write_file(reduced_vector, path)
        return reduced_vector
    
    
    def load_reduced_vectors(self, path='static/reduced_vectors'):
#        with open (path, 'rb') as fp:
#            reduced_vectors = pickle.load(fp)
        reduced_vectors = utilities.load_file(path)
        return reduced_vectors