# sample login created for a previous project

from flask_login import LoginManager,login_user, current_user, login_required, logout_user

@app.route("/login", methods = ["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        try:
            this_user = load_user(request.form.get("username",None))
            if this_user.check_pass(request.form["password"]):
                # if user is valid
                login_user(User(request.form.get("username",None)))
                return redirect(url_for("dashboard"))
        except Exception as e:
            error = format(e)
    return render_template("login.html", msg_err = error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"), code=302, Response=None)

@app.route("/register", methods = ["POST","GET"])
def register():
    error = None
    if request.method == "POST":
        if request.form['pw'] == request.form['re_pw']:
            try:
                UserData().register(request.form['id'], request.form['pw'])
                return render_template("msg.html", msg_suc_l = ['Successful Register', "Wait for admin to approve your request.", url_for('index'), "Return to Home Page"])
            except Exception as e:
                # extract the message of error
                error = format(e)
        else:
            error = "Password provided is not same."
    return render_template("register.html",msg_err = error)
