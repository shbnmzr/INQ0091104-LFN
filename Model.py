import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter
import os

class Model:
    """
    This class encapsulates common functionality for loading and drawing graphs.
    """
    def __init__(self):
        self.file = None
        self.graph = None
        self.isDrawn = False

    def set_file_location(self, location: str):
        self.file = location

    def panic(self, message):
        raise Exception(f"Panic: {message}")

    def panic_if_file_not_loaded(self):
        if not self.file:
            self.panic("Graph file NOT set")
        if not os.path.exists(self.file):
            self.panic("Graph file does not exist")

    def draw(self):
        if not self.isDrawn:
            edge_labels = {(u, v): f"{d['weight']:.2f}"
                           for u, v, d in self.graph.edges(data=True)}
            pos = nx.spring_layout(self.graph, k=0.15, iterations=20)
            nx.draw(self.graph, pos, with_labels=True, font_weight='bold',
                    node_size=700, node_color='skyblue', font_size=10)
            nx.draw_networkx_edge_labels(
                self.graph, pos, edge_labels=edge_labels, font_color='red')
            self.isDrawn = True

    def show(self):
        self.draw()
        plt.show()

    def load_graph(self):
        self.panic_if_file_not_loaded()

        with open(self.file) as handler:
            data = json.loads(handler.read())
            if data["directed"]:
                self.graph = nx.DiGraph()
            else:
                self.graph = nx.Graph()
            self.graph.add_nodes_from(
                (node["id"], {"label": node["label"], "color": node.get("color", "skyblue")}) for node in data["nodes"])
            self.graph.add_weighted_edges_from([(edge["source"], edge["target"], edge["weight"])
                                                for edge in data["links"]])
