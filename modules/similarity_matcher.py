
from datetime import datetime
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class simi_matcher:

    # find the similar documents to the uploaded file or input text.
    # Used NearestNeighbors API from scikit-learn
    def simi_matching(self, uploaded_file, existed_files, neighbors=20):
        start=datetime.now()
        uploaded_file = np.array(uploaded_file).reshape(1, -1)
        nbrs = NearestNeighbors(n_neighbors=neighbors, algorithm='auto').fit(existed_files)
        distances, indices = nbrs.kneighbors(uploaded_file)
        
        neighbor_list = [existed_files[i] for i in indices][0]
        
        similarity = cosine_similarity(uploaded_file, neighbor_list)
        end = datetime.now()
        return distances, indices, similarity
    
    # get the filename, title and top words with the similarity searching result.
    def combine_fname_sim(self, all_filenames, similarity,indices, all_top_words):
        all_filenames_pd = pd.DataFrame(all_filenames,columns=["filename","title"])
        all_top_words_pd = pd.DataFrame(all_top_words, columns=["filename", "top_words"])
        similarity_pd = pd.DataFrame(similarity[0],columns=["similarity"])
        result_filenames = all_filenames_pd.iloc[indices[0]]
        result_topwords = all_top_words_pd.iloc[indices[0]]
        result_topwords = result_topwords.reset_index(drop=True)
        result_filenames = result_filenames.reset_index(drop=True)
        result = result_filenames.join(similarity_pd)
        result = result.join(result_topwords.iloc[:,1])
        result.sort_values("similarity", inplace=True, ascending=False)
        result_array = np.array(result)
        return result_array
