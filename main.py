"""
FoodFinder
by Kenneth Tran

main.py

Main module to be executed.
"""

from typing import Any

from flask import Flask, render_template, redirect, url_for
import os

import load

from views import views

app = Flask(__name__)


@app.route('/')
def root() -> Any:
    """Root route."""
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e) -> Any:
    """Route to handle 404 errors."""
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.secret_key = os.urandom(12)

    food_choices_path = 'data/food_choices_clean.csv'

    # Display error message if the food choices dataset is not found
    if not os.path.isfile(food_choices_path):
        raise FileNotFoundError(f'The food choices dataset file: {food_choices_path} was not found')

    # Load the graph
    comfort_graph = load.load_comfort_food_graph(food_choices_path)

    # Register Blueprints for routes in other modules
    app.register_blueprint(views.construct_blueprint(comfort_graph))

    app.run(debug=True)
