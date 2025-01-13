import csv
import os
import json


def extract_drug_target_data(input_data_path, output_path):
    """
    Extracts drug-target gene data from a TSV file and saves it to a JSON file.

    Parameters:
        input_data_path (str): Path to the input TSV file containing drug-gene mappings.
        output_path (str): Path to save the output JSON file.
    """
    # Check if input file exists
    if not os.path.exists(input_data_path):
        exit(f"Input file not found at: {input_data_path}")

    # Prevent overwriting an existing output file
    if os.path.exists(output_path):
        exit(f"Output file already exists at {output_path}")

    results = {}

    # Read drug-gene data from the specified file
    with open(input_data_path, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter='\t')

        # Skip header row
        next(tsv_reader, None)

        # Process each row in the TSV file
        for row in tsv_reader:
            if len(row) != 2:
                print(f"Skipping invalid row: {row}")
                continue

            drug, gene = row[0], row[1]

            # Add gene to the corresponding drug
            if drug in results:
                results[drug]["genes"].append(gene)
            else:
                results[drug] = {"genes": [gene]}

    # Save results to a JSON file
    with open(output_path, 'w') as json_file:
        json.dump(results, json_file, indent=2)

    print(f"Extracted drug-gene data saved to {output_path}")


if __name__ == "__main__":
    output = "../graphs/drug_gene_data.json"
    input_data = '../raw_data/ChG-Miner_miner-chem-gene.tsv'

    # Extract data from the TSV file and save it to JSON
    extract_drug_target_data(input_data, output)
