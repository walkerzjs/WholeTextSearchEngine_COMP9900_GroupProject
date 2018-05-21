
import modules.html_parser as html_parser, modules.vector_operator as vector_operator
import modules.similarity_matcher as similarity_matcher
import numpy as np
import nltk, re
from collections import defaultdict
nltk.download('wordnet')
from nltk.corpus import wordnet
hp= html_parser.html_parser()
vo = vector_operator.vector_operator()
sm = similarity_matcher.simi_matcher()

#pre-load reduced_vectors and filenames as well as models
all_filenames =  hp.load_filenames_not_first()
vectorizer = vo.load_vectorizer()
reducer = vo.load_dim_red_model()
reduced_vectors = vo.load_reduced_vectors()
top_words = vo.load_all_top_words_not_first()

# find the similar documents with the input text
def find_similarity(input, input_savepath = "static/reduced_vector", result_size = 200):
    input_parsed = hp.parse_input_text(input)
    input_vector = vo.transform_text_not_first_time(vectorizer, [input_parsed])
    input_reduced = vo.dim_reduction_not_first(input_vector, reducer, input_savepath)
    distances, indices, similarity = sm.simi_matching(input_reduced, reduced_vectors, result_size)
    current_result = sm.combine_fname_sim(all_filenames, similarity, indices,top_words)
    return current_result

