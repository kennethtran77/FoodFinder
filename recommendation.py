"""
FoodFinder
by Kenneth Tran

Calculate recommendations and any related data.
"""

from graph import ComfortFoodGraph


def recommend_comfort_foods(graph: ComfortFoodGraph, keyword: str, liked_foods: set[str],
                            limit: int) -> list[str]:
    """Given a keyword and a set of liked foods, recommend a list of foods of at most
    length `limit` that do not contain any foods in the original set of foods.
    """
    recommended_foods = {}

    # Get all foods
    all_foods = graph.get_foods()

    # Get foods that at least one user is connected to with the given keyword (reason)
    foods_with_reasons = get_foods_with_reasons(graph, {keyword})

    for food in all_foods:
        for liked_food in liked_foods:
            # Ignore foods that were already in `liked_foods`
            if food not in liked_foods:
                # Compare similarity between each liked food and potential foods to recommend
                sim = get_similarity(graph, food, liked_food)

                # Get the highest sim score between food and any liked food
                new_score = max(recommended_foods.get(food, 0), sim)

                # Prioritize foods that are associated with the given reasons
                if food in foods_with_reasons:
                    new_score += 5

                if sim > 0:
                    recommended_foods[food] = new_score

    # Sort by descending order
    sorted_recs = sorted(recommended_foods, key=recommended_foods.get, reverse=True)

    return sorted_recs[:limit]


def get_similarity(graph: ComfortFoodGraph, food1: str, food2: str) -> float:
    """Return the similarity (a float between 0.0 and 1.0) between two food vertices.

    The similarity score is calculated using the Jaccard Similarity formula which measures
    the similarity between two sets A and B. We define A as the set of neighbours of food1
    and B as the set of neighbours of food2.
    """
    food1_neighbours = graph.get_neighbours(food1)
    food2_neighbours = graph.get_neighbours(food2)

    if len(food1_neighbours) == 0 or len(food2_neighbours) == 0:
        return 0
    else:
        intersection = food1_neighbours.intersection(food2_neighbours)
        union = food1_neighbours.union(food2_neighbours)

        return len(intersection) / len(union)


def get_foods_with_reasons(graph: ComfortFoodGraph, reasons: set[str]) -> set[str]:
    """Return a set of foods that are associated with at least one reason in `reasons`.
    """
    foods_so_far = set()

    for user in graph.get_users():
        for food in graph.get_neighbours(user):
            if any(reason in graph.get_reasons(user, food) for reason in reasons):
                foods_so_far.add(food)

    return foods_so_far
