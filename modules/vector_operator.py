from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
import modules.html_parser as html_parser
import modules.utilities as utilities
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet
import re, glob
import numpy as np

class vector_operator():

    # Using TF-IDF to fit all the HTML files and save the model to the local file
    def vectorize(self, outfile, path='static/vectorizer'):
        vectorizer = TfidfVectorizer(max_df=0.5, ngram_range=(1, 1),
                                     min_df=2, stop_words='english', max_features=10000)
        vectorizer.fit(outfile)
        utilities.write_file(vectorizer, path)
        return vectorizer

    # Load the fitted TF-IDF model from local file
    def load_vectorizer(self, path="static/vectorizer"):
        vectorizer = utilities.load_file(path)
        return vectorizer

    # using the fitted TF-IDF model to transform all the documents into vectors and save it to the local file
    def transform_text_first_time(self, vectorizer, file_list, path='static/vectors'):
        vectors = vectorizer.transform(file_list)
        utilities.write_file(vectors, path)
        return vectors

    # using the fitted TF-IDF model to transform one document, used when user input or upload text.
    def transform_text_not_first_time(self, vectorizer, text):
        vector = vectorizer.transform(text)
        return vector

    # load the vectors produced by TF-IDF from local file
    def load_vector(self, path='static/vectors'):
        vectors = utilities.load_file(path)
        return vectors

    # Transforming the sparse matrix produced by TF-IDF to the normal matrix,
    # then use PCA to reduce the dimension size of it.
    # Finally save the PCA model and the reduced matrix to the local files.
    def dim_reduction_first_time(self, vectors, n_components=1000, \
                                 path='static/PCA', \
                                 path_red='static/reduced_vectors'):
        vectors = vectors.toarray()
        pca = PCA(n_components=n_components)
        pca.fit(vectors)
        utilities.write_file(pca, path)
        reduced_vectors = pca.transform(vectors)
        utilities.write_file(reduced_vectors, path_red)
        return reduced_vectors

    # load the fitted PCA model from local file
    def load_dim_red_model(self, path='static/PCA'):
        reducer = utilities.load_file(path)
        return reducer

    # Do the dimension reduction using fitted PCA
    # This is for the transformation when the user upload or input text for similarity searching
    def dim_reduction_not_first(self, vector, reducer, path='static/reduced_vector'):
        vector = vector.toarray()
        reduced_vector = reducer.transform(vector)
        utilities.write_file(reduced_vector, path)
        return reduced_vector

    # Load the dimension-reduced matrix from local file
    def load_reduced_vectors(self, path='static/reduced_vectors'):
        reduced_vectors = utilities.load_file(path)
        return reduced_vectors

    # Acknowledgement: part of the function(extracting top important words) below reffered to the answer of https://stackoverflow.com/questions/25217510/how-to-see-top-n-entries-of-term-document-matrix-after-tfidf-in-scikit-learn
    # The function mainly extracts the top important words from the result produced by the TF-IDF algorithm. This function will only extract the 1-gram features.(words)
    def get_top_words_one_gram(self, filepath, indices, features, html_parser, num=100):
        with open(filepath, encoding="ISO-8859-1") as file:
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
        indices = np.argsort(vectorizer.idf_)[::-1]
        features = vectorizer.get_feature_names()
        all_files = glob.glob(path)
        all_file_topwords = []
        for filename in all_files:
            file_id = re.sub(r"^.*/", "", filename)
            file_id = re.sub("^.*[\\\\]", "", file_id)
            top_words = self.get_top_words_one_gram(filename, indices, features, hp)
            with open(filename) as f:
                all_file_topwords.append([file_id, top_words])

        utilities.write_file(all_file_topwords, save_path)
        return all_file_topwords

    # load all the top words produced by TF-IDF from local file.
    def load_all_top_words_not_first(self, path="static/all_file_topwords"):
        top_words = utilities.load_file(path)
        return top_words



