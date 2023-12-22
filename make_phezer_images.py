import os
import sys
from PIL import Image, ImageDraw, ImageFont
import pandas as pd

# Define constants for the columns to print
COLUMNS_TO_PRINT = ['name', 'PHASH', 'URL', 'group_key_x']

def create_image_from_row(row, headers, filename, image_width=1020, image_height=56):
    """
    Creates an image file from the given row data, including selected headers above each value.
    """
    # Create a blank image with white background
    image = Image.new('RGB', (image_width, image_height), 'white')
    draw = ImageDraw.Draw(image)

    # Load a font
    font = ImageFont.load_default()

    # Determine the spacing based on the selected columns
    spacing = image_width // len(COLUMNS_TO_PRINT)

    # Initialize the starting position
    x_position = 10
    for header in COLUMNS_TO_PRINT:
        # Draw the header
        draw.text((x_position, 10), header, fill='black', font=font)

        # Draw the value below the header
        value = str(row[header])
        draw.text((x_position, 25), value, fill='black', font=font)

        # Move to the next position
        x_position += spacing

    # Save the image
    image.save(filename)

def main(input_file):
    # Read the input file
    data = pd.read_csv(input_file, delimiter='\t')

    # Extract headers
    headers = data.columns.tolist()

    # Filter out the columns that are not needed
    data = data[COLUMNS_TO_PRINT]

    # Create output directory
    output_dir = os.path.join(os.path.dirname(input_file), 'phezer images')
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each row and create an image
    for index, row in data.iterrows():
        filename = os.path.join(output_dir, f'{row["name"]}.png')
        create_image_from_row(row, headers, filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    main(input_file)
