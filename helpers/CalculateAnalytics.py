import networkx as nx
import matplotlib.pyplot as plt
import json
import os


def main():
    graph_file = "../graphs/drug_drug_graph.json"
    analyze_and_save_graph_plots(graph_file, plot_dir="../plots", top_k=10, verbose=False)


def load_graph_from_json(json_path):
    """
    Loads a graph from a JSON file and creates a NetworkX graph.

    Parameters:
    - json_path (str): Path to the JSON file containing graph data.

    Returns:
    - networkx.Graph: The constructed graph.
    """
    with open(json_path, 'r') as file:
        data = json.load(file)

    G = nx.Graph() if not data["directed"] else nx.DiGraph()

    for node in data["nodes"]:
        G.add_node(node["id"], label=node["label"], color=node["color"])

    for link in data["links"]:
        G.add_edge(link["source"], link["target"], weight=link.get("weight", 1))

    return G


def analyze_and_save_graph_plots(graph_path, plot_dir="../plots", top_k=10, verbose=False):
    """
    Loads a graph from JSON, analyzes its structure, and saves metric plots.

    Parameters:
    - graph_path (str): Path to the JSON graph file.
    - plot_dir (str): Directory to save plots.
    - top_k (int): Number of top nodes to analyze for each metric.
    - verbose (bool): If True, prints detailed analysis.

    Returns:
    - None
    """
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)

    G = load_graph_from_json(graph_path)

    # Analyze connected components
    components = (
        list(nx.connected_components(G)) if not nx.is_directed(G) else list(nx.strongly_connected_components(G))
    )
    largest_component = max(components, key=len)
    subgraph = G.subgraph(largest_component).copy()

    print(f"Graph loaded with {len(G.nodes)} nodes and {len(G.edges)} edges.")
    print(f"Largest connected component has {len(subgraph.nodes)} nodes and {len(subgraph.edges)} edges.")

    # Metrics
    metrics = {
        "Degree Centrality": nx.degree_centrality(subgraph),
        "Closeness Centrality": nx.closeness_centrality(subgraph),
        "Betweenness Centrality": nx.betweenness_centrality(subgraph),
    }

    for metric_name, metric_values in metrics.items():
        print(f"\nTop {top_k} nodes by {metric_name}:")
        top_nodes = sorted(metric_values.items(), key=lambda x: x[1], reverse=True)[:top_k]
        for node, value in top_nodes:
            label = subgraph.nodes[node].get("label", node)
            print(f"  Node {node} ({label}): {value:.4f}")

        # Save plot
        plot_path = os.path.join(plot_dir, f"{metric_name.replace(' ', '_').lower()}.png")
        save_graph_with_highlights(subgraph, metric_values, top_nodes, metric_name, plot_path, verbose)


def save_graph_with_highlights(G, metric_values, top_nodes, title, save_path, verbose=False):
    """
    Saves the graph plot with top nodes highlighted to a file.

    Parameters:
    - G (networkx.Graph): Graph to plot.
    - metric_values (dict): Node metric values for coloring.
    - top_nodes (list): Nodes to highlight.
    - title (str): Title of the plot.
    - save_path (str): Path to save the plot.
    - verbose (bool): If True, shows node labels.

    Returns:
    - None
    """
    top_node_ids = [node for node, _ in top_nodes]
    node_colors = [
        "red" if node in top_node_ids else "blue" for node in G.nodes
    ]
    node_sizes = [
        300 if node in top_node_ids else 100 for node in G.nodes
    ]

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, seed=42)

    nx.draw(
        G,
        pos=pos,
        node_color=node_colors,
        node_size=node_sizes,
        with_labels=verbose,
        labels={node: G.nodes[node]["label"] for node in top_node_ids},
        font_weight="bold",
        font_size=8,
    )

    plt.title(title, fontsize=16)
    plt.savefig(save_path, format="png", dpi=300)
    plt.close()
    print(f"Saved plot: {save_path}")


if __name__ == "__main__":
    main()
