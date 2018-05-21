
import pickle

# load local file
def load_file(input_path):
    with open(input_path, 'rb') as file:
        x = pickle.load(file)
    return x

# save a file into local storage
def write_file(out_file, output_path):
    with open(output_path, 'wb') as file:
        pickle.dump(out_file, file)