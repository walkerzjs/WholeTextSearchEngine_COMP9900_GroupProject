# import modules.html_parser as html_parser, modules.vector_operator as vector_operator
# import glob
# import re
# hp= html_parser.html_parser()
# filenames = hp.load_filenames_not_first(path = "static/filenames")
# print(filenames)
#
# all_files = glob.glob("static/NSW/*.html")
# print(all_files)
#
# all_filenames = []
# for filename in all_files:
#     file_id = re.sub(r"^.*\/", "", filename)
#     file_id = re.sub("^.*[\\\\]", "", file_id)
#     print(file_id)
#
# import re
# filename = 'static/test.html'
# with open(filename,'r', encoding="ISO-8859-1") as f:
#     for line in f:
#         # print(line)
#         if re.match("^.*<title>.*", line):
#             line = re.sub("^.*<title>", "", line)
#             line = re.sub("<\/title>.*$", "", line)
#             line = re.sub("\n$", "", line)
#             print(line)

import re
from datetime import datetime
import glob
import modules.utilities as utilities
path = "static/filenames"
filenames = utilities.load_file(path)
name='NSWSC_2017_321.html'
for i in range(len(filenames)):
    file = filenames[i]
    if file[0] == name:

        print(filenames[i])