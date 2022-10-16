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
    /number/<n>: display “n is a number” only if n is an integer
    /number_template/<n>: display a HTML page only if n is an integer
    H1 tag: “Number: n” inside the tag BODY
"""

from flask import Flask, render_template

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


@app.route('/number/<int:n>')
def number_route(n):
    # display “n is a number” only if n is an integer
    return '{} is a number'.format(n)


@app.route('/number_template/<int:n>')
def number_template(n):
    return render_template('5-number.html', number=n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
