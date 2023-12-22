#  BasedArtFoundry.py
#  Author: TJ Murphy
#  Date: 11/18/2023
#  Purpose: BasedArtFoundry is a tool used to create digital certificates of authenticity for physical art 
#  using a taproot asset anchored in the Bitcoin blockchain to act as the certificate. 
#  The process is as follows:
#   Check the balance of the lightning wallet
#   take a directory of images which are photographs of physical art, 
#   convert them to jpgs, 
#   deskew them, 
#   find their phash, upload them to imgur, and find the SHA256 of the uploaded image, 
#   mint certificates based on this data using taproot assets,  
#   combine the data from the taproot minting process with the data from imgur,
#   print labels for them
#   calculate the amount spent in sats
# REQUIRES: a locally running bitcoin, lightning, and taproot node

#Application: 
print("Running BasedArtFoundry.py")

import subprocess
import argparse
import os
import sys
import json
import requests

# Helper function to get the balance of the wallet, used to calculate the amount spent in sats
def get_balance():
    result = subprocess.run(['lncli', 'walletbalance'], stdout=subprocess.PIPE)
    data = json.loads(result.stdout)
    balance = float(data['total_balance'])
    return balance

# Helper function to get the current price of bitcoin
def get_bitcoin_price():
    response = requests.get('https://api.coindesk.com/v1/bpi/currentprice/BTC.json')
    data = response.json()
    price = float(data['bpi']['USD']['rate'].replace(',', ''))
    return price

def chain_scripts(input_dir):
    # get the starting balance of the local LN wallet and calculate the dollar value of the starting balance
    price = get_bitcoin_price()
    starting_balance = get_balance()
    dollar_value_of_starting_balance = round((starting_balance * price)/100000000,2)
    print("Starting balance: ", starting_balance, "sats, $", dollar_value_of_starting_balance)

    scripts = [
        ('convert_heic_dir.py', [input_dir]),
        ('deskew.py', [input_dir]),
        ('hash_and_post_to_imgur.py', [input_dir]),
        ('mint_taproot_assets.py', [input_dir]),
        ('parse_json_into_table.py', [os.path.join(input_dir, 'tapcli_output.txt'), 'flattened_tap_cli.txt']),
        ('combine_data.py', [os.path.join(input_dir, 'flattened_tap_cli.txt'), os.path.join(input_dir, 'Hashes_and_urls.txt'), 'combined_data.txt']),
        ('format_hashes_for_labels.py', [os.path.join(input_dir, 'combined_data.txt'), os.path.join(input_dir, 'labels.pdf')]),
        ('send_to_printer.py', [os.path.join(input_dir, 'labels.pdf')]),
        ('make_phezer_images.py', [os.path.join(input_dir, 'combined_data.txt')])
    ]

    for script, args in scripts:
        result = subprocess.run(['python3', script] + args)
        if result.returncode != 0:
            print(f"Error running {script}. Exiting.")
            sys.exit(1)

    # get the ending balance of the local LN wallet and calculate the amount spent
    ending_balance = get_balance()
    amount_spent = starting_balance - ending_balance
    dollar_value_of_ending_balance = round((ending_balance * price)/100000000,2)
    dollar_value_of_amount_spent = round((amount_spent * price)/100000000,2)
    print("Ending balance:", ending_balance, "sats, $", dollar_value_of_ending_balance)
    print("Amount spent:", amount_spent, "sats, $", dollar_value_of_amount_spent)

def main():
    parser = argparse.ArgumentParser(description='Chain together scripts.')
    parser.add_argument('input_dir', help='The directory of images to feed into convert_heic_dir.py')
    args = parser.parse_args()
   
    chain_scripts(args.input_dir)

if __name__ == "__main__":
    main()



# Todo: 
# - create a thumbnail of the collection of images together
# - publish to Proof of Existence, get bitcoin hash
