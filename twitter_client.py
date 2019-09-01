from TwitterAPI import TwitterAPI
from twitter_creds import *
import buoy_data
import pprint

api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

#get new data for buoy 44011
data = buoy_data.fetchRealTime2Data(44011)

#get status for air temps
newstatus = buoy_data.airTempStatus(data)

#post tweet
r = api.request('statuses/update', 
    {'status': newstatus, 
    'lat': buoy_data.buoyLat(), 
    'long': buoy_data.buoyLong(), })

#r = api.request('geo/search', {'lat': buoy_data.buoyLat(), 
#    'long': buoy_data.buoyLong()
#    },None,'GET')

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(r.json()) 