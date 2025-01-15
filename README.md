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
