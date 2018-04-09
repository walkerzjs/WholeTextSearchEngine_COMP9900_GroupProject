from sklearn.decomposition import TruncatedSVD
import numpy as np
import pickle

def load_file(input_path):
    with open(input_path, 'rb') as file:
        x = pickle.load(file)
    return x

def write_file(svd_model, output_path):
    with open(output_path, 'wb') as file:
        pickle.dump(svd_model, file)

def dimention_Reduction(input_path, output_svd_transform):
    svd = TruncatedSVD(n_components=1000, n_iter=7, random_state=42)
    x = load_file(input_path)
    y = svd.fit_transform(x)
    write_file(y, output_svd_transform)

# if __name__ == '__main__':
#     # dimention_Reduction('/Users/hc/Desktop/S1_2018/cs3900/searchengine/vectors', '/Users/hc/Desktop/S1_2018/cs3900/searchengine/svd_transform')
#     # x = load_file('/Users/hc/Desktop/S1_2018/cs3900/searchengine/svd_transform')
#     # print(x.shape)
