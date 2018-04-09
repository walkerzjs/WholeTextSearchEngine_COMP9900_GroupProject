#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 11:26:08 2018

@author: junshuaizhang, Hossein
"""
import re
from datetime import datetime
import glob
import modules.utilities as utilities

class html_parser:
    
#    def load_filenames_first(self, path="/Users/junshuaizhang/UNSW/COMP9900/NSWSC/*.html"):   
#        all_files = glob.glob(path)
#        all_filenames = [re.sub(r"^.*/","/",i) for i in all_files]
##        with open('/Users/junshuaizhang/UNSW/COMP9900/filenames', 'wb') as fp:
##            pickle.dump(all_filenames, fp)
#
#        with open(os.path.join("templates/NSW/", i)) as f:
#            for line in f:
#        utilities.write_file(all_filenames, path)
#        return all_files, all_filenames
    def extract_html_title(self, f):
        for line in f:
            #print(line)
            if re.match("^<title>", line):
                line = re.sub("^<title>", "", line)
                line = re.sub("<\/title>$", "", line)
                line = re.sub("\n$", "", line)
                return line
        
    
    def load_filenames_first(self, path="static/NSW/*.html",
                         save_path = "static/filenames"):
        all_files = glob.glob(path)
        #all_filenames = [re.sub(r"^.*/","/",i) for i in all_files]
    #        with open('static/filenames', 'wb') as fp:
    #            pickle.dump(all_filenames, fp)
        all_filenames = []
        for filename in all_files:
            file_id = re.sub(r"^.*/","",filename)
            #print(filename)
            with open(filename) as f:
                title = self.extract_html_title(f)
                all_filenames.append([file_id, title])
                    
        utilities.write_file(all_filenames, save_path)
        return all_files, all_filenames
    
    def load_filenames_not_first(self, path = "static/filenames"):
#        with open (path, 'rb') as fp:
#            filenames = pickle.load(fp)
        filenames = utilities.load_file(path)
        return filenames
#
##file = open(all_files[0], "r")
##file = file.read()
#files = []
#for filename in all_files:
#    f=codecs.open(filename, 'r').read()
#    file = bs(f)
#    filetext = bs.get_text(file)
#    test = re.sub(r'\n','',filetext)
#    test = re.sub(r'\t','',test)
#    files.append(test)
#end = datetime.now()
#
#with open('outfile', 'wb') as fp:
#    pickle.dump(files, fp)

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
        #print(f)
        return f

    #load htmls and save to a file
    def load_files_first(self, path="static/NSW/*.html", savefile='static/outfile'):
        start=datetime.now()
        all_files = glob.glob(path)
        all_filenames = [re.sub(r"^.*/","",i) for i in all_files]
        
        #file = open(all_files[0], "r")
        #file = file.read()
        files = []
        for filename in all_files:
            f=open(filename, 'r').read()
            f = self.clean_file(f)
            files.append(f)
        end = datetime.now()
#        with open('outfile', 'wb') as fp:
#            pickle.dump(files, fp)
        utilities.write_file(files, savefile)
        return files, all_files, all_filenames
    
    def parse_input_text(self, input_text):
        #print("inpt: {}".format(input_text))
        f = self.clean_file(input_text)
        utilities.write_file(f,"static/input_cleaned_test")
        print("output: {}".format(f))
        return f
    
    def load_files_not_first(self, path = 'static/outfile'):
#        with open (path, 'rb') as fp:
#            files = pickle.load(fp)
        files = utilities.load_file(path)
        return files


# this function is extracting the content of an uncleaned txt file
# for example the content of the file that user uploaded
    def extract_fromTXT(path):

        #all_files = filenames(path)
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