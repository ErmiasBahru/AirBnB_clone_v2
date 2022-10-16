#!/usr/bin/python3
"""
Script that starts a Flask web application
/states: display a HTML page: (inside the tag BODY)
/states/<id>: display a HTML page: (inside the tag BODY)
"""
from flask import Flask, render_template
from models import storage, State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_context(exception):
    storage.close()


@app.route('/states')
@app.route('/states/<string:id>')
def states_cities_route(id=None):
    # route that fetches all states or a certain state
    states = storage.all(State)
    all_states = []

    if id is None:
        for state in states.values():
            all_states.append([state.id, state.name])
        return render_template('9-states.html', states=all_states, id=id)
    else:
        state_list = list(filter(lambda x: x.id == id, states.values()))
        state = None if len(state_list) == 0 else state_list[0]
        city_data = None
        if state:
            cities = state.cities
            cities_list = list(
                filter(lambda x: x.state_id == state.id, cities))
            city_data = list(map(lambda x: [x.id, x.name], cities_list))
        return render_template('9-states.html', state=state, cities=city_data, id=id)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
