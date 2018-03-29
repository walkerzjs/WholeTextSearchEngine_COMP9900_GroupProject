#!/usr/bin/python3

import os, re, collections, datetime, operator
from flask import Flask, request, render_template, redirect, url_for, make_response, session
from werkzeug import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 4000

@app.route('/')
def hello_world():
    return redirect(url_for('home'))
	
@app.route('/home', methods=['GET','POST'])
def home():
	return render_template("home.html")

@app.route('/all/p<page>', methods=['GET','POST'])
def show_all(page):
	page = int(page)
	total = int(len(os.listdir("templates/NSW/")))
	articles = get_all_aritcles(page, total)
	
	return render_template("all.html", articles=articles, page=page, total=total)

@app.route('/showing/<link>', methods=['GET','POST'])
def showing_article(link):

    os.system("rm static/*.html")
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
		elif button == "upload_file":
			f = request.files['file']
			file_name = secure_filename(f.filename)
			f.save(file_name)
			os.system("mv " + file_name + " uploads/" + file_name)
			message = "Uploaded successfully!" 
					
	return render_template("upload.html", message=message)
	
@app.route('/search/<field>', methods=['GET','POST'])
def search(field):
	return render_template("home.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
def get_all_aritcles(page, total):

	list = os.listdir("templates/NSW/")
	articles = collections.OrderedDict()
	count = 1
    
	for i in sorted(list):
		if count > (page-1) * 100 and count <= page * 100:
			with open(os.path.join( "templates/NSW/", i )) as f:
				for line in f:
					if re.match("^<title>",line):
						line = re.sub("^<title>","",line)
						line = re.sub("<\/title>$","",line)
						line = re.sub("\n$","",line)
						# print(line+"\n")
						articles[i] = line
						break
		count += 1
		
	return articles
	
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1345)
