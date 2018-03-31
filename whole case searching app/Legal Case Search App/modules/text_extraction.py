import os
import re
import pickle

def filenames(path):
    fileslist = os.listdir(path)
    return fileslist

# this function get a path as an input and does the following:
#   1 - create a clean text file for each html file in the path
#   2 - create a dump file for a list of all file content (clean content)
#   3 - return all file names in the list and all file contents
def convertAll_ToTXT(path):

    # Loading all files in the provided path
    all_files = filenames(path)

    # reading the content of all files, clean them, convert to lower case
    for filename in all_files:
        with open(os.path.join(path, filename)) as file:
            content = file.read()
        content = re.sub(r"<.*?>", "", content)
        content = re.sub(r"\n", " " , content)
        content = re.sub(r"\t", " ", content)

        content = re.sub(r"[0-9]", " ", content)
        content = re.sub(r"\[|\]", " ", content)
        content = re.sub(r"[\.\(\)\:\|]"," ", content)
        content = re.sub(r"[\.\(\)\:\|\/\$\;\"\"\&\#\,]", " ", content)
        #content = re.sub(r" *+ *"," ",content)
        content = re.sub(r" +", " ", content)
        content = content.lower()

        # create a filename for .txt
        new_file = re.sub(r".html", ".txt", filename)

        # Create a clean TXT file for each html file
        with open(os.path.join(path, new_file), "w") as file:
            file.write(new_content)

        # dump the list of all file Contents
        with open('all_Contents', 'wb') as output:
            pickle.dump(files_content, output)


# this function get a path as an input and does the following:
#   1 - Note that this function does not create a txt files
#   2 - create a dump file for a list of all file content (clean content)
#   3 - return all file names in the list and all file contents
def extractAll_formHTML(path):

    all_files = filenames(path)
    files_content = []

    for filename in all_files:
        with open(os.path.join(path, filename)) as file:
            content = file.read()
        content = re.sub(r"<.*?>", "", content)
        content = re.sub(r"\n", " " , content)
        content = re.sub(r"\t", " ", content)
        content = re.sub(r" +", " ", content)
        content = re.sub(r"[0-9]", " ", content)
        content = re.sub(r"\[|\]", " ", content)
        content = re.sub(r"[\.\(\)\:\|]"," ", content)
        content = re.sub(r"[\.\(\)\:\|\/\$\;\"\"\&\#\,]", " ", content)
        content = re.sub(r" *+ *"," ",content)
        content = content.lower()
        files_content.append(content)

        with open('all_Contents', 'wb') as output:
            pickle.dump(files_content, output)

    return files_content, filename


# this function is extracting the content of an uncleaned txt file
# for example the content of the file that user uploaded
def extract_fromTXT(path):

    all_files = filenames(path)
    files_content = []

    for filename in all_files:
        with open(os.path.join(path, filename)) as file:
            content = file.read()
        content = re.sub(r"<.*?>", "", content)
        content = re.sub(r"\n", " " , content)
        content = re.sub(r"\t", " ", content)

        content = re.sub(r"[0-9]", " ", content)
        content = re.sub(r"\[|\]", " ", content)
        content = re.sub(r"[\.\(\)\:\|]"," ", content)
        content = re.sub(r"[\.\(\)\:\|\/\$\;\"\"\&\#\,]", " ", content)
        #content = re.sub(r" *+ *"," ",content)
        content = re.sub(r" +", " ", content)
        content = content.lower()

        files_content.append(content)

    return files_content, filename
