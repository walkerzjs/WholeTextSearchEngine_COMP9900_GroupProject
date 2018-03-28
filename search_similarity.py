
"""
Created on Tue Mar 20 12:13:22 2018

@author: junshuaizhang
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import sys
import codecs
import glob
import re
import pickle
from bs4 import BeautifulSoup as bs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pandas as pd
from operator import itemgetter

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
#existed_files = np.random.random((30000, 1000))
#uploaded_file = np.random.random((1,1000))


def simi_matching(uploaded_file, existed_files, neighbors=20):
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
    print(indices)
    print(distances)
    print(similarity)
    end = datetime.now()
    print(end-start)
    return distances, indices, similarity

#simi_matching(uploaded_file, existed_files)

def load_filenames(path="/Users/junshuaizhang/UNSW/COMP9900/NSWSC/*.html"):   
    all_files = glob.glob(path)
    all_filenames = [re.sub(r"^.*/","/",i) for i in all_files]
    return all_files, all_filenames
#
##file = open(all_files[0], "r")
##file = file.read()
#files = []
#for filename in all_files:
#    f=codecs.open(filename, 'r').read()
#    file = bs(f)
#    filetext = bs.get_text(file)
#    test = re.sub(r'\n','',filetext)
#    test = re.sub(r'\t','',test)
#    files.append(test)
#end = datetime.now()
#
#with open('outfile', 'wb') as fp:
#    pickle.dump(files, fp)


#load htmls and save to a file
def load_files(path="/Users/junshuaizhang/UNSW/COMP9900/NSWSC/*.html", savefile='outfile'):
    start=datetime.now()
    all_files = glob.glob("/Users/junshuaizhang/UNSW/COMP9900/NSWSC/*.html")
    all_filenames = [re.sub(r"^.*/","/",i) for i in all_files]
    
    #file = open(all_files[0], "r")
    #file = file.read()
    files = []
    for filename in all_files:
        f=open(filename, 'r').read()
        f = re.sub("<.*?>", " ", f)
        f = re.sub(r'\n',' ',f)
        f = re.sub(r'\t',' ',f)
        f = re.sub(r'[0-9]','',f)
        f = re.sub(r'\[','',f)
        f = re.sub(r'\]','',f)
        f = re.sub(r'[\.\(\)\:\|]','',f)
        f = re.sub(r'[\.\(\)\:\|\/\$\;\'\"\&\#\,]','',f)
        f = re.sub(r' +',' ',f)
        f = f.lower()     
        files.append(f)
    end = datetime.now()
    with open('outfile', 'wb') as fp:
        pickle.dump(files, fp)
    return files, all_files, all_filenames


def load_files_not_first(path = '/Users/junshuaizhang/UNSW/COMP9900/outfile'):
    with open (path, 'rb') as fp:
        files = pickle.load(fp)
    return files


def vectorize(outfile):
    vectorizer = TfidfVectorizer(max_df=0.5,
                                     min_df=2, stop_words='english',max_features=10000)
    vectorizer.fit(outfile)
    with open('/Users/junshuaizhang/UNSW/COMP9900/vectorizer', 'wb') as fp:
        pickle.dump(vectorizer, fp)
    return vectorizer


def load_vectorizer(filename="/Users/junshuaizhang/UNSW/COMP9900/vectorizer"):
    with open (filename, 'rb') as fp:
        vectorizer = pickle.load(fp)
    return vectorizer


def transform_text_first_time(vectorizer, file_list):
    
    vectors = vectorizer.transform(file_list)
    with open('/Users/junshuaizhang/UNSW/COMP9900/vectors', 'wb') as fp:
        pickle.dump(vectors, fp)
    return vectors

def transform_text_not_first_time(vectorizer, text):
    vector = vectorizer.transform(text)
    return vector
    


def load_vector(vec_path):
    
    with open ('/Users/junshuaizhang/UNSW/COMP9900/vectors', 'rb') as fp:
        vectors = pickle.load(fp)
    return vectors


def dim_reduction_first_time(vectors, n_components = 1000):
    svd = TruncatedSVD(n_components=n_components)
    svd.fit(vectors)
    with open('/Users/junshuaizhang/UNSW/COMP9900/TruncatedSVD', 'wb') as fp:
        pickle.dump(svd, fp)
    reduced_vectors = svd.transform(vectors) 
    with open('/Users/junshuaizhang/UNSW/COMP9900/reduced_vectors', 'wb') as fp:
        pickle.dump(reduced_vectors, fp)
    return reduced_vectors


def load_dim_red_model(path = '/Users/junshuaizhang/UNSW/COMP9900/TruncatedSVD'):
    with open (path, 'rb') as fp:
        reducer = pickle.load(fp)
    return reducer

 
def dim_reduction_not_first(vector,reducer):
    reduced_vector = reducer.transform(vector)
    with open('/Users/junshuaizhang/UNSW/COMP9900/reduced_vector', 'wb') as fp:
        pickle.dump(reduced_vector, fp)
    return reduced_vector


def load_reduced_vectors(path='/Users/junshuaizhang/UNSW/COMP9900/reduced_vectors'):
    with open (path, 'rb') as fp:
        reduced_vectors = pickle.load(fp)
    return reduced_vectors


#combine filename and cooresponding similarities, and sort by similarities in descending order.
#input are the results from function simi_matching
def combine_fname_sim(all_filenames, similarity,indices):
    all_filenames_pd = pd.DataFrame(all_filenames,columns=["filename"])
    similarity_pd = pd.DataFrame(similarity[0],columns=["similarity"])
    result_filenames = all_filenames_pd.iloc[indices[0]]
    result_filenames = result_filenames.reset_index(drop=True)
    result = result_filenames.join(similarity_pd)
    
    result.sort_values("similarity", inplace=True, ascending=False)
    result_array = np.array(result)
    return result_array


# files, all_files, all_filenames = load_files()
# vectorizer = vectorize(files)
# vectors = transform_text_first_time(vectorizer, files)
# #reduced_vectors = load_reduced_vectors()
# reduced_vectors = dim_reduction_first_time(vectors, n_components = 1000)

# distances, indices,similarity = simi_matching(reduced_vectors[501], reduced_vectors,100)
# result = combine_fname_sim(all_filenames, similarity,indices)
#print(end-start)

