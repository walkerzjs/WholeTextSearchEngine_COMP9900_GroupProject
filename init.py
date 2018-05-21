
import modules.html_parser as html_parser, modules.vector_operator as vector_operator
import modules.similarity_matcher as similarity_matcher

hp= html_parser.html_parser()
vo = vector_operator.vector_operator()
sm = similarity_matcher.simi_matcher()


print("start to load filenames")
all_files, all_filenames = hp.load_filenames_first(path = "static/NSW/*.html",save_path="static/filenames")
print("start to load files")
files, all_files, all_filenames =hp.load_files_first(path = "static/NSW/*.html", savefile = "static/outfiles")
print("start fitting TF-IDF")
vectorizer = vo.vectorize(files,path="static/vectorizer")
print("start extracting top words from TF-IDF results")
vo.load_all_top_words_first(vectorizer)
print("start transforming text into vectors")
vectors = vo.transform_text_first_time(vectorizer, files, path = "static/vectors")
print("start reducing vectors dimensions")
reduced_vectors = vo.dim_reduction_first_time(vectors, 1000, path="static/PCA", path_red = "static/reduced_vectors")
print("init finished")
