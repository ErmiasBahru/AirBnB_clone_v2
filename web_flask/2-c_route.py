#!/usr/bin/python3
"""
    Script that starts a Flask web application
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ” followed by the value of the
    text variable (replace underscore _ symbols with a space)
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    # displays “Hello HBNB!”
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    # displays "HBNB"
    return "HBNB"


@app.route('/c/<string:text>', strict_slashes=False)
def c_route(text):
    # displays "C + text"
    return "C {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
