"""
FoodFinder
by Kenneth Tran

Stores all the routes/views for the Flask app.
"""

import ast
from typing import Optional, Any

from flask import Blueprint, render_template, request, url_for, redirect, flash

from graph import ComfortFoodGraph
import visualization
import recommendation


def construct_blueprint(comfort_graph: ComfortFoodGraph) -> Blueprint:
    """Return a Blueprint managing the comfort food views.
    """
    comfort_views = Blueprint('views', __name__, template_folder='templates')

    @comfort_views.route('/keywords')
    def choose_keywords() -> Any:
        """Route to select a keyword for comfort food.
        """
        return render_template('choose-keyword.html',
                               keywords=list(comfort_graph.get_all_reasons()))

    @comfort_views.route('/foods')
    def choose_foods() -> Any:
        """Route to select favourite comfort foods.
        """
        # Fetch the keyword from the GET method argument
        keyword = request.args['keyword'].strip()

        # Display error message if keyword is empty
        if keyword == '':
            flash('Please enter a keyword.')
            return redirect(url_for('views.choose_keywords'))

        return render_template('choose-foods.html',
                               foods=list(comfort_graph.get_foods()),
                               keyword=keyword)

    @comfort_views.route('/calculate-recommendations')
    def calculate_recommendations() -> Any:
        """Route to calculate recommendations for comfort meals based on the arguments
        from the GET method.
        """
        # Illegal access error handling
        args = {'keyword', 'food1', 'food2', 'food3'}

        if any(arg not in request.args for arg in args):
            return redirect(url_for('root'))

        # Fetch the keyword argument
        keyword = request.args['keyword'].strip()

        # Fetch the favourite comfort meal arguments
        food1 = request.args['food1'].strip()
        food2 = request.args['food2'].strip()
        food3 = request.args['food3'].strip()

        # Check the inputs
        error_redirect = _check_inputs(keyword, food1, food2, food3)

        if error_redirect is not None:
            return error_redirect

        foods = set()

        if food1 != '':
            foods.add(food1)
        if food2 != '':
            foods.add(food2)
        if food3 != '':
            foods.add(food3)

        recommendations = recommendation.recommend_comfort_foods(comfort_graph, keyword, foods, 5)

        return redirect(url_for('views.display_recommendations',
                                keyword=keyword, food1=food1, food2=food2, food3=food3,
                                recommendations=','.join(recommendations)))

    @comfort_views.route('/recommendations')
    def display_recommendations() -> Any:
        """Route to display recommendations for comfort meals based on the arguments
        from the GET method.
        """
        # Illegal access error handling
        args = {'keyword', 'food1', 'food2', 'food3', 'recommendations'}

        if any(arg not in request.args for arg in args):
            return redirect(url_for('root'))

        # Fetch the keyword argument
        keyword = request.args['keyword'].strip()

        # Fetch the favourite comfort meal arguments
        food1 = request.args['food1'].strip()
        food2 = request.args['food2'].strip()
        food3 = request.args['food3'].strip()

        # Check the inputs
        error_redirect = _check_inputs(keyword, food1, food2, food3)

        if error_redirect is not None:
            return error_redirect

        # Fetch the recommendations argument
        recommendations = request.args['recommendations'].strip().split(',')

        return render_template('recommendations.html', keyword=keyword, food1=food1,
                               food2=food2, food3=food3, recommendations=recommendations)

    @comfort_views.route('/visualize-recommendations')
    def visualize_recommendations() -> Any:
        """Route to visualize recommendations for comfort meals based on the arguments
        from the GET method.
        """
        # Illegal access error handling
        args = {'keyword', 'food1', 'food2', 'food3', 'recommendations'}

        if any(arg not in request.args for arg in args):
            return redirect(url_for('root'))

        # Fetch the keyword argument
        keyword = request.args['keyword'].strip()

        # Fetch the favourite comfort meal arguments
        food1 = request.args['food1'].strip()
        food2 = request.args['food2'].strip()
        food3 = request.args['food3'].strip()

        # Check the inputs
        error_redirect = _check_inputs(keyword, food1, food2, food3)

        if error_redirect is not None:
            return error_redirect

        # Fetch the recommendations argument
        recommendations = ast.literal_eval(request.args['recommendations'].strip())

        # Visualize the results
        subgraph = comfort_graph.create_subgraph(recommendations)
        visualization.visualize_comfort_food_recommendations(subgraph)

        return redirect(url_for('views.display_recommendations',
                                keyword=keyword, food1=food1, food2=food2, food3=food3,
                                recommendations=','.join(recommendations)))

    return comfort_views


def _check_inputs(keyword: str, food1: str, food2: str, food3: str) -> Optional:
    """Return a redirect object if the inputs did not pass the error handling check.
    """
    # Display error message if keyword is empty
    if keyword == '':
        flash('Please enter a keyword.')
        return redirect(url_for('views.choose_keywords'))

    # Display error message if no foods were chosen
    if food1 == '' and food2 == '' and food3 == '':
        flash('Please select at least one value.')
        return redirect(url_for('views.choose_foods', keyword=keyword))

    # Display error message if the user selects duplicate values
    if _check_duplicates_ignore_case([food1, food2, food3]):
        flash('Please select unique values.')
        return redirect(url_for('views.choose_foods', keyword=keyword))

    return None


def _check_duplicates_ignore_case(values: list[str]) -> bool:
    """Return whether there is a duplicate value among values, ignoring case and
    empty strings.

    >>> _check_duplicates_ignore_case(['AbC', 'abc', 'aa'])
    True
    >>> _check_duplicates_ignore_case(['ABC', '', ''])
    False
    """
    no_empty = [value for value in values if value != '']

    uniques = {str.lower(value) for value in no_empty}
    return len(uniques) != len(no_empty)
