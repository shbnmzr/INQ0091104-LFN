import csv
import json


def main():
    input_csv = "../raw_data/private/drugbank_vocabulary.csv"
    output_file = "../graphs/drug_data.json"

    # Extract data from the CSV file and save it to JSON
    extract_drug_data(input_csv, output_file)


def extract_drug_data(input_csv, output_file):
    """
    Extract DrugBank IDs and their common names from the DrugBank dataset CSV file.
    Save the results to a JSON file.
    """
    results = {}

    with open(input_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        for row in reader:
            drug_id = row.get("DrugBank ID")
            common_name = row.get("Common name")

            if drug_id and common_name:
                results[drug_id] = {"common_name": common_name}
            else:
                print(f"Skipping row with missing data: {row}")

    # Save the results to a JSON file
    with open(output_file, 'w') as jsonfile:
        json.dump(results, jsonfile, indent=2)

    print(f"Extracted drug data saved to {output_file}")


if __name__ == "__main__":
    main()
