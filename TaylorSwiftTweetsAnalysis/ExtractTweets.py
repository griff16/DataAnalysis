# This code extracts Taylor Swfit's recent tweets (up to 3200) and output to a csv file
# This code requires the user to have Twitter's developer account and have set those keys as their OS environment variables
# to set environment variable just type [export TWITTER_ACCESS_TOKEN="YOUR KEYS"] on a terminal

import os
import json
import tweepy
import pandas as pd


ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_SECRET')
CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')


def printj(data):
    print(json.dumps(data, indent=4, sort_keys=True))


# Setup access to API
def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    return tweepy.API(auth)


def extract_tweet_attributes(api, target_name):
    # create empty list
    tweet_list = []

    # loop through tweet objects
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=target_name, twee_mode='extended').items():
        tweet_id = tweet.id  # unique integer identifier for tweet
        text = tweet.text  # utf-8 text of tweet
        favorite_count = tweet.favorite_count  # number of time this tweet liked
        retweet_count = tweet.retweet_count  # number of times this tweet retweeted
        created_at = tweet.created_at  # utc time tweet created
        source = tweet.source  # utility used to post tweet
        reply_to_status = tweet.in_reply_to_status_id  # if reply int of orginal tweet id
        location = tweet.geo
        reply_to_user = tweet.in_reply_to_screen_name

        # append attributes to list
        tweet_list.append({'tweet_id': tweet_id,
                           'text': text,
                           'likes': favorite_count,
                           'retweets': retweet_count,
                           'created_at': created_at,
                           'source': source,
                           'reply_to_status': reply_to_status,
                           'reply_to_user': reply_to_user,
                           'location': location})

    # create dataframe
    df = pd.DataFrame(tweet_list, columns=['tweet_id',
                                           'text',
                                           'likes',
                                           'retweets',
                                           'created_at',
                                           'source',
                                           'reply_to_status',
                                           'reply_to_user',
                                           'location'])

    return df


def main():
    pd.options.display.max_columns = None
    pd.options.display.width = None

    api = connect_to_twitter_OAuth()  # Create API object
    df = extract_tweet_attributes(api, '@taylorswift13')
    df.to_csv(r'./taylor_swift_tweets.csv')


# main entry point
if __name__ == '__main__':
    main()
