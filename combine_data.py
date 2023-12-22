# combine data.py
# author: TJ Murphy
# Date: 11/18/2023
# Purpose: This script combines two tab-separated files into one. 
# the files are the flattened tap cli file and the hashes and urls file
print("Running combine_data.py")

import pandas as pd
import argparse
import os

def combine_files(file_path_flattened_tap_cli, file_path_hashes_and_urls, output_file_name):
    df_flattened_tap_cli = pd.read_csv(file_path_flattened_tap_cli, sep='\t')
    df_hashes_and_urls = pd.read_csv(file_path_hashes_and_urls, sep='\t')

    combined_df = pd.merge(df_flattened_tap_cli, df_hashes_and_urls, left_on='name', right_on='Title')

    # Create the output file path in the same directory as the file_path_flattened_tap_cli file
    output_file = os.path.join(os.path.dirname(file_path_flattened_tap_cli), output_file_name)

    combined_df.to_csv(output_file, sep='\t', index=False)
    print(f"Combined file has been written to {output_file}")

if __name__ == "__main__":
    # Setting up the argument parser
    parser = argparse.ArgumentParser(description='Combine two tab-separated files into one.')
    parser.add_argument('file_path_flattened_tap_cli', type=str, help='Path to the flattened tap cli file')
    parser.add_argument('file_path_hashes_and_urls', type=str, help='Path to the hashes and urls file')
    parser.add_argument('output_file', type=str, help='Path to the output file')

    # Parsing the arguments
    args = parser.parse_args()

    # Call the function with the provided file paths
    combine_files(args.file_path_flattened_tap_cli, args.file_path_hashes_and_urls, args.output_file)
