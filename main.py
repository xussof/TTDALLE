

import tweepy
import os

access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
api_key = os.environ['API_KEY']
api_key_secret = os.environ['API_KEY_SECRET']

dalle_api_key = os.environ['DALLE_API_KEY']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key, 
    api_key_secret)
auth.set_access_token(access_token, 
    access_token_secret)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def get_top_countries(api):
    top_countries = []
    for tweet in tweepy.Cursor(api.search_users, q='', lang='en').items(20):
        if tweet.location:
            top_countries.append(tweet.location)
    
    top_countries_woeid = []
    for country in top_countries:
        woeid = api.trends_location(q = country)[0]['woeid']
        top_countries_woeid.append(woeid)
    return top_countries_woeid

print(get_top_countries(api))