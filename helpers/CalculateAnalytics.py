import json
import os

import networkx as nx
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import numpy as np


def get_top_k_nodes(dictionary, k):
    """
    Retrieves the top k elements from a dictionary based on their values.

    Parameters:
    - dictionary (dict): The dictionary to be processed.
    - k (int): The number of top elements to retrieve.

    Returns:
    - list: A list containing the keys of the top k elements.
    """
    sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    return [c[0] for c in sorted_dict[:k]]


def plot_colored_graph(G, colors_list, title, save_dir='./plots'):
    """
    Plots and saves a colored graph using NetworkX and Matplotlib.

    Parameters:
    - G (networkx.Graph): The graph to be plotted.
    - colors_list (list): A list specifying node colors.
    - title (str): The title of the plot.
    - save_dir (str): The directory where the plot should be saved.

    Returns:
    - None
    """
    # Ensure the directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    plt.figure(figsize=(20, 15))
    pos = nx.spring_layout(G, iterations=100, scale=8.0, k=0.2, seed=37)
    nx.draw_networkx(G, pos=pos, with_labels=True, font_weight='bold', node_color=colors_list, node_size=500,
                     font_size=15)
    plt.title(title)

    # Save the plot as an image
    plot_path = os.path.join(save_dir, f"{title}.png")
    plt.savefig(plot_path)
    plt.close()  # Close the plot to avoid memory issues


def analyze_connected_component(subgraph, component_number, drug_data, drug_gene_data):
    """
    Analyzes a connected component of a graph, extracting both graph-level and node-level features.

    Parameters:
    - subgraph (networkx.Graph): The connected component to be analyzed.
    - component_number (int): The identifier of the component.
    - drug_data (dict): The dictionary containing drug data with common names.
    - drug_gene_data (dict): The dictionary containing drug - genes data (drug - targets interactions).

    Returns:
    - None
    """
    print(f"\nAnalyzing Connected Component {component_number}:")
    if len(subgraph) <= 1:
        print("Single-node component. Skipping analysis.")
        return

    diameter = nx.diameter(subgraph)
    if nx.is_directed(subgraph):
        avg_out_degree = sum(dict(subgraph.out_degree()).values()) / len(subgraph)
        avg_in_degree = sum(dict(subgraph.in_degree()).values()) / len(subgraph)
        print(f"Average Out Degree: {avg_out_degree:.4f}")
        print(f"Average In Degree: {avg_in_degree:.4f}")
    else:
        avg_degree = sum(dict(subgraph.degree()).values()) / len(subgraph)
        print(f"Average Degree: {avg_degree:.4f}")

    avg_clustering_coefficient = nx.average_clustering(subgraph)
    avg_shortest_path_length = nx.average_shortest_path_length(subgraph)
    triangles = sum(nx.triangles(subgraph).values()) // 3

    print("\nGraph Features:")
    print(f"Diameter: {diameter}")
    print(f"Average Clustering Coefficient: {avg_clustering_coefficient:.4f}")
    print(f"Average Shortest Path Length: {avg_shortest_path_length:.4f}")
    print(f"Number of closed triangles: {triangles}")

    # Node-level features
    degree_centralities = nx.degree_centrality(subgraph)
    closeness_centralities = nx.closeness_centrality(subgraph)
    betweenness_centralities = nx.betweenness_centrality(subgraph)
    clustering_coefficients = nx.clustering(subgraph)

    print("\nNode Features:")
    for node in subgraph.nodes:
        common_name = drug_data.get(subgraph.nodes[node]['label'], {}).get('common_name', 'N/A')
        print(f"Node {node}: "
              f"Degree Centrality: {degree_centralities[node]:.4f}, "
              f"Closeness Centrality: {closeness_centralities[node]:.4f}, "
              f"Betweenness Centrality: {betweenness_centralities[node]:.4f}, "
              f"Clustering Coefficient: {clustering_coefficients[node]:.4f}, "
              f"Common Name: {common_name}")

    k = 5

    # Degree centrality
    top_k_degree_nodes = get_top_k_nodes(degree_centralities, k)
    print(f"\nTop {k} nodes with highest degree centrality:")
    for node in top_k_degree_nodes:
        drug_label = subgraph.nodes[node]['label']
        common_name = drug_data.get(drug_label, {}).get('common_name', 'N/A')
        genes = drug_gene_data.get(drug_label, {}).get('genes', [])
        print(f"Node {node}: "
              f"Degree Centrality: {degree_centralities[node]:.4f}, "
              f"Node Label: {subgraph.nodes[node]['label']}, "
              f"Common Name: {common_name}, "
              f"Target genes: {genes}")
    node_colors = ['red' if node in top_k_degree_nodes else 'lightblue' for node in subgraph.nodes]
    plot_colored_graph(subgraph, node_colors, f"Top {k} nodes with highest degree centrality")

    # Closeness centrality
    top_k_closeness_nodes = get_top_k_nodes(closeness_centralities, k)
    print(f"\nTop {k} nodes with highest closeness centrality:")
    for node in top_k_closeness_nodes:
        drug_label = subgraph.nodes[node]['label']
        common_name = drug_data.get(drug_label, {}).get('common_name', 'N/A')
        genes = drug_gene_data.get(drug_label, {}).get('genes', [])
        print(f"Node {node}: "
              f"Closeness Centrality: {closeness_centralities[node]:.4f}, "
              f"Node Label: {subgraph.nodes[node]['label']}, "
              f"Common Name: {common_name}, "
              f"Target genes: {genes}")
    node_colors = ['red' if node in top_k_closeness_nodes else 'lightblue' for node in subgraph.nodes]
    plot_colored_graph(subgraph, node_colors, f"Top {k} nodes with highest closeness centrality")

    # Betweenness centrality
    top_k_betweenness_nodes = get_top_k_nodes(betweenness_centralities, k)
    print(f"\nTop {k} nodes with highest betweenness centrality:")
    for node in top_k_betweenness_nodes:
        drug_label = subgraph.nodes[node]['label']
        common_name = drug_data.get(drug_label, {}).get('common_name', 'N/A')
        genes = drug_gene_data.get(drug_label, {}).get('genes', [])
        print(f"Node {node}: "
              f"Betweenness Centrality: {betweenness_centralities[node]:.4f}, "
              f"Node Label: {subgraph.nodes[node]['label']}, "
              f"Common Name: {common_name}, "
              f"Target genes: {genes}")
    node_colors = ['red' if node in top_k_betweenness_nodes else 'lightblue' for node in subgraph.nodes]
    plot_colored_graph(subgraph, node_colors, f"Top {k} nodes with highest betweenness centrality")

    # Clustering coefficient
    top_k_clustering_nodes = get_top_k_nodes(clustering_coefficients, k)
    print(f"\nTop {k} nodes with highest clustering coefficient:")
    for node in top_k_clustering_nodes:
        drug_label = subgraph.nodes[node]['label']
        common_name = drug_data.get(drug_label, {}).get('common_name', 'N/A')
        genes = drug_gene_data.get(drug_label, {}).get('genes', [])
        print(f"Node {node}: "
              f"Clustering Coefficient: {clustering_coefficients[node]:.4f}, "
              f"Node Label: {subgraph.nodes[node]['label']}, "
              f"Common Name: {common_name}, "
              f"Target genes: {genes}")
    node_colors = ['red' if node in top_k_clustering_nodes else 'lightblue' for node in subgraph.nodes]
    plot_colored_graph(subgraph, node_colors, f"Top {k} nodes with highest clustering coefficient")

    # Combination feature
    degree_centralities_normalized = {node: value for node, value in zip(
        subgraph.nodes,
        MinMaxScaler().fit_transform(np.array(list(degree_centralities.values())).reshape(-1, 1)).flatten())}
    closeness_centralities_normalized = {node: value for node, value in zip(
        subgraph.nodes,
        MinMaxScaler().fit_transform(np.array(list(closeness_centralities.values())).reshape(-1, 1)).flatten())}
    betweenness_centralities_normalized = {node: value for node, value in zip(
        subgraph.nodes,
        MinMaxScaler().fit_transform(np.array(list(betweenness_centralities.values())).reshape(-1, 1)).flatten())}
    clustering_coefficients_normalized = {node: value for node, value in zip(
        subgraph.nodes,
        MinMaxScaler().fit_transform(np.array(list(clustering_coefficients.values())).reshape(-1, 1)).flatten())}

    degree_centrality_coeff, closeness_centrality_coeff, betweenness_centrality_coeff, clustering_coefficient_coeff = 1, 1.5, 2, 1
    combination_node_features = {}
    for node in subgraph.nodes:
        combination_node_features[node] = (
                degree_centrality_coeff * degree_centralities_normalized[node] +
                closeness_centrality_coeff * closeness_centralities_normalized[node] +
                betweenness_centrality_coeff * betweenness_centralities_normalized[node] +
                clustering_coefficient_coeff * clustering_coefficients_normalized[node]
        )

    top_k_combination = get_top_k_nodes(combination_node_features, k)
    print(f"\nTop {k} nodes with the highest combination of node features:")
    for node in top_k_combination:
        drug_label = subgraph.nodes[node]['label']
        common_name = drug_data.get(drug_label, {}).get('common_name', 'N/A')
        genes = drug_gene_data.get(drug_label, {}).get('genes', [])
        print(f"Node {node}: "
              f"Combination value: {combination_node_features[node]:.4f}, "
              f"Node Label: {subgraph.nodes[node]['label']}, "
              f"Common Name: {common_name}, "
              f"Target genes: {genes}")
    node_colors = ['red' if node in top_k_combination else 'lightblue' for node in subgraph.nodes]
    plot_colored_graph(subgraph, node_colors, f"Top {k} nodes with highest combination of node features")


