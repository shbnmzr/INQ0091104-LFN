import networkx as nx
import random
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score, f1_score


def split_graph_for_link_prediction(graph, test_fraction=0.1, seed=42):
    """
    Splits the graph into training and testing sets by removing a fraction of edges.

    Parameters:
        - graph (networkx.Graph): The input graph.
        - test_fraction (float): Fraction of edges to remove for testing.
        - seed (int): Random seed for reproducibility.

    Returns:
        tuple: (training_graph, test_edges, test_non_edges)
    """
    random.seed(seed)

    # Remove a fraction of edges for testing
    edges = list(graph.edges)
    num_test_edges = int(len(edges) * test_fraction)
    test_edges = random.sample(edges, num_test_edges)

    training_graph = graph.copy()
    training_graph.remove_edges_from(test_edges)

    # Generate a set of non-edges for evaluation
    non_edges = list(nx.non_edges(training_graph))
    test_non_edges = random.sample(non_edges, num_test_edges)

    return training_graph, test_edges, test_non_edges


def compute_link_prediction_scores(graph, edge_list, method):
    """
    Computes scores for the given edge list using the specified method.

    Parameters:
        - graph (networkx.Graph): The input graph.
        - edge_list (list): List of edges to score.
        - method (str): The link prediction method.

    Returns:
        list: Scores for the edges.
    """
    if method == "Common Neighbors":
        return [len(list(nx.common_neighbors(graph, u, v))) for u, v in edge_list]

    if method == "Jaccard Coefficient":
        return [score for _, _, score in nx.jaccard_coefficient(graph, edge_list)]

    if method == "Adamic Adar":
        return [score for _, _, score in nx.adamic_adar_index(graph, edge_list)]

    if method == "Preferential Attachment":
        return [score for _, _, score in nx.preferential_attachment(graph, edge_list)]

    raise ValueError(f"Unknown method: {method}")


def evaluate_predictions(edges, non_edges, scores, threshold=None):
    """
    Evaluates link prediction performance using precision, recall, AUC, and average precision.

    Parameters:
        - edges (list): List of existing edges in the graph.
        - non_edges (list): List of non-existing edges in the graph.
        - scores (list): Predicted scores for all edges (existing and non-existing combined).
        - threshold (float, optional): Threshold for converting scores into binary predictions.

    Returns:
        dict: Evaluation metrics (AUC, Average Precision, Precision, Recall, F1 Score).
    """
    # Combine edges and labels
    y_true = [1] * len(edges) + [0] * len(non_edges)

    # Use a threshold to create binary predictions
    if threshold is None:
        # Default threshold: mean of scores
        threshold = sum(scores) / len(scores)

    y_pred = [1 if score >= threshold else 0 for score in scores]

    # Calculate metrics
    auc = roc_auc_score(y_true, scores)
    ap = average_precision_score(y_true, scores)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return {"AUC": auc,
            "Average Precision": ap,
            "Precision": precision,
            "Recall": recall,
            "F1 Score": f1
            }


def link_prediction_workflow(graph, test_fraction=0.1):
    """
    Full workflow for link prediction: edge removal, prediction, and evaluation.

    Parameters:
        - graph (networkx.Graph): The input graph.
        - test_fraction (float): Fraction of edges to remove for testing.

    Returns:
        None
    """
    # Step 1: Prepare the graph
    training_graph, test_edges, test_non_edges = split_graph_for_link_prediction(graph, test_fraction)
    print(f"Training graph has {training_graph.number_of_edges()} edges.")
    print(f"Testing with {len(test_edges)} positive and {len(test_non_edges)} negative edges.")

    # Step 2: Define methods and evaluate
    methods = ["Common Neighbors", "Jaccard Coefficient", "Adamic Adar", "Preferential Attachment"]
    results = {}

    for method in methods:
        print(f"\nEvaluating method: {method}")
        # Step 3: Compute prediction scores
        test_combined_edges = test_edges + test_non_edges
        scores = compute_link_prediction_scores(training_graph, test_combined_edges, method)

        # Step 4: Evaluate predictions
        evaluation = evaluate_predictions(test_edges, test_non_edges, scores)
        results[method] = evaluation

        print(f"  - AUC: {evaluation['AUC']:.4f}")
        print(f"  - Average Precision: {evaluation['Average Precision']:.4f}")
        print(f"  - Precision: {evaluation['Precision']:.4f}")
        print(f"  - Recall: {evaluation['Recall']:.4f}")
        print(f"  - F1 Score: {evaluation['F1 Score']:.4f}")

    # Step 5: Display comparison
    print("\nComparison of Link Prediction Methods:")
    for method, metrics in results.items():
        print(f"{method}:")
        print(f"  - AUC: {metrics['AUC']:.4f}")
        print(f"  - Average Precision: {metrics['Average Precision']:.4f}")
        print(f"  - Precision: {metrics['Precision']:.4f}")
        print(f"  - Recall: {metrics['Recall']:.4f}")
        print(f"  - F1 Score: {metrics['F1 Score']:.4f}")
