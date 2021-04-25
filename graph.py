"""
FoodFinder
by Kenneth Tran

Defines the relevant graph class.
"""

from __future__ import annotations
from typing import Any

import networkx as nx


class _ComfortFoodVertex:
    """A weighted vertex in a ComfortFoodGraph.

    Instance Attributes:
        - value: The value (or name) of this vertex
        - vertex_type: The type of this vertex
        - neighbours: The vertices adjacent to this vertex with weights
    """
    value: str
    vertex_type: str
    neighbours: dict[_ComfortFoodVertex, list[str]]

    def __init__(self, value: Any, vertex_type: str) -> None:
        """Initialize a new vertex with the given item and type."""
        self.value = value
        self.vertex_type = vertex_type
        self.neighbours = {}


class ComfortFoodGraph:
    """A bipartite graph with two disjoint sets: one with users that were surveyed, and one
    representing a food item.
    """
    _vertices: dict[str, _ComfortFoodVertex]

    def __init__(self) -> None:
        self._vertices = {}

    def add_vertex(self, value: str, vertex_type: str) -> None:
        """Add a vertex with the given value and type. Does nothing if the vertex is already in
        this graph.
        """
        if value not in self._vertices:
            self._vertices[value] = _ComfortFoodVertex(value, vertex_type)

    def add_edge(self, user: str, food: str, reasons: list[str]) -> None:
        """Add an edge between user and food with a list of reasons.

        Raise a ValueError if either user or food are not vertices in this graph, or if
        user and food are the same vertex type.
        """
        if user not in self._vertices or food not in self._vertices or \
                self._vertices[user].vertex_type == self._vertices[food].vertex_type:
            raise ValueError
        else:
            # Add the edge between the two vertices
            v1 = self._vertices[user]
            v2 = self._vertices[food]

            v1.neighbours[v2] = reasons
            v2.neighbours[v1] = reasons

    def get_vertex_type(self, item: str) -> str:
        """Return the vertex type of item.

        Raise a ValueError if item is not a vertex in this graph.
        """
        if item in self._vertices:
            return self._vertices[item].vertex_type
        else:
            raise ValueError

    def get_vertices(self) -> set:
        """Return a set of all vertices of this graph.
        """
        return set(self._vertices.keys())

    def get_users(self) -> set:
        """Return a set of all user vertices og this graph.
        """
        return {v.value for v in self._vertices.values() if v.vertex_type == 'user'}

    def get_foods(self) -> set:
        """Return a set of all food vertices og this graph.
        """
        return {v.value for v in self._vertices.values() if v.vertex_type == 'food'}

    def get_neighbours(self, item: str) -> set:
        """Return a set of the neighbours of the given item.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            return {neighbour.value for neighbour in self._vertices[item].neighbours}
        else:
            raise ValueError

    def get_reasons(self, user: str, food: str) -> list[str]:
        """Return a list of strings representing comfort food reasons between the user and food.

        Return an empty list if user and food are not adjacent.

        Raise a ValueError if either user or food are not vertices in this graph, or if
        user and food are the same vertex type.
        """
        if user not in self._vertices or food not in self._vertices or \
                self._vertices[user].vertex_type == self._vertices[food].vertex_type:
            raise ValueError
        else:
            v1 = self._vertices[user]
            v2 = self._vertices[food]
            return v1.neighbours.get(v2, [])

    def get_all_reasons(self) -> set[str]:
        """Return a set of all comfort foods reasons in this graph."""
        reasons = set()

        for v in self.get_users():
            for u in self.get_neighbours(v):
                for reason in self.get_reasons(v, u):
                    reasons.add(reason)

        return reasons

    def create_subgraph(self, foods: list[str]) -> ComfortFoodGraph:
        """Return a subgraph of this current ComfortFoodGraph with only the given foods and users
        that are neighbours with at least one food from `foods`.

        Return an empty ComfortFoodGraph if `foods` is empty.
        """
        subgraph = ComfortFoodGraph()

        if len(foods) == 0 or foods == ['']:
            return subgraph

        # Only add users into subgraph if they are neighbours with at least one food in `foods`
        for user in self.get_users():
            if any(food in self.get_neighbours(user) for food in foods):
                subgraph.add_vertex(user, 'user')

        # Add the given foods into the subgraph
        for food in foods:
            subgraph.add_vertex(food, 'food')

            # Add any edges between the food and every user
            for user in self.get_neighbours(food):
                reasons = self.get_reasons(user, food)
                subgraph.add_edge(user, food, reasons)

        return subgraph

    def to_networkx(self) -> nx.Graph:
        """Convert this graph into a networkx Graph.
        """
        nx_graph = nx.Graph()

        for v in self.get_vertices():
            nx_graph.add_node(v, vertex_type=self.get_vertex_type(v))

            for u in self.get_neighbours(v):
                nx_graph.add_node(u, vertex_type=self.get_vertex_type(u))

                if u in nx_graph.nodes:
                    nx_graph.add_edge(v, u)

        return nx_graph
