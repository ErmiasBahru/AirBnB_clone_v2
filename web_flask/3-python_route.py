#!/usr/bin/python3
"""
    Script that starts a Flask web application
    /: display “Hello HBNB!”
    /hbnb: display “HBNB”
    /c/<text>: display “C ” followed by the value of the
    text variable (replace underscore _ symbols with a space)
    /python/(<text>): display “Python ”, followed by the value of the
    text variable (replace underscore _ symbols with a space)
    the default value of text is “is cool”
"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    # displays “Hello HBNB!”
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    # displays "HBNB"
    return "HBNB"


@app.route('/c/<string:text>')
def c_route(text):
    # displays "C + text"
    return "C {}".format(text.replace("_", " "))


@app.route('/python')
@app.route('/python/<string:text>')
def python_route(text='is cool'):
    # displays "Python + text"
    return "Python {}".format(text.replace("_", " "))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
