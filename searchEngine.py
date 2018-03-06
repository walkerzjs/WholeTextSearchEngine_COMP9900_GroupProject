import datetime
import os
from flask import request, render_template, Flask, redirect, url_for, make_response, session

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
