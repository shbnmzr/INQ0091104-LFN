# Learning from Drug Interaction Networks

This repository contains the code and resources for analyzing drug-drug interaction (DDI) networks using graph-based techniques. The project explores centrality measures, clustering algorithms, and link prediction methods to uncover patterns and relationships in DDI data.

## Overview

Drug-drug interactions can significantly affect therapeutic outcomes and lead to adverse effects. This project applies advanced graph analysis techniques to identify key drugs, detect meaningful communities, and predict potential missing interactions within a DDI network.

### Key Features
- **Graph Construction:** Builds and processes a DDI network from raw datasets.
- **Centrality Analysis:** Computes degree, closeness, and betweenness centrality to identify influential drugs.
- **Clustering:** Applies algorithms like Girvan-Newman, Louvain, Label Propagation, and Spectral Clustering to detect communities.
- **Link Prediction:** Uses methods like Adamic-Adar, Common Neighbors, and Jaccard Coefficient to infer missing interactions.
- **Data Enrichment:** Integrates drug-target gene interactions to provide biological context.

## Dataset

1. **Drug Interaction Network:**
   - Source: [ChCh-Miner Dataset](https://snap.stanford.edu/biodata/datasets/10001/10001-ChCh-Miner.html)
   - Details: 1514 drugs and 48514 interactions.

2. **Drug-Target Gene Data:**
   - Source: [ChG-Miner Dataset](https://snap.stanford.edu/biodata/datasets/10002/10002-ChG-Miner.html)
   - Details: Links drugs to target genes for enriched analysis.

3. **DrugBank Vocabulary Dataset:**
   - Provides drug names and additional metadata (extracted into `drug_info.json`).

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/shbnmzr/INQ0091104-LFN.git
   cd INQ0091104-LFN```
   
2. Install Dependencies: Create a virtual environment and install the required libraries:
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt```

## Usage
1. Construct the Graph
Run the `ExtractGraph.py` script to process the raw DDI dataset and construct the graph:
    ```bash
    python scripts/ExtractGraph.py
   ```
   
2. Enrich the Graph with Drug Information
Use the `FetchDrugInfo.py` and `FetchDrugGeneInfo.py` scripts to extract and add metadata:
    ```bash
   python scripts/FetchDrugInfo.py
   python scripts/FetchDrugGeneInfo.py
   ```

3. Perform Centrality Analysis
Compute centrality measures using `CalculateAnalytics.py`:
    ```bash
    python scripts/CalculateAnalytics.py
    ```
4. Clustering Analysis
Apply clustering algorithms with the `Clustering.py` script:
    ```bash
   python scripts/Clustering.py
    ```
5. Link Prediction
Run link prediction analysis using `LinkPrediction.py`:
    ```bash
   python scripts/LinkPrediction.py
    ```
   
# Methodology

## Dataset

The primary dataset used in this project is a drug interaction network with 1514 nodes and 48514 edges, available at [ChCh-Miner](https://snap.stanford.edu/biodata/datasets/10001/10001-ChCh-Miner.html). Each node represents a drug, while an edge between two nodes indicates a known interaction between the corresponding drugs. This dataset serves as the foundation for constructing the graph, calculating centrality measures, and performing clustering and link prediction analysis.

In addition to the drug-drug interaction dataset, we enriched the analysis with drug-target gene interaction data from the publicly available [ChG-Miner dataset](https://snap.stanford.edu/biodata/datasets/10002/10002-ChG-Miner.html). This dataset contains information on interactions between 5017 drugs (including the 1514 drugs from the primary dataset) and 2324 genes, forming 15138 drug-target pairs. The inclusion of drug-target information enabled us to investigate whether drugs within identified clusters act on some common targets.

Furthermore, we used the DrugBank Vocabulary dataset obtained from DrugBank Online, which provides detailed information on each drug, including its common name. This dataset allowed us to link each drug node to its corresponding name for easier interpretation and reporting. While the full DrugBank Vocabulary dataset is not publicly accessible, we extracted the relevant data into a JSON file named `drug_info.json` for use in our analysis.

## Implementation

### Model Class

The `Model.py` file defines a `Model` class that serves as a utility for loading, validating, and visualizing graphs. It includes methods for setting the graph file location, loading the graph data from a JSON file, and handling errors if the file is not set or does not exist. The graph is constructed using NetworkX, supporting both directed and undirected graphs based on the input data. The `draw` method visualizes the graph with node labels, edge weights, and customizable node colors, while the `show` method displays the rendered graph using Matplotlib. This class provides a robust foundation for managing graph data and generating insightful visualizations.

### DrugDrug Class

The `DrugDrug.py` file extends the functionality of the base `Model` class by defining a specialized `DrugDrug` class for handling drug-drug interaction networks. This class automatically sets the file location for the drug-drug interaction graph upon initialization and loads the graph data. By inheriting from the `Model` class, `DrugDrug` retains all the base functionalities for graph visualization and interaction while being tailored specifically for analyzing drug-drug interactions. The `NAME` attribute is defined as `"Drug-Drug"` to provide a clear identifier for this graph type.

### Graph Construction and Filtering

The graph construction and filtering process is implemented in the `extract_graph.py` script. This script processes raw data of drug-drug interactions stored in a TSV file, builds an undirected graph, and filters out smaller connected components to retain meaningful clusters. The key functions and their roles are:

- **`main`**: Serves as the entry point of the script, defining file paths and invoking the `extract_graph` function to process the data and save the resulting graph.
- **`extract_graph`**: Ensures the existence of the raw data file, checks if the graph file already exists, and calls `build_graph` to construct the graph from raw data. The graph is further refined using the `filter_small_components` function to exclude connected components smaller than a predefined size.
- **`build_graph`**: Reads the raw TSV data, identifies unique drugs, and constructs graph nodes and edges. Each node is assigned a unique identifier, label, and color (e.g., blue or green). Edges represent interactions between drugs.
- **`filter_small_components`**: Filters out small connected components from the graph using NetworkX. Only components with a size above the specified threshold are retained, ensuring the graph focuses on significant interaction clusters.
- **`to_node`** and **`to_link`**: Helper functions that create standardized node and link dictionaries for graph representation.

The final output is a JSON file containing the graph structure, with nodes and links explicitly defined. This format is compatible with further analysis and visualization. The graph is saved only if it does not already exist, preventing redundant computations. Error handling is integrated to notify users if the raw data is missing or invalid.

### ExtractDrugData Module

The `extract_drug_data.py` script is responsible for extracting drug-related information, specifically DrugBank IDs and their associated common names, from a CSV file containing DrugBank dataset information. The extracted data is then stored in a JSON format for easy access and integration with other components of the project. The script is structured as follows:

- **`main`**: Serves as the entry point of the script. It defines the input CSV file path and the output JSON file path, then invokes the `extract_drug_data` function to process the data and save the results.
- **`extract_drug_data`**: Reads the CSV file containing drug data, processes each row to extract the DrugBank ID and common name, and stores the results in a dictionary. If either value is missing from a row, the row is skipped with a warning message. The dictionary is then saved as a JSON file, where the keys are DrugBank IDs and the values are the associated common names.

### CalculateAnalytics Module

The `CalculateAnalytics.py` module is responsible for analyzing the connectivity of a graph and its connected components. It calculates various graph-level and node-level features, including centrality measures and clustering coefficients, and visualizes the results using colored graphs. The module is structured as follows:

- **`calculate_analytics`**: Checks if the graph is connected (for undirected graphs) or strongly connected (for directed graphs) and, if not, identifies the connected components. For each component, it invokes `analyze_connected_component`.
- **`analyze_connected_component`**: Performs analysis of a connected component by calculating graph-level features (e.g., diameter, average clustering coefficient) and node-level features (e.g., degree centrality, betweenness centrality). It identifies the top `$k$` nodes based on various centrality measures and visualizes the results with colored graphs.
- **`get_top_k_nodes`**: Retrieves the top `$k$` nodes based on their values in a dictionary.
- **`plot_colored_graph`**: Generates and saves visualizations of the graph with nodes colored according to specific centrality measures.
- **`load_drug_data`**: Loads drug-related data from a JSON file to map drugs to their common names, which are displayed alongside the nodes in the visualizations.

### Clustering Module

The `Clustering.py` module applies community detection algorithms to a graph, compares clustering results, and visualizes the detected clusters. Supported algorithms include:

- **Girvan-Newman**
- **Label Propagation**
- **Louvain**
- **Spectral Clustering**

### LinkPrediction Module

The `LinkPrediction.py` module implements workflows for predicting missing edges in graphs. It evaluates methods like Common Neighbors, Jaccard Coefficient, and Adamic-Adar using metrics such as AUC and precision.
