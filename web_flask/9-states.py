#!/usr/bin/python3
"""
the proceess that start the Flask framework
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City


app = Flask(__name__)


@app.teardown_appcontext
def teardown_session(exception):
    """
    this clossethe Teardown"""
    storage.close()


@app.route('/states/', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def display_html(id=None):
    """defines the states route
    """
    states = storage.all(State)

    if not id:
        dict_to_html = {value.id: value.name for value in states.values()}
        return render_template('7-states_list.html',
                Table="States",
                ite=dict_to_html)

    d = "State.{}".format(id)
    if d in states:
        return render_template('9-states.html',
                Table="State: {}".format(states[d].name),
                ite=states[d])

    return render_template('9-states.html',
                           ite=None)

if __name__ == "__main__":
    app.run(host='0.0.00', port=5000)
