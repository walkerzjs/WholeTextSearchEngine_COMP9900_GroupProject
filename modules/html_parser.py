
import re
from datetime import datetime
import glob
import modules.utilities as utilities


class html_parser:
    
    # extract html title, if title cannot be extracted, then output "Unknown Title"
    def extract_html_title(self, f):
        for line in f:
            if re.match("^.*<title>.*", line):
                line = re.sub("^.*<title>", "", line)
                line = re.sub("<\/title>.*$", "", line)
                line = re.sub("\n$", "", line)
                return line

        return "Unknown Title"

    # load filenames and save it in the local storage, if file cannot be extracted title, then ignore it.
    def load_filenames_first(self, path="static/NSW/*.html",
                         save_path = "static/filenames"):
        all_files = glob.glob(path)
        all_filenames = []
        count = 0
        for filename in all_files:
            file_id = re.sub(r"^.*\/","",filename)
            file_id = re.sub("^.*[\\\\]", "", file_id)

            with open(filename, 'r', encoding="ISO-8859-1") as f:
                title = self.extract_html_title(f)
                if title == 'Unknown Title':
                    continue
                all_filenames.append([file_id, title])

            count+=1
        utilities.write_file(all_filenames, save_path)
        return all_files, all_filenames

    # read filenames from local file.
    def load_filenames_not_first(self, path = "static/filenames"):
        filenames = utilities.load_file(path)
        return filenames

    # remove unnecessary symbols and numbers from the document as well as lowering the case.
    def clean_file(self, f):
        f = re.sub("<.*?>", " ", f)
        f = re.sub(r'\n',' ',f)
        f = re.sub(r'\t',' ',f)
        f = re.sub(r'[0-9]',' ',f)
        f = re.sub(r'\[',' ',f)
        f = re.sub(r'\]',' ',f)
        f = re.sub(r'\-', ' ', f)
        f = re.sub(r'[\>\<]', ' ', f)
        f = re.sub(r'[\.\(\)\:\|]',' ',f)
        f = re.sub(r'[\.\(\)\:\|\/\$\;\'\"\&\#\,]',' ',f)
        f = re.sub(r' +',' ',f)
        f = f.lower()
        return f

    # load html contents and save them to a file
    def load_files_first(self, path="static/NSW/*.html", savefile='static/outfile'):
        start=datetime.now()
        all_files = glob.glob(path)
        all_filenames = [re.sub(r"^.*/","",i) for i in all_files]
        files = []
        count=0
        for filename in all_files:
            with open(filename, 'r', encoding="ISO-8859-1") as f:
                title = self.extract_html_title(f)
                if title == 'Unknown Title':
                    #print(filename)
                    continue
                f.close()
            f=open(filename, 'r', encoding="ISO-8859-1").read()
            f = self.clean_file(f)
            files.append(f)
            count+=1
        end = datetime.now()
        utilities.write_file(files, savefile)
        return files, all_files, all_filenames


    def parse_input_text(self, input_text):
        f = self.clean_file(input_text)
        utilities.write_file(f,"static/input_cleaned_test")
        return f

    # local all file contents from the local file system
    def load_files_not_first(self, path = 'static/outfile'):
        files = utilities.load_file(path)
        return files


# # this function is extracting the content of an uncleaned txt file
# # for example the content of the file that user uploaded
#     def extract_fromTXT(path):
#
#         #all_files = filenames(path)
#         files_content = []
#
#         for filename in all_files:
#             with open(os.path.join(path, filename)) as file:
#                 content = file.read()
#             content = re.sub(r"<.*?>", "", content)
#             content = re.sub(r"\n", " " , content)
#             content = re.sub(r"\t", " ", content)
#
#             content = re.sub(r"[0-9]", " ", content)
#             content = re.sub(r"\[|\]", " ", content)
#             content = re.sub(r"[\.\(\)\:\|]"," ", content)
#             content = re.sub(r"[\.\(\)\:\|\/\$\;\"\"\&\#\,]", " ", content)
#             #content = re.sub(r" *+ *"," ",content)
#             content = re.sub(r" +", " ", content)
#             content = content.lower()
#
#             files_content.append(content)
#
#         return files_content, filename