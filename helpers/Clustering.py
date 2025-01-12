import os
import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms.community import girvan_newman, label_propagation_communities
from community import community_louvain
from sklearn.cluster import SpectralClustering
from collections import Counter


def load_drug_gene_data(file_path):
    """Loads drug-gene data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)


def enrich_graph_with_genes(graph, drug_gene_data):
    """Adds target genes information as node attributes."""
    for node in graph.nodes:
        graph.nodes[node]['genes'] = drug_gene_data.get(graph.nodes[node]['label'], {}).get("genes", [])


def largest_connected_component(graph):
    """Returns the larges connected component of the graph."""
    lcc = max(nx.connected_components(graph), key=len)
    return graph.subgraph(lcc).copy()


def analyze_cluster_targets(graph, clusters, frequency_threshold=0.25):
    """
    Analyzes clusters to find frequent/dominant target genes within each cluster.

    Parameters:
        graph (networkx.Graph): The input graph to analyze.
        clusters (list): A list of clusters (lists of nodes).
        frequency_threshold (float): The minimum frequency (0-1) for a target gene to be considered frequent.

    Returns:
        dict: A dictionary where keys are cluster indices and values are lists of frequent target genes.
    """
    cluster_analysis = {}
    for idx, cluster in enumerate(clusters):
        target_counter = Counter()
        cluster_size = len(cluster)

        # Count target genes in the cluster
        for node in cluster:
            target_genes = graph.nodes[node].get('genes', [])
            target_counter.update(target_genes)

        # Determine dominant target genes based on frequency threshold
        dominant_targets = [
                gene for gene, count in target_counter.items()
                if count / cluster_size >= frequency_threshold
        ]
        cluster_analysis[idx] = dominant_targets

    return cluster_analysis


def girvan_newman_clustering(graph):
    """
    Applies the Girvan-Newman algorithm to detect clusters in a graph.

    Parameters:
        - graph (networkx.Graph): The input graph to be clustered.

    Returns:
        list: A list of clusters, where each cluster is represented as a sorted list of nodes.
    """
    clusters_gen = girvan_newman(graph)
    return [sorted(list(c)) for c in next(clusters_gen)]


def label_propagation_clustering(graph):
    """
    Detects communities using the Label Propagation algorithm.

    Parameters:
        - graph (networkx.Graph): The input graph to be clustered.

    Returns:
        list: A list of clusters, where each cluster is represented as a sorted list of nodes.
    """
    return [sorted(list(c)) for c in label_propagation_communities(graph)]


def louvain_clustering(graph):
    """
    Detects clusters using the Louvain method for modularity maximization.

    Parameters:
        - graph (networkx.Graph): The input graph to be clustered.

    Returns:
        list: A list of clusters, where each cluster is represented as a sorted list of nodes.
    """
    partition = community_louvain.best_partition(graph)
    clusters = {}
    for node, community_id in partition.items():
        clusters.setdefault(community_id, []).append(node)
    return sorted(list(clusters.values()))


def spectral_clustering(graph, n_clusters=5):
    """
    Detects communities using Spectral Clustering on the graph's adjacency matrix.

    Parameters:
        - graph (networkx.Graph): The input graph to be clustered.
        - n_clusters (int): The number of clusters to be considered (default is 5).

    Returns:
        list: A list of clusters, where each cluster is represented as a sorted list of nodes.
    """
    adjacency_matrix = nx.adjacency_matrix(graph)
    sc = SpectralClustering(n_clusters=n_clusters, affinity='precomputed', random_state=42)
    labels = sc.fit_predict(adjacency_matrix.toarray())
    clusters = {}
    for node, label in zip(graph.nodes, labels):
        clusters.setdefault(label, []).append(node)
    return sorted(list(clusters.values()))


def visualize_clusters(graph, clusters, title, save_dir='./plots'):
    """
    Visualizes clusters on a graph using Matplotlib.

    Parameters:
        - graph (networkx.Graph): The input graph to be clustered.
        - clusters (list): A list of clusters, where each cluster is represented as a list of nodes.
        - title (str): The title of the plot.
        - save_dir (str): The directory where the plot should be saved.
    """
    pos = nx.spring_layout(graph, iterations=100, scale=8.0, k=0.2, seed=42)

    plt.figure(figsize=(16, 12))
    colors = plt.cm.tab20(np.linspace(0, 1, len(clusters)))

    for idx, cluster in enumerate(clusters):
        nx.draw_networkx_nodes(graph, pos, nodelist=cluster, node_color=[colors[idx]], node_size=50,
                               label=f"Cluster {idx + 1}")

    nx.draw_networkx_edges(graph, pos, alpha=0.3, edge_color="gray")
    plt.legend(scatterpoints=1, loc="upper right", fontsize=10, frameon=True, title="Clusters")
    plt.title(title, fontsize=14)
    plt.axis("off")

    # Save the plot as an image
    plot_path = os.path.join(save_dir, f"{title}.png")
    plt.savefig(plot_path)
    plt.close()


def compare_clustering(graph):
    """
    Compares clustering results (cluster sizes and frequent target genes) from different clustering algorithms and
    visualizes the results.

    Parameters:
        - graph (networkx.Graph): The input graph to be clustered.
        - drug_gene_data (dict): Drug-gene data loaded from JSON.

    Returns:
        None
    """
    # Enrich the graph with target genes data
    drug_gene_data_path = "./graphs/drug_gene_data.json"
    drug_gene_data = load_drug_gene_data(drug_gene_data_path)
    enrich_graph_with_genes(graph, drug_gene_data)

    # Focus on the largest connected component
    graph_lcc = largest_connected_component(graph)

    # Perform clustering
    girvan_newman_clusters = girvan_newman_clustering(graph)
    label_propagation_clusters = label_propagation_clustering(graph)
    louvain_clusters = louvain_clustering(graph)
    spectral_clusters = spectral_clustering(graph)

    algorithms = [
        ("Girvan-Newman", girvan_newman_clusters),
        ("Label Propagation", label_propagation_clusters),
        ("Louvain", louvain_clusters),
        ("Spectral Clustering", spectral_clusters)
    ]

    for name, clusters in algorithms:
        cluster_sizes = [len(c) for c in clusters]
        print(f"{name} detected {len(clusters)} clusters with sizes: {cluster_sizes}")

        cluster_targets = analyze_cluster_targets(graph_lcc, clusters)
        for idx, targets in cluster_targets.items():
            print(f" Cluster {idx + 1} ({name}): Frequent target proteins -> {targets}")

    visualize_clusters(graph, girvan_newman_clusters, "Clusters Detected by Girvan-Newman")
    visualize_clusters(graph, label_propagation_clusters, "Clusters Detected by Label Propagation")
    visualize_clusters(graph, louvain_clusters, "Clusters Detected by Louvain Method")
    visualize_clusters(graph, spectral_clusters, "Clusters Detected by Spectral Clustering")
