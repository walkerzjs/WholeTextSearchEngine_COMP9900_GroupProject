#!/usr/bin/python3

import os, re, collections, datetime, operator
#change working dir
here = os.path.dirname(__file__)
#print(os.getcwd())
os.chdir(here)
#print(os.getcwd())
from flask import Flask, request, render_template, redirect, url_for, make_response, session
from werkzeug import secure_filename
import searchEngine_backend as se


app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 4000




global current_result
@app.route('/')
def hello_world():
    return redirect(url_for('home'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route('/all/p<page>', methods=['GET', 'POST'])
def show_all(page):
    page = int(page)
    total = int(len(os.listdir("static/NSW/")))
    #print(total)
    #print(page)
    articles = get_all_aritcles(page, total)

    return render_template("all.html", articles=articles, page=page, total=total)


@app.route('/showing/<link>', methods=['GET', 'POST'])
def showing_article(link):
    os.system("rm static/*.html")
    os.system("cp static/NSW/" + link + " static/" + link)
    return render_template("showing.html", link=link)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global current_result
    message = None
    if request.method == "POST":
        button = request.form.get("btn")

        if button == "upload_article":
            input = request.form["upload_new"]
            if re.match("\w", input):
                message = "Uploaded successfully!"
            #print(input)
            #print(type(input))
            #start to transform input text and compute similarities.

            #print("parsed: {}".format(input_parsed))
            #print(type(input_parsed))
            # input_parsed = se.hp.parse_input_text(input)
            # input_vector = se.vo.transform_text_not_first_time(se.vectorizer,[input_parsed])
            # input_reduced = se.vo.dim_reduction_not_first(input_vector, se.reducer,"static/reduced_vector")
            # distances, indices, similarity = se.sm.simi_matching(input_reduced,se.reduced_vectors,200)
            # current_result = se.sm.combine_fname_sim(se.all_filenames, similarity, indices)
            current_result = se.find_similarity(input, input_savepath = "static/reduced_vector", result_size = 200)
            #print(current_result[:,[0,2,1]])
            #print(input_parsed)
            return redirect(url_for('show_search_result',page = 1))
        elif button == "upload_file":
            f = request.files['file']

            print(f)
            file_name = secure_filename(f.filename)
            print(file_name)
            save_path = "static/uploaded_files/{}".format(file_name)
            f.save(save_path)
            input = ""
            with open(save_path) as file:
                input = file.read()
                print(input)
            current_result = se.find_similarity(input, input_savepath="static/uploaded_file_reduced_vector", result_size=200)
            #os.system("mv " + file_name + " uploads/" + file_name)
            message = "Uploaded successfully!"
            return redirect(url_for('show_search_result',page = 1))

    return render_template("upload.html", message=message)


@app.route('/search_result/p<page>', methods=['GET','POST'])
def show_search_result(page):
    global current_result
    page = int(page)
    #total = int(len(os.listdir("static/NSW/")))
    total = len(current_result)
    #articles = get_all_aritcles(page, total)
    articles = current_result[((page - 1) * 100):page * 100,[0,1,2]]
    #print(articles)
    return render_template("search_results.html", articles=articles, page=page, total=total)


@app.route('/search/<field>', methods=['GET', 'POST'])
def search(field):
    return render_template("home.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_all_aritcles(page, total):
    list = os.listdir("static/NSW/")
    #print(list)
    articles = collections.OrderedDict()
    count = 1

    for i in sorted(list):
        if count > (page - 1) * 100 and count <= page * 100:
            with open(os.path.join("static/NSW/", i)) as f:
                title = se.hp.extract_html_title(f)
                articles[i] = title
                #for line in f:

                    # if re.match("^<title>", line):
                    #     line = re.sub("^<title>", "", line)
                    #     line = re.sub("<\/title>$", "", line)
                    #     line = re.sub("\n$", "", line)
                    #     # print(line+"\n")
                    #     articles[i] = line
                    #     break
        count += 1
    #print(articles)
    return articles


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1345)
