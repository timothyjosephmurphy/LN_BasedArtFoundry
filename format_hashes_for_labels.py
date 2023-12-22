# format_hashes_for_labels.py
# author: TJ Murphy
# Date: 11/18/2023
# Purpose: This script reads a tab-separated file, formats the data for printing on labels, 
# and outputs a pdf file called labels.pdf
print("Running format_hashes_for_labels.py")

import sys
import argparse
import pandas as pd
import qrcode
import tempfile
import os
import json
import subprocess
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from textwrap import wrap


def create_labels_from_file_wrapped(input_file_name, output_pdf_name):
    # Read the input file into a DataFrame
    df = pd.read_csv(input_file_name, sep='\t')

    # Create the output file path in the same directory as the input_file_name file
    output_pdf_path = os.path.join(os.path.dirname(input_file_name), output_pdf_name)

    # Create a new PDF with the labels
    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    # Define label dimensions and margins
    label_width = 4 * inch
    label_height = 2 * inch
    left_margin = 0.4 * inch
    top_margin_adjustment = 0.7 * inch
    initial_top_margin = letter[1] - top_margin_adjustment

    # Define the smaller font size
    font_size = 6.5  # Adjust as needed

    # Define the maximum number of characters per line
    max_char_per_line = 80

    # Calculate the number of labels per row and per column
    labels_per_row = int(letter[0] / label_width)
    labels_per_column = int(letter[1] / label_height)

    for i, row in df.iterrows():
        column = i % labels_per_row
        row_number = i // labels_per_row
        if row_number >= labels_per_column:
            c.showPage()
            row_number = 0

        x = left_margin + column * label_width
        y = initial_top_margin - (row_number * label_height)

        # Set the font size
        c.setFont("Helvetica", font_size)

        # Execute the command and capture its output
        timechainstats = 'echo "$(date -u +%Y-%m-%d\ %T) UTC | 1 BTC = $(curl -s https://api.coindesk.com/v1/bpi/currentprice/usd.json | grep -o \'rate":"[^"]*\' | cut -d\\" -f3) USD | Block Height = $(curl -s https://blockchain.info/q/getblockcount)"'
        btc_info = subprocess.check_output(timechainstats, shell=True).decode('utf-8').strip()
        # Wrapping text for each field
        wrapped_text = []
        for field in ['Title','URL', 'group_key_x']:
            wrapped_text += wrap(f"{field}: {row[field]}", max_char_per_line)
        # Add the BTC info
        wrapped_text += wrap(btc_info, max_char_per_line)

        # Add the constant string
        wrapped_text += wrap("Email: TimothyJosephMurphy@gmail.com | Phone: 206-471-0639 | @TJ_de_la_playa", max_char_per_line)

        # Drawing text with reduced font size
        y_offset = y
        for line in wrapped_text:
            c.drawString(x, y_offset, line)
            y_offset -= font_size * 1.2  # Adjust the spacing based on the font size
        # Define the data for each QR code
        image_data = {field: row[field] for field in ['Title', 'SHA256', 'PHASH', 'URL']}
        # asset_data = {field: row[field] for field in ['batch_key', 'batch_txid', 'data', 'meta_hash', 'group_key']}
        asset_data = {field: row[field] for field in ['asset_meta.data', 'asset_meta.meta_hash', 'group_key_x']}
        artist_data = "Email: TimothyJosephMurphy@gmail.com | Phone: 206-471-0639 | @TJ_de_la_playa"

        # Generate each QR code
        qr_codes = []
        for data in [image_data, asset_data, artist_data]:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(json.dumps(data))
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            # Save the QR code to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                img.save(tmp.name)
                qr_codes.append(tmp.name)
        # Draw each QR code on the canvas
        qr_size = 75  # Size of QR code
        qr_labels = ['Image', 'Certificate', 'Artist']
        for i, tmp_name in enumerate(qr_codes):
            img_reader = ImageReader(tmp_name)
            qr_x = x + i * (qr_size + 10)  # Add 10 for spacing between QR codes
            qr_y = y_offset - qr_size

            # Draw the QR code
            c.drawImage(img_reader, qr_x, qr_y, width=qr_size, height=qr_size)

            # Draw the label below the QR code, shifted to the right by 20 whitespace characters
            label_y = qr_y - 10  # Subtract 10 for spacing between the label and the QR code
            c.drawString(qr_x, label_y, ' ' * 13
                          + qr_labels[i])

            # Delete the temporary file
            os.remove(tmp_name)

    c.save()

def main():
    parser = argparse.ArgumentParser(description='Create labels from file.')
    parser.add_argument('input_file', help='The input file to create labels from.')
    parser.add_argument('output_file', help='The output file to write the labels to.')
    args = parser.parse_args()

    create_labels_from_file_wrapped(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
