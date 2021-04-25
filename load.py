"""
FoodFinder
by Kenneth Tran

Load the dataset.
"""

import csv

from graph import ComfortFoodGraph


def load_comfort_food_graph(filename: str) -> ComfortFoodGraph:
    """Return a ComfortFoodFraph from extracting the relevant data from the Food choices
    dataset (cleaned).
    """
    with open(filename) as csv_file:
        reader = csv.reader(csv_file)

        graph = ComfortFoodGraph()

        # Skip header
        next(reader)

        # Each row represents one user
        for index, row in enumerate(reader):
            user_comfort_foods_raw = row[0]
            user_comfort_foods_reason_raw = row[1]

            # A list of comfort foods that the user likes
            user_comfort_foods = [comfort_food.strip()
                                  for comfort_food in user_comfort_foods_raw.split(',')]

            # A list of reasons why the user likes the comfort foods
            user_comfort_foods_reasons = [comfort_food_reason.strip()
                                          for comfort_food_reason in
                                          user_comfort_foods_reason_raw.split(',')]

            # Add each user as a vertex
            graph.add_vertex(f'User #{index}', 'user')

            for food in user_comfort_foods:
                graph.add_vertex(food, 'food')
                graph.add_edge(f'User #{index}', food, user_comfort_foods_reasons)

        return graph
