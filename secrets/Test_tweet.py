# not working yet
# 453 - You currently have access to a subset of Twitter API v2 endpoints and limited v1.1 endpoints (e.g. media post, oauth) only. If you need access to this endpoint, you may need a different access level. You can learn more here: https://developer.twitter.com/en/portal/product
# Timothys-MacBook-Pro-2:BasedArtFoundry tj$ 

import tweepy

# Twitter API credentials
consumer_key = "K6yw5IQt4XRa63z94sfets4bM"
consumer_secret = "NH28dobp8HKOCal2dhro5cpe0wO7OKKeHy6Y9Il2NFnkYYd7Ag"
access_token = "1594388568570478595-bV8FFBgy8ZDP46ZWG4Gv3fKhHHvLX8"
access_token_secret = "Wln0YHe2TcvORFyfWDyuRq4Uhktx9WlDduKjeipsCnGoI"

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

# Tweet content
tweet_content = "Hello, world! This is my first tweet using Tweepy."

# Post the tweet
try:
    api.update_status(tweet_content)
    print("Tweet successfully posted!")
except Exception as e:
    print(f"An error occurred: {e}")
