# send_to_printer.py
# author: TJ Murphy
# Date: 11/18/2023
# Purpose: Print the pdf output of format_hashes_for_labels.py to the local default printer.
print("Running send_to_printer.py")

import os
import argparse

def print_pdf(pdf_file):
    # Use the lpr command to print the PDF file to the default printer
    os.system(f'lpr "{pdf_file}"')

def main():
    parser = argparse.ArgumentParser(description='Print a PDF file to the local default printer.')
    parser.add_argument('filename', help='The name of the file to be printed')

    args = parser.parse_args()

    print_pdf(args.filename)

if __name__ == "__main__":
    main()