#!/usr/bin/python3

import os, re, collections, datetime, operator
from flask import Flask, request, render_template, redirect, url_for, make_response, session


app = Flask(__name__)

@app.route('/')
def hello_world():
    return redirect(url_for('home'))
	
@app.route('/home', methods=['GET','POST'])
def home():
	return render_template("home.html")

@app.route('/all', methods=['GET','POST'])
def show_all():
	articles = get_all_aritcles()
	return render_template("all.html", articles = articles)

@app.route('/showing/<link>', methods=['GET','POST'])
def showing_article(link):
	# html = "NSW/" + link
	os.system("cp templates/NSW/" + link + " static/" + link)
	return render_template("showing.html", link = link)
	
	
@app.route('/upload', methods=['GET','POST'])
def upload():
	message = None
	if request.method == "POST":
		button = request.form.get("btn")
		if button == "upload_article":
			input = request.form["upload_new"]
			if re.match("\w",input):
				message = "Uploaded successfully!"
	return render_template("upload.html", message=message)
	
@app.route('/search/<field>', methods=['GET','POST'])
def search(field):
	return render_template("home.html")

def get_all_aritcles():
	list = os.listdir("templates/NSW/")
	articles = collections.OrderedDict()
	for i in sorted(list):
		with open(os.path.join( "templates/NSW/", i )) as f:
			for line in f:
				if re.match("^<title>",line):
					line = re.sub("^<title>","",line)
					line = re.sub("<\/title>$","",line)
					line = re.sub("\n$","",line)
					# print(line+"\n")
					articles[i] = line
					break
	return articles
	
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1234)
