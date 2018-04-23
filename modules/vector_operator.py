#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:26:52 2018

@author: junshuaizhang
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import modules.html_parser as html_parser
import modules.utilities as utilities
from collections import defaultdict
from nltk.corpus import wordnet
import re, glob, os
import numpy as np


class vector_operator():

    def vectorize(self, outfile, path='static/vectorizer'):
        vectorizer = TfidfVectorizer(max_df=0.5, ngram_range=(1, 1),
                                     min_df=2, stop_words='english', max_features=10000)
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

    def transform_text_first_time(self, vectorizer, file_list, path='static/vectors'):

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

    def dim_reduction_first_time(self, vectors, n_components=1000, \
                                 path_svd='static/TruncatedSVD', \
                                 path_red='static/reduced_vectors'):
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

    def load_dim_red_model(self, path='static/TruncatedSVD'):
        #        with open (path, 'rb') as fp:
        #            reducer = pickle.load(fp)
        reducer = utilities.load_file(path)
        return reducer

    def dim_reduction_not_first(self, vector, reducer, path='static/reduced_vector'):
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

    # reffered to the answer of https://stackoverflow.com/questions/25217510/how-to-see-top-n-entries-of-term-document-matrix-after-tfidf-in-scikit-learn
    def get_top_words_one_gram(self, filepath, indices, features, html_parser, num=100):
        with open(filepath) as file:
            input = file.read()
            input_parsed = html_parser.parse_input_text(input)
            words = re.split(" ", input_parsed)
            # print("input: {}".format(input_parsed))
            # print("words: {}".format(words))

            top_n = 10000
            top_features = [features[i] for i in indices[:top_n]]
            # print(wordnet.synsets("word"))
            words = set(words)
            result = []
            for feature in top_features:
                if feature in words and wordnet.synsets(feature):
                    result.append(feature)
                    if len(result) == num:
                        break
            # print(result)
            return result

    # use after the vectorizer has been trained
    # top words one gram
    def load_all_top_words_first(self, vectorizer, path="static/NSW/*.html", save_path="static/all_file_topwords"):
        hp = html_parser.html_parser()
        # vectorizer = self.load_vectorizer()
        indices = np.argsort(vectorizer.idf_)[::-1]
        features = vectorizer.get_feature_names()
        all_files = glob.glob(path)
        # all_filenames = [re.sub(r"^.*/","/",i) for i in all_files]
        #        with open('static/filenames', 'wb') as fp:
        #            pickle.dump(all_filenames, fp)
        all_file_topwords = []
        for filename in all_files:
            file_id = re.sub(r"^.*/", "", filename)
            # print(filename)
            top_words = self.get_top_words_one_gram(filename, indices, features, hp)
            with open(filename) as f:
                all_file_topwords.append([file_id, top_words])

        utilities.write_file(all_file_topwords, save_path)
        return all_file_topwords

    def load_all_top_words_not_first(self, path="static/all_file_topwords"):
        top_words = utilities.load_file(path)
        return top_words



