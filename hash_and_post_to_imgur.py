# hash_and_post_to_imgur.py
# Date: 11/18/2023 
# Author: TJ Murphy
# Purpose: 
#   Find the phash of the image
#   Upload the image to imgur
#   Find the sha256 of the image using the imgur url
#   Write the filename, phash, url, and sha256 hash to a file
print("Running hash_and_post_to_imgur.py")
import os
import sys
import hashlib
import argparse
import json
from imgurpython import ImgurClient
from PIL import Image
from imagehash import phash
import requests

client_id='777656888384970'
client_secret='27689d9a4fcd39cc16306cfaf91f03a910813b13'

def get_sha256(image_url):
    response = requests.get(image_url)
    sha256_hash = hashlib.sha256(response.content).hexdigest()
    return sha256_hash

def get_phash(image_path):
    image = Image.open(image_path)
    return str(phash(image))

# 11/18/2023 reordered this fucntion to find the sha256 hash of the image after uploading it to imgur
def upload_images(dir_path):
    client = ImgurClient(client_id, client_secret)
    with open(os.path.join(dir_path, 'Hashes_and_urls.txt'), 'w') as f:
        dir_path = dir_path.rstrip('/')  # Remove trailing slash
        group_key = os.path.basename(os.path.dirname(dir_path))
        f.write('Title\tSHA256\tPHASH\tURL\tgroup_key\n')
        for file_name in os.listdir(dir_path):
            if file_name.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(dir_path, file_name)
                phash_hash = get_phash(image_path)
                response = client.upload_from_path(image_path, config={'title': file_name}, anon=True)
                sha256_hash = get_sha256(response["link"])
                f.write(f'{file_name}\t{sha256_hash}\t{phash_hash}\t{response["link"]}\t{group_key}\n')

if len(sys.argv) > 1:
    dir_path = sys.argv[1]
    upload_images(dir_path)
else:
    print("Please provide a directory path.")