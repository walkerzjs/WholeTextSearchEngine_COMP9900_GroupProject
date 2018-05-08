#!/usr/bin/python3

import os, re, collections, datetime, operator, random
#change working dir
here = os.path.dirname(__file__)
#print(os.getcwd())
#os.chdir(here)
#print(os.getcwd())
from flask import Flask, request, render_template, redirect, url_for, make_response, session
from werkzeug import secure_filename
import searchEngine_backend as se
import csv
import modules.keyword_search as keyword_search

app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 4000


global logged

global current_result
# @app.route('/')
# def hello_world():
#     return redirect(url_for('home'))


@app.route('/', methods = ["GET","POST"])
@app.route('/login', methods = ["GET","POST"])
def login():
    global logged
    user = None
    err_msg = request.args.get('err_msg')

    if logged:  return redirect(url_for('home'))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            err_msg = "Username and password field cannot be empty"
        else:
            user = authentication(username, password)

            if user is not None:
                login_id = username
                logged = True
                return redirect(url_for('home'))
            else:
                login_id = None
                err_msg = "Incorrect username or password."
    return render_template("login.html", err_msg=err_msg)


@app.route('/register', methods = ["GET", "POST"])
def register():
    err_msg = None
    err_msg = request.args.get('err_msg')

    if request.method == "POST":
        check = 0
        username = request.form["username"]
        password = request.form["password"]
        with open('credentials.csv', "r") as f:
            for i in f:
                if re.match("^"+username+",",i):
                    check = 1
                    break
        if check == 0:
            with open('credentials.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([request.form.get("username"), request.form.get("password")])
            return redirect(url_for('login',err_msg=""))
        else:
            err_msg = "User name already exists."


    return render_template("register.html", err_msg = err_msg)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    files = os.listdir("static/NSW/")
    files = [random.choice(files) for i in range(10)]
    articles = collections.OrderedDict()
    for i in files:
        with open(os.path.join("static/NSW/", i)) as f:
            title = se.hp.extract_html_title(f)
        articles[i] = title
    return render_template("home.html", articles=articles)

@app.route('/all/p<page>', methods=['GET', 'POST'])
def show_all(page):
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    page = int(page)
    total = int(len(os.listdir("static/NSW/")))
    #print(total)
    #print(page)
    articles = get_all_aritcles(page, total)

    return render_template("all.html", articles=articles, page=page, total=total)

@app.route('/showing/<link>', methods=['GET', 'POST'])
def showing_article(link):
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    searching = request.args.get('searching')
    print(searching)

    if searching == "True":
        link = highlight(link)
    elif searching == "key":
        link = re.sub("NSW[\\\\|\/]", "", link)
        link = "NSW/" + link
    else:
        link = "NSW/" + link
    return render_template("showing.html", link=link)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global current_result
    if not logged:  return redirect(url_for('login', err_msg="Please login."))

    message = None
    if request.method == "POST":
        button = request.form.get("btn")
        if button == "logout":  return redirect(url_for('logout'))
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

            # print(f)
            file_name = secure_filename(f.filename)
            # print(file_name)
            save_path = "static/uploaded_files/{}".format(file_name)
            f.save(save_path)
            input = ""
            with open(save_path) as file:
                input = file.read()
            current_result = se.find_similarity(input, input_savepath="static/uploaded_file_reduced_vector", result_size=200)
            #os.system("mv " + file_name + " uploads/" + file_name)
            message = "Uploaded successfully!"
            return redirect(url_for('show_search_result',page = 1))
    type = request.args.get('t')
    if type=="file":
        return render_template("upload_txt.html", message=message)
    return render_template("upload_plain.html", message=message)



@app.route('/search_result/p<page>', methods=['GET','POST'])
def show_search_result(page):
    global current_result
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    page = int(page)
    total = len(current_result)
    articles = current_result[((page - 1) * 100):page * 100,[0,1,2,3]]

    return render_template("search_results.html", articles=articles, page=page, total=total)



@app.route('/searchkw_result/p<page>', methods=['GET','POST'])
def searchkw_result(page):
    global current_result

    # print(current_result)
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    page = int(page)
    #total = int(len(os.listdir("static/NSW/")))
    total = len(current_result)
    #articles = get_all_aritcles(page, total)
    articles = current_result[((page - 1) * 10):page * 10]
    #print(articles)
    return render_template("search_res_keyword.html", articles=articles, page=page, total=total)


@app.route('/searchkw', methods=['POST'])
def searchkw():
    global current_result
    search_content_title = request.form['title']
    search_content_content = request.form['content']

    print(search_content_title)
    print(search_content_content)

    # search_method = request.form['btn']

    # print(search_method)

    print("in the searchkw")
    # print(search_content)

    if search_content_content:
        current_result = keyword_search.keyword_content(search_content_content)
    elif search_content_title:
        current_result = keyword_search.keyword_title(search_content_title)
    return redirect(url_for('searchkw_result',page = 1))


@app.route('/search', methods=['POST'])
def search():
    global current_result
    search_content = request.form['search']
    print("in the search")
    print(search_content)
    current_result = se.find_similarity(search_content, input_savepath="static/reduced_vector", result_size=200)
    return redirect(url_for('show_search_result',page = 1))

@app.route('/logout')
def logout():
    global logged
    logged = False
    return redirect(url_for('login',err_msg="Successfully logged out."))

@app.route('/about_us')
def about_us():
    return render_template("dashboard.html")

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
                # i = "NSW/" + i
                articles[i] = title

        count += 1
    #print(articles)
    return articles

def authentication (username, password):

    with open('credentials.csv', 'r') as f:
        for i in f:
            if re.match("^"+username, i):
                line = re.sub("^.*\,","",i)
                line = re.sub("\n$","",line)
                if line == password:
                    return username

    return None

def highlight (link):
    files = os.listdir("static/")
    for file in files:
        # print(file)
        if re.match(".*\.html$", file):
            os.remove("static/" + file)
    page = 1

    articles = current_result[((page - 1) * 100):page * 100, [0, 1, 2, 3]]
    for link_a, b, c, top_words in articles:
        if link_a == link:
            break
    print(link)
    with open(os.path.join("static/", link), "r") as f:
        lines = []
        for line in f:
            if re.match("^\s*$", line) or re.match("^\s*<title>", line):
                lines.append(line)
                continue
            for word in top_words[0:16]:

                if re.match("\\b<mark>" + word + "<\/mark>\\b", line, flags=re.I):
                    continue
                if re.match(r".*" + word + ".*", line, flags=re.I):
                    # print(line)
                    found = re.findall("\\b" + word + "\\b", line, flags=re.I)
                    if found:
                        line = re.sub("\\b" + word + "\\b", "<mark>" + found[0] + "</mark>", line, flags=re.I)

            lines.append(line)
    f.close()
    # open("static/showing.html", "w").close()

    link = re.sub("^NSW\\\\", "", link)

    with open(os.path.join("static/", link), "a") as f:
        for line in lines:
            f.write(line)
    return link




if __name__ == '__main__':
    global logged
    logged = True
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=1345)
