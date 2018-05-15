#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Wed Mar 28 11:48:58 2018
    
    @author: junshuaizhang
    """

import modules.html_parser as html_parser, modules.vector_operator as vector_operator
import modules.similarity_matcher as similarity_matcher
import numpy as np
import nltk, re
from collections import defaultdict
# nltk.download('wordnet')
from nltk.corpus import wordnet
hp= html_parser.html_parser()
vo = vector_operator.vector_operator()
sm = similarity_matcher.simi_matcher()

#pre-load reduced_vectors and filenames as well as models
all_filenames =  hp.load_filenames_not_first()
#all_files = hp.load_files_not_first()
vectorizer = vo.load_vectorizer()
reducer = vo.load_dim_red_model()
reduced_vectors = vo.load_reduced_vectors()
top_words = vo.load_all_top_words_not_first()
# #print(all_filenames)


def find_similarity(input, input_savepath = "static/reduced_vector", result_size = 200):
    input_parsed = hp.parse_input_text(input)
    input_vector = vo.transform_text_not_first_time(vectorizer, [input_parsed])
    input_reduced = vo.dim_reduction_not_first(input_vector, reducer, input_savepath)
    distances, indices, similarity = sm.simi_matching(input_reduced, reduced_vectors, result_size)
    current_result = sm.combine_fname_sim(all_filenames, similarity, indices,top_words)
    return current_result


# path = "/Users/junshuaizhang/UNSW/COMP9900/temp/static/vectorizer"
# filepath1 = "/Users/junshuaizhang/UNSW/COMP9900/temp/static/NSW/NSWSC_1993_1.html"
# filepath2 = "/Users/junshuaizhang/UNSW/COMP9900/temp/static/NSW/NSWSC_2002_952.html"
# filepath3 = "/Users/junshuaizhang/UNSW/COMP9900/temp/static/NSW/NSWSC_2002_618.html"
# filepath4 = "/Users/junshuaizhang/UNSW/COMP9900/temp/static/NSW/NSWSC_2002_56.html"
# vectorizer = vo.load_vectorizer(path = path)


#reffered to the answer of https://stackoverflow.com/questions/25217510/how-to-see-top-n-entries-of-term-document-matrix-after-tfidf-in-scikit-learn
# def get_top_words_one_gram(filepath, vectorizer, num = 100):
#     with open(filepath) as file:
#         input = file.read()
#         input_parsed = hp.parse_input_text(input)
#         words = re.split(" ",input_parsed)
#         # #print("input: {}".format(input_parsed))
#         # #print("words: {}".format(words))
#         indices = np.argsort(vectorizer.idf_)[::-1]
#         features = vectorizer.get_feature_names()
#         top_n = 10000
#         top_features = [features[i] for i in indices[:top_n]]
#         # #print(wordnet.synsets("word"))
#         words = set(words)
#         result = []
#         for feature in top_features:
#             if feature in words and wordnet.synsets(feature):
#                 result.append(feature)
#                 if len(result)==num:
#                     break
#         # #print(result)
#         return result

# referred to the answer of https://stackoverflow.com/questions/25217510/how-to-see-top-n-entries-of-term-document-matrix-after-tfidf-in-scikit-learn
#The function mainly extracts the top important words from the result produced by the TF-IDF algorithm.
# def get_top_words_two_gram(filepath, vectorizer, top_n=100):
#     features_by_gram = defaultdict(list)
#     for f, w in zip(vectorizer.get_feature_names(), vectorizer.idf_):
#         features_by_gram[len(f.split(' '))].append((f, w))
#     # #print(features_by_gram.items())
#     # #print(features_by_gram[2])
#     # for gram, features in features_by_gram.items():
#     #    top_features = sorted(features, key=lambda x: x[1], reverse=True)[:top_n]
#     #    top_features = [f[0] for f in top_features]
#     #    #print ('{}-gram top:'.format(gram), top_features)
#     with open(filepath) as file:
#         input = file.read()
#         input_parsed = hp.parse_input_text(input)
#         words = re.split(" ", input_parsed)
#         pairs = [words[i] + " " + words[i + 1] for i in range(len(words) - 1)]
#         # #print(pairs)
#
#         top_words = []
#         top_features = sorted(features_by_gram[2], key=lambda x: x[1], reverse=True)
#         for feature in top_features:
#             if feature[0] in pairs:
#                 top_words.append(feature[0])
#         # #print(top_words)
#         return top_words
# res1 = get_top_words_one_gram(filepath1, vectorizer)
# res2 = get_top_words_one_gram(filepath2, vectorizer)
# res3 = get_top_words_one_gram(filepath3, vectorizer)
# res4 = get_top_words_one_gram(filepath4, vectorizer)
#
# #print(res1)
# #print(res2)
# interc1 = [val for val in res1 if val in res2]
# interc2 = [val for val in res1 if val in res3]
# interc3 = [val for val in res1 if val in res4]
# #print(interc1)
# #print(interc2)
# #print(interc3[:10])
# #print([val for val in res2 if val in res3])
#['paintings', 'thailand', 'methadone', 'cavity', 'grams', 'tapes', 'ba', 'recordings'






# get_top_words_two_gram(filepath3, vectorizer)
# get_top_words_one_gram(filepath3, vectorizer)
# #print(all_filenames)
#all_files, all_filenames = hp.load_filenames_first()
#hp.parse_input_text("On 21 October 1993 Grahame James Daubney pleaded guilty before me to a charge on")
import os
# here = os.path.dirname(__file__)
# #print(here)

# result = vo.load_all_top_words_first()
# #print(result)
