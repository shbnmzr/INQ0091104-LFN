import csv
import os
import json


def main():
    output_path = "../graphs/drug_target_data.json"
    input_data_path = '../raw_data/ChG-Miner_miner-chem-gene.tsv'

    # Extract data from the TSV file and save it to JSON
    extract_drug_target_data(input_data_path, output_path)


def extract_drug_target_data(input_data_path, output_path):
    if not os.path.exists(input_data_path):
        exit(f"Input data file not found at {input_data_path}")

    if os.path.exists(output_path):
        exit(f"Drug-gene data file already exists at {output_path}")

    results = {}

    # Read drug-gene data from the specified file
    with open(input_data_path, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')

        # Skip header row
        next(tsv_reader, None)

        for row in tsv_reader:
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue

            drug, gene = row[0], row[1]
            if drug in results:
                results[drug]["genes"].append(gene)
            else:
                results[drug] = {"genes": [gene]}

    # Save results to JSON
    with open(output_path, 'w') as json_file:
        json.dump(results, json_file, indent = 2)

    print(f"Extracted drug-gene data saved to {output_path}")


if __name__ == "__main__":
    main()
