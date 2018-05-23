import os, re, collections,  random
#change working dir to the current path
here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import searchEngine_backend as se
import csv
import modules.keyword_search as keyword_search

app = Flask(__name__)
app.config['MAX_CONTENT_PATH'] = 4000
global logged
global current_result


# login function
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


# function for register new user
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


# Display the home page and some random articles.
@app.route('/home', methods=['GET', 'POST'])
def home():
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    articles = get_random_articles()
    return render_template("home.html", articles=articles)


# Display a page showing all articles
@app.route('/all/p<page>', methods=['GET', 'POST'])
def show_all(page):
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    page = int(page)
    total = int(len(os.listdir("static/NSW/")))
    articles = get_all_aritcles(page, total)
    return render_template("all.html", articles=articles, page=page, total=total)


# Shows one case document in a single page
@app.route('/showing/<link>', methods=['GET', 'POST'])
def showing_article(link):
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    searching = request.args.get('searching')
    keyword = request.args.get('keyword')

    if searching == "True":
        link = highlight(link)
    else:
        link = "NSW/" + link
    return render_template("showing.html", link=link)


# This function processes two types of input for whole case search
# The first one is processing the input text directly from textarea
# and the second is processing the uploaded file from user.
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
            current_result = se.find_similarity(input, input_savepath = "static/reduced_vector", result_size = 200)
            return redirect(url_for('show_search_result',page = 1))
        elif button == "upload_file":
            f = request.files['file']
            file_name = secure_filename(f.filename)
            save_path = "static/uploaded_files/{}".format(file_name)
            f.save(save_path)
            input = ""
            with open(save_path) as file:
                input = file.read()
            current_result = se.find_similarity(input, input_savepath="static/uploaded_file_reduced_vector", result_size=200)
            message = "Uploaded successfully!"
            return redirect(url_for('show_search_result',page = 1))
    type = request.args.get('t')
    if type=='fav':
        input = request.args.get("fav")
        if re.match("\w", input):
            message = "Uploaded successfully!"
        current_result = se.find_similarity(input, input_savepath="static/reduced_vector", result_size=200)
        return redirect(url_for('show_search_result', page=1))
    if type=="file":
        return render_template("upload_txt.html", message=message)
    return render_template("upload_plain.html", message=message)


# showing the search result with specific page number
@app.route('/search_result/p<page>', methods=['GET','POST'])
def show_search_result(page):
    global current_result
    if not logged:  return redirect(url_for('login', err_msg="Please login."))
    page = int(page)
    total = len(current_result)
    articles = current_result[((page - 1) * 100):page * 100,[0,1,2,3]]
    return render_template("search_results.html", articles=articles, page=page, total=total)


# showing key words search result with specific page number
@app.route('/searchkw_result/p<page>', methods=['GET','POST'])
def searchkw_result(page):
    global current_result

    if not logged:
        return redirect(url_for('login', err_msg="Please login."))
    page = int(page)
    total = len(current_result)
    articles = current_result[((page - 1) * 10):page * 10]
    return render_template("search_res_keyword.html", articles=articles, page=page, total=total)


# key word search
@app.route('/searchkw', methods=['POST'])
def searchkw():
    global current_result
    search_content_title = request.form['title']
    search_content_content = request.form['content']

    if search_content_content and search_content_title:
        results = []
        current_result_temp = keyword_search.keyword_content(search_content_content)
        for item in current_result_temp:
            if search_content_title.lower() in item[1].lower():
                results.append(item)
        current_result = results
    elif search_content_content:

        current_result = keyword_search.keyword_content(search_content_content)
    elif search_content_title:
        current_result = keyword_search.keyword_title(search_content_title)
    else:

        return redirect(url_for('home'))
    return redirect(url_for('searchkw_result',page = 1))


# similarity search
@app.route('/search', methods=['POST'])
def search():
    global current_result
    search_content = request.form['search']
    current_result = se.find_similarity(search_content, input_savepath="static/reduced_vector", result_size=200)
    return redirect(url_for('show_search_result',page = 1))


# logout function
@app.route('/logout')
def logout():
    global logged
    logged = False
    return redirect(url_for('login',err_msg="Successfully logged out."))


# display the 'about_us' page
@app.route('/about_us')
def about_us():
    return render_template("dashboard.html", logged=logged)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# function to load all articles
def get_all_aritcles(page, total):
    list = os.listdir("static/NSW/")
    articles = collections.OrderedDict()
    count = 1

    for i in sorted(list):
        if count > (page - 1) * 100 and count <= page * 100:
            with open(os.path.join("static/NSW/", i), encoding="ISO-8859-1") as f:
                title = se.hp.extract_html_title(f)
                articles[i] = title

        count += 1
    return articles


# authentication for checking the username and password in local file.
def authentication (username, password):

    with open('credentials.csv', 'r') as f:
        for i in f:
            if re.match("^"+username, i):
                line = re.sub("^.*\,","",i)
                line = re.sub("\n$","",line)
                if line == password:
                    return username

    return None


# get random articles from the local storage
# used for homepage to display some random articles
def get_random_articles ():
    files = os.listdir("static/NSW/")
    files = [random.choice(files) for i in range(50)]
    articles = collections.OrderedDict()
    for i in files:
        title = None
        while title is None:
            i = random.choice(files)
            with open(os.path.join("static/NSW/", i), encoding="ISO-8859-1") as f:
                title = se.hp.extract_html_title(f)
            f.close()
        articles[i] = title
        if len(articles) >= 10:
            break
    return articles


# highlight top important words when displaying the single case in similarity search results.
def highlight (link):
    files = os.listdir("static/")
    for file in files:
        if re.match(".*\.html$", file):
            os.remove("static/" + file)
    page = 1
    articles = current_result[((page - 1) * 100):page * 100]
    for link_a, b, c, top_words in articles:
        if link_a == link:
            break
    with open(os.path.join("static/NSW", link), "r") as f:
        lines = []
        for line in f:
            if re.match("^\s*$", line) or re.match("^\s*<title>", line):
                lines.append(line)
                continue
            for word in top_words[0:16]:

                if re.match("\\b<mark>" + word + "<\/mark>\\b", line, flags=re.I):
                    continue
                if re.match(r".*" + word + ".*", line, flags=re.I):
                    found = re.findall("\\b" + word + "\\b", line, flags=re.I)
                    if found:
                        line = re.sub("\\b" + word + "\\b", "<mark>" + found[0] + "</mark>", line, flags=re.I)

            lines.append(line)
    f.close()
    link = re.sub("^NSW\\\\", "", link)

    with open(os.path.join("static/", link), "a") as f:
        for line in lines:
            f.write(line)
    return link


if __name__ == '__main__':
    global logged
    logged = False
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=9900)
