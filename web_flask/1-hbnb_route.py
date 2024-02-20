#!/usr/bin/python3
"""
this process start Flask application
"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    defines route" and returns HBNB
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """define hbnb route and returns HBNB
    """
    return "HBNB"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