def calculate_analytics(model):
    """
    Analyzes the connectivity of a graph, identifies connected components, and analyzes each component separately.

    Parameters:
    - model: An object containing the graph data.

    Returns:
    - None
    """
    print(f"Analyzing {model.NAME} network\n")
    graph = model.graph
    drug_data = load_json_data('./graphs/drug_data.json')
    drug_gene_data = load_json_data('./graphs/drug_gene_data.json')

    if nx.is_directed(graph):
        if nx.is_strongly_connected(graph):
            print('Graph is strongly connected!')
            analyze_connected_component(graph, 1, drug_data, drug_gene_data)
        else:
            print("Graph is not strongly connected.")
            components = list(nx.strongly_connected_components(graph))
            print("Connected Components:", components)
            for i, scc in enumerate(components):
                subgraph = graph.subgraph(scc)
                analyze_connected_component(subgraph, i + 1, drug_data, drug_gene_data)
    else:
        if nx.is_connected(graph):
            print('Graph is connected!')
            analyze_connected_component(graph, 1, drug_data, drug_gene_data)
        else:
            print("Graph is not connected.")
            components = list(nx.connected_components(graph))
            print("Connected Components:", components)
            for i, scc in enumerate(components):
                subgraph = graph.subgraph(scc)
                analyze_connected_component(subgraph, i + 1, drug_data, drug_gene_data)

    print("\n\n\n------------------------------------------------------------------\n\n\n")


# Load drug data from the JSON file
def load_json_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
