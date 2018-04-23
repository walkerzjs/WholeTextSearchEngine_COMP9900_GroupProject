import os
import modules.html_parser as html_parser, modules.vector_operator as vector_operator
import modules.similarity_matcher as similarity_matcher

here = os.path.dirname(__file__)
print(here)

hp= html_parser.html_parser()
vo = vector_operator.vector_operator()
sm = similarity_matcher.simi_matcher()

all_files, all_filenames = hp.load_filenames_first(path = "static/NSW/*.html",save_path="static/filenames")
files, all_files, all_filenames =hp.load_files_first(path = "static/NSW/*.html", savefile = "static/outfiles")
vectorizer = vo.vectorize(files,path="static/vectorizer")
vo.load_all_top_words_first(vectorizer)
vectors = vo.transform_text_first_time(vectorizer, files, path = "static/vectors")
reduced_vectors = vo.dim_reduction_first_time(vectors, 1000, path_svd="static/TruncatedSVD", path_red = "static/reduced_vectors")


