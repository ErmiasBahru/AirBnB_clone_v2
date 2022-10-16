#!/usr/bin/python3
"""
Script that starts a Flask web application
/states_list: display a HTML page: (inside the tag BODY) 
"""
from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_context(exception):
    storage.close()


@app.route('/states_list')
def states_route():
    states = storage.all(State)
    all_states = []

    for state in states.values():
        all_states.append([state.id, state.name])
    return render_template('7-states_list.html', states=all_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
