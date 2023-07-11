import tweepy
import pandas as pd
import json
from datetime import datetime
import s3fs
from config import api_key, api_secret_key, bearer_token, access_token, access_token_secret

# twitter authentication

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

# load keywords

f = open('text_df.csv', 'r')
search = f.read().splitlines()
del search[0]
f.close()
params = '-filter:retweets AND -filter:replies AND -filter:links'

# search params

no_of_tweets=100
dates = pd.read_csv('temp_df.csv')
dates['Date'] = dates['Date'].astype('datetime64[ns]')
start = str(dates['Date'].dt.date.min())
end = str(dates['Date'].dt.date.max())

# creating an api object

api = tweepy.API(auth, wait_on_rate_limit=True)

try:
        tweets = api.search_tweets(q=search
                           , lang='en'
                           ,count=no_of_tweets
                           ,tweet_mode='extended'
                           ,until=start)
        
        attributes_container = [[tweet.created_at, tweet.favorite_count,tweet.source, tweet.full_text] for tweet in tweets]
        
        columns = ['Date','Likes','Source','Tweet']
        
        tweets_df = pd.DataFrame(attributes_container, columns)
except BaseException as e:
        print('Status Failed on,' str(e))


# tweets = [
# for x in search:
#         for tweet in tweepy.Cursor(api.search_tweets
#                                    ,q=search
#                                    ,lang='en'
#                                    ,result_type='mixed'
#                                    ,count=100)]


