#!/usr/bin/python3
"""
    Starts a flask web application listening on 0.0.0.0, port 5000
    and displays the results of states and amenities to a web page
    via "/hbnb_filters" route
"""
from flask import Flask, render_template
from models import storage, State, Amenity

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_context(exception):
    """
        These functions are typically also called when the request
        context is popped.
    """
    storage.close()


@app.route("/hbnb_filters")
def states_cities_route():
    """
        Route that fetches all cities in a stage
        from the storage engine
    """
    states = storage.all(State)
    amenities = storage.all(Amenity)
    all_states = []
    all_amenities = []

    for state in states.values():
        cities = state.cities
        cities_list = list(filter(lambda x: x.state_id == state.id, cities))
        c_data = list(map(lambda x: [x.id, x.name], cities_list))
        all_states.append([state.id, state.name, c_data])
    for amenity in amenities.values():
        all_amenities.append([amenity.id, amenity.name])

    return render_template("10-hbnb_filters.html", states=all_states,
                           amenities=all_amenities
                           )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
