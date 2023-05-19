#!/usr/bin/python3
"""Script that starts a Flask server."""
from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Method to remove the current SQLAlchemy Session after each request.
    """
    storage.close()


@app.route('/states_list', strict_slashes=False)
def display_html():
    """
    Route to display a HTML page with the list of all State objects present in DBStorage.
    """
    states = storage.all(State)
    dict_to_html = {value.id: value.name for value in states.values()}
    return render_template('7-states_list.html',
            Table=states,
            items=dict_to_html)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
