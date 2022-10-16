#!/usr/bin/python3
"""
Script that starts a Flask web application
and displays “Hello HBNB!” at / and "HBNB" at /hbnb
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
