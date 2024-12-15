from helpers.CalculateAnalytics import calculate_analytics
from models.DrugDrug import DrugDrug


def main():
    # getting models from datasets
    drug_drug = DrugDrug()

    # calculate analytics
    calculate_analytics(drug_drug)


if __name__ == "__main__":
    main()
