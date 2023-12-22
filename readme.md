# BasedArtFoundry

**Author:** TJ Murphy  
**Date:** 11/18/2023  

## Description

BasedArtFoundry is a tool used to create digital certificates of authenticity for physical art using a taproot asset anchored in the Bitcoin blockchain to act as the certificate. 

## Process

The process involves the following steps:

1. Check the balance of the lightning wallet.
2. Take a directory of images which are photographs of physical art.
3. Convert them to jpgs.
4. Deskew them.
5. Find their phash, upload them to imgur, and find the SHA256 of the uploaded image.
6. Mint certificates based on this data using taproot assets.
7. Combine the data from the taproot minting process with the data from imgur.
8. Print labels for them.
9. Calculate the amount spent in sats.

## Requirements

This tool requires a locally running Bitcoin, Lightning, and Taproot node.

## Usage

Run the `BasedArtFoundry.py` script to start the process:

```bash
python BasedArtFoundry.py