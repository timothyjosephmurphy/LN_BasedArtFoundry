# parse_json_into_table.py
# Author: TJ Murphy
# Date: 11/18/2023
# Purpose: This script reads a JSON file, converts the JSON objects into a pandas DataFrame, and writes the DataFrame to a CSV file in the same directory as the input file.
print("Running parse_json_into_table.py")
import pandas as pd
import json
import argparse
import os


def convert_json_to_dataframe(input_file, output_file_name):
    with open(input_file, 'r') as file:
        if os.stat(input_file).st_size == 0:
            print(f"File is empty: {input_file}")
            return
        try:
            json_data = json.load(file)
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {input_file}")
            return

    # Read the JSON content from the file
    with open(input_file, 'r') as file:
        json_data = json.load(file)

    # Extracting the list of JSON objects (assets)
    assets_data = json_data['batch']['assets']

    # Converting the list of JSON objects into a DataFrame
    assets_df = pd.json_normalize(assets_data)

    # Extracting the directory of the input file
    input_dir = os.path.dirname(input_file)

    # Constructing the full path for the output file
    output_file = os.path.join(input_dir, output_file_name)

    # Write the DataFrame to the output file
    assets_df.to_csv(output_file, sep='\t', index=False)
    print(f"Data has been written to {output_file}")

if __name__ == "__main__":
    # Setting up the argument parser
    parser = argparse.ArgumentParser(description='Convert JSON in a file to a tabular TSV format.')
    parser.add_argument('input_file', type=str, help='Path to the input file containing JSON data')
    parser.add_argument('output_file_name', type=str, help='Name of the output file')

    # Parsing the arguments
    args = parser.parse_args()

    # Call the function with the provided input file path and output file name
    convert_json_to_dataframe(args.input_file, args.output_file_name)

