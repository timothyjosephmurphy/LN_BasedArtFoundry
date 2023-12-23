# mint_taproot_assets.py
# author: TJ Murphy
# Date: 11/18/2023
# Purpose: This script mints taproot assets based on the data in the input file.
print("Running mint_taproot_assets.py")
import csv
import json
import subprocess
import sys
import os

def mint_asset(title, sha256, phash, url, group_key):
    meta_data = json.dumps({
        'title': title,
        'sha256': sha256,
        'phash': phash,
        'url': url
    })
    command = f'tapcli --network mainnet a m --type collectible --name "{title}" --supply 1 --meta_bytes \'{meta_data}\' --enable_emission false --group_key "{group_key}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def mint_assets_from_file(dir_path):
    file_path = os.path.join(dir_path, 'Hashes_and_urls.txt')
    output_file_path = os.path.join(os.path.dirname(file_path), 'tapcli_output.txt')
    with open(file_path, 'r') as f, open(output_file_path, 'w') as output_file:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            title = row['Title']
            sha256 = row['SHA256']
            phash = row['PHASH']
            url = row['URL']
            group_key = row['group_key']
            asset_id = mint_asset(title, sha256, phash, url, group_key)
        # THIS BLOCK SPENDS REAL MONEY:      
        command2 = 'tapcli -n mainnet a m f'
        result2 = subprocess.check_output(command2, shell=True, text=True)
        # #  for testing purposes: substitute the following line for the previous line:
        # with open('/Users/tj/Documents/Paintings Nov 18 2023/corrected/tapcli_output.txt', 'r') as file:
        #     result2 = file.read()        
        output_file.write(result2)

if len(sys.argv) > 1:
    mint_assets_from_file(sys.argv[1])
else:
    print("Please provide the input file as a command line argument.")