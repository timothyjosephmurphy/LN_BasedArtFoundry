import tweepy
import argparse
import os
import json
import imagehash
from PIL import Image

def post_to_twitter(image_path, input_dir, consumer_key, consumer_secret, access_token, access_token_secret):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth)

    # Compute phash of image
    image = Image.open(image_path)
    phash = imagehash.phash(image)

    # Construct tweet text
    filename = os.path.basename(image_path)
    tweet_text = f"{filename} - {input_dir} - {phash}"

    # Upload image
    media = api.media_upload(image_path)

    # Post tweet with uploaded media
    status = api.update_status(status=tweet_text, media_ids=[media.media_id])
    return status._json  # return the JSON representation of the status

def main():
    parser = argparse.ArgumentParser(description='Post images to Twitter.')
    parser.add_argument('input_dir', help='The input image directory')
    parser.add_argument('credentials_file', help='The file containing Twitter API credentials')

    args = parser.parse_args()

    # Read credentials from file
    with open(args.credentials_file, 'r') as file:
        consumer_key = file.readline().strip()
        consumer_secret = file.readline().strip()
        access_token = file.readline().strip()
        access_token_secret = file.readline().strip()

    statuses = []  # list to store status objects

    for image_name in os.listdir(args.input_dir):
        if image_name.endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(args.input_dir, image_name)
            status = post_to_twitter(image_path, args.input_dir, consumer_key, consumer_secret, access_token, access_token_secret)
            statuses.append(status)  # append status to list

    # write statuses to output file
    with open('x_posts.txt', 'w') as file:
        json.dump(statuses, file)

if __name__ == "__main__":
    main()