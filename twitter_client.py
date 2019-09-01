from TwitterAPI import TwitterAPI
from twitter_creds import consumer_key
from twitter_creds import consumer_secret
from twitter_creds import access_token_key
from twitter_creds import access_token_secret
import buoy_data

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

data = buoy_data.fetchRealTime2Data(44011)
status = buoy_data.airTempStatus(data)

print(status)