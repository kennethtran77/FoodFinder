"""
FoodFinder
by Kenneth Tran

Visualizes the results from the recommender systems as plotly figures.
"""
import networkx as nx

import plotly.offline
import plotly.graph_objects as go
from plotly.graph_objs import Scatter, Figure

from graph import ComfortFoodGraph


def visualize_comfort_food_recommendations(graph: ComfortFoodGraph) -> None:
    """Use plotly and networkx to visualize the graph.
    """
    graph_nx = graph.to_networkx()

    # Fetch positioning for bipartite graph layout
    left_or_top = graph.get_vertices()
    pos = nx.bipartite_layout(graph_nx, left_or_top)

    x_nodes = [pos[k][0] for k in graph_nx.nodes]
    y_nodes = [pos[k][1] for k in graph_nx.nodes]
    x_edges = []
    y_edges = []

    labels = []

    # Colour nodes based on their number of connections
    node_adjacencies = []

    for adjacencies in graph_nx.adjacency():
        node_adjacencies.append(len(adjacencies[1]))
        labels.append(f'{adjacencies[0]}<br># of connections: {len(adjacencies[1])}')

    for edge in graph_nx.edges:
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    # Create the edge and node traces
    edge_trace = Scatter(
                    x=x_edges,
                    y=y_edges,
                    mode='lines',
                    name='edges',
                    line=dict(color='rgb(70,70,70)', width=1),
                    hoverinfo='none',
                )
    node_trace = Scatter(
                    x=x_nodes,
                    y=y_nodes,
                    mode='markers',
                    name='nodes',
                    marker=dict(
                        symbol='circle-dot',
                        size=7.5,
                        showscale=True,
                        colorscale='YlGnBu',
                        reversescale=True,
                        color=node_adjacencies,
                        line=dict(color='rgb(50, 50, 50)', width=0.5),
                        colorbar=dict(
                            thickness=15,
                            title='Node Connections',
                            xanchor='left',
                            titleside='right'
                        )
                    ),
                    text=labels,
                    hovertemplate='%{text}',
                    hoverlabel={'namelength': 0}
                )

    fig = Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                     title='<b>People who liked the foods recommended to you</b>'
                           '<br><a href="https://www.kaggle.com/borapajo/food-choices">'
                           'Dataset: Food choices from Kaggle</a>',
                     showlegend=False,
                     xaxis=dict(showgrid=False, zeroline=False, visible=False),
                     yaxis=dict(showgrid=False, zeroline=False, visible=False)
                 ))

    # Save the figure to an html file
    plotly.offline.plot(fig)
