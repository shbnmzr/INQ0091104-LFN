import os
import csv
import json
import networkx as nx


def extract_graph(raw_data_path, output_path):
    """
    Extracts a graph from raw drug-drug interaction data, filters small connected components, and saves the result as
    a JSON file.

    Parameters:
        raw_data_path (str): Path to the raw data file.
        output_path (str): Path to save the extracted graph in JSON format.
    """
    # Check if the output file already exists
    if os.path.exists(output_path):
        exit(f"Graph file already exists at: {output_path}")

    # Check if the input file exists
    if not os.path.exists(raw_data_path):
        exit(f"Raw data file not found at {raw_data_path}.")

    # Build and filter the graph
    graph_content = build_graph(raw_data_path)
    graph_content = filter_small_components(graph_content, min_size=3)

    # Save the graph to a JSON file
    with open(output_path, "w") as json_file:
        json.dump(graph_content, json_file, indent=2)

    print(f"Graph successfully saved to {output_path}.")


def build_graph(file_path):
    """
    Builds a graph structure (nodes and links) from raw drug interaction data.

    Parameters:
        file_path (str): Path to the raw TSV file.

    Returns:
        dict: The graph structure containing nodes and links.
    """
    node_mapping = {}
    nodes = []
    links = []
    node_counter = 0

    # Read drug data from the specified file
    with open(file_path, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')

        # Skip the header if present
        header = next(tsv_reader, None)

        # Process each row
        for row in tsv_reader:
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue

            drug_a, drug_b = row[0], row[1]

            # Add DrugA to nodes if not already present
            if drug_a not in node_mapping:
                node_mapping[drug_a] = node_counter
                nodes.append(to_node(drug_a, node_counter, "blue"))
                node_counter += 1

            # Add DrugB to nodes if not already present
            if drug_b not in node_mapping:
                node_mapping[drug_b] = node_counter
                nodes.append(to_node(drug_b, node_counter, "green"))
                node_counter += 1

            # Add the link between DrugA and DrugB
            links.append(to_link(node_mapping[drug_a], node_mapping[drug_b]))

    return {"directed": False, "nodes": nodes, "links": links}


def filter_small_components(graph_content, min_size):
    """
    Removes connected components smaller than the specified minimum size.

    Parameters:
        graph_content (dict): The graph data in dictionary format (nodes and links).
        min_size (int): The minimum size of connected components to retain.

    Returns:
        dict: The filtered graph content.
    """
    g = nx.Graph()

    # Add nodes and edges to the NetworkX graph
    for node in graph_content['nodes']:
        g.add_node(node['id'], **node)

    for link in graph_content['links']:
        g.add_edge(link['source'], link['target'], **link)

    # Filter connected components by size
    filtered_nodes = []
    filtered_links = []

    for component in nx.connected_components(g):
        if len(component) >= min_size:
            subgraph = g.subgraph(component)
            filtered_nodes.extend(subgraph.nodes(data=True))
            filtered_links.extend(subgraph.edges(data=True))

    # Reconstruct the filtered graph content
    nodes = [{"id": n, **attr} for n, attr in filtered_nodes]
    links = [{"source": u, "target": v, **attr} for u, v, attr in filtered_links]

    return {"directed": graph_content["directed"], "nodes": nodes, "links": links}


def to_node(label, node_id, color="red"):
    """
    Creates a node representation for the graph.

    Parameters:
        label (str): The label of the node (drug ID).
        node_id (int): Unique identifier for the node.
        color (str): Color associated with the node.

    Returns:
        dict: Node attributes
    """
    return {"id": node_id, "label": label, "color": color}


def to_link(source, target, weight=1):
    """
    Creates a link representation for the graph.

    Parameters:
        source (int): Source node ID.
        target (int): Target node ID.
        weight (int): Weight of the link (default is 1).

    Returns:
        dict: Link attributes.
    """
    return {"source": source, "target": target, "weight": weight}


def main():
    location = "../graphs/drug_drug_graph.json"
    raw_data_path = '../raw_data/ChCh-Miner_durgbank-chem-chem.tsv'
    extract_graph(raw_data_path, output_path=location)


if __name__ == "__main__":
    main()
