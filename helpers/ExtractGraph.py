import os
import csv
import json


def main():
    location = "../graphs/drug_drug_graph.json"
    raw_data_path = '../raw_data/ChCh-Miner_durgbank-chem-chem.tsv'
    extract_graph(raw_data_path, output_path=location)


def extract_graph(raw_data_path, output_path):
    if os.path.exists(output_path):
        exit("Graph file already exists.")

    if not os.path.exists(raw_data_path):
        exit(f"Raw data file not found at {raw_data_path}.")

    graph_content = build_graph(raw_data_path)

    # Save the graph to a JSON file
    with open(output_path, "w") as json_file:
        json.dump(graph_content, json_file, indent=2)

    print(f"Graph successfully saved to {output_path}.")


def build_graph(file_path):
    keep = {}
    nodes = []
    links = []
    node_counter = 0

    # Read drug data from the specified file
    with open(file_path, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')
        header = next(tsv_reader, None)  # Skip the header if present

        for row in tsv_reader:
            if len(row) < 2:
                print(f"Skipping invalid row: {row}")
                continue

            drug_a, drug_b = row[0], row[1]  # Assuming the file has two columns: DrugA and DrugB

            # Add DrugA to nodes if not already present
            if drug_a not in keep:
                keep[drug_a] = node_counter
                nodes.append(to_node(drug_a, node_counter, "blue"))
                node_counter += 1

            # Add DrugB to nodes if not already present
            if drug_b not in keep:
                keep[drug_b] = node_counter
                nodes.append(to_node(drug_b, node_counter, "green"))
                node_counter += 1

            # Add the link between DrugA and DrugB
            links.append(to_link(keep[drug_a], keep[drug_b]))

    return {"directed": False, "nodes": nodes, "links": links}


def to_node(label, id, color="red"):
    return {"id": id, "label": label, "color": color}


def to_link(source, target, weight=1):
    return {"source": source, "target": target, "weight": weight}


if __name__ == "__main__":
    main()
