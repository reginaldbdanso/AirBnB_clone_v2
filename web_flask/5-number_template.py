#!/usr/bin/python3
"""Start a Flask web application"""
from flask import Flask, abort, render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Display Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Display HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Display C followed by the value
    of the text variable"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route(
    '/python/',
    strict_slashes=False
)
@app.route(
    '/python/<text>',
    strict_slashes=False
)
def python(text='is cool'):
    """Display Python followed by the value
    of the text variable"""
    if text is None:
        abort(404)
    return 'Python {}'.format(text.replace('_', ' '))


@app.route('/number/<n>', strict_slashes=False)
def number(n):
    """Display n is a number only if n is an integer"""
    try:
        return '{} is a number'.format(int(n))
    except Exception as e:
        abort(404)


@app.route('/number_template/<n>', strict_slashes=False)
def number_template(n):
    """Display a HTML page only if n is an
    integer"""
    try:
        return render_template('5-number.html', n=int(n))
    except Exception as e:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
