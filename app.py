from helpers.CalculateAnalytics import calculate_analytics
from helpers.Clustering import compare_clustering
from helpers.LinkPrediction import link_prediction_workflow
from models.DrugDrug import DrugDrug


def main():
    # getting models from datasets
    drug_drug = DrugDrug()

    # calculate analytics
    calculate_analytics(drug_drug)

    # compare clustering algorithms
    compare_clustering(drug_drug.graph)

    # compare link prediction algorithms
    link_prediction_workflow(drug_drug.graph)


if __name__ == "__main__":
    main()
