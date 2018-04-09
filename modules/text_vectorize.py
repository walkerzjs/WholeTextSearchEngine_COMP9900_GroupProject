from sklearn.feature_extraction.text import TfidfVectorizer



# this function is used to create a matrix of tf-idf vectors all document
# mostly used for initial run of the app

def vectorise_All(contents_list):

    vectoriser = TfidfVectorizer(analyzer='word', ngram_range=(1, 6), min_df = 0.5, stop_words='english', sublinear_tf=True, max_features=10000)
    vectoriser.fit(contents_list)
    vectors_matrix = vectoriser.transform(contents_list)

    # print(vector.shape)
    # print("Vocabulary: {}".format(vectoriser.vocabulary_))
    # print(vector.toarray())

    with open('vectorizer', 'wb') as output:
            pickle.dump(vectors_matrix, output)

    return vectors_matrix

# this function is used for the file that user uploaded

def vectorise_file(file):

    vectoriser = TfidfVectorizer(analyzer='word', ngram_range=(1, 6), min_df = 0.5, stop_words='english', sublinear_tf=True, max_features=10000)
    vectoriser.fit(file)
    vector_matrix = vectoriser.transform(file)

    return vector_matrix
