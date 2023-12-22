# convert_heic_dir.py
# Author: TJ Murphy
# Date: 11/18/2023
# Purpose: Convert all HEIC files in a directory to JPG files using ImageMagick
print("Running convert_heic_dir.py")
import sys
import os
import subprocess

def convert_heic_to_jpg(heic_path):
    jpg_path = os.path.splitext(heic_path)[0] + ".jpg"
    subprocess.run(["magick", heic_path, jpg_path])

if len(sys.argv) > 1:
    directory = sys.argv[1]
    for filename in os.listdir(directory):
        if filename.endswith(".HEIC") or filename.endswith(".heic"):
            convert_heic_to_jpg(os.path.join(directory, filename))
else:
    print("Please provide a directory path.")