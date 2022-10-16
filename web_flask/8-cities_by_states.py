#!/usr/bin/python3
"""
Script that starts a Flask web application
/cities_by_states: display a HTML page: (inside the tag BODY)
"""
from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_context(exception):
    storage.close()


@app.route('/cities_by_states')
def cities_states_route():
    # route that fetches all cities in a stage from the sotrage engine

    states = storage.all(State)
    all_states = []

    for state in states.values():
        cities = state.cities
        cities_list = list(filter(lambda x: x.state_id == state.id, cities))
        city_data = list(map(lambda x: [x.id, x.name], cities_list))
        all_states.append([state.id, state.name, city_data])

    return render_template('8-cities_by_states.html', states=all_states)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
