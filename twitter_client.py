from TwitterAPI import TwitterAPI
from twitter_creds import *
from pandas import DataFrame
import buoy_data
import pprint

#init TwitterAPI with your own credentials
api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

#get new data for buoy 44011
data = buoy_data.fetchRealTime2Data(44011)

#general post tweet
def postTweet(updateContent: dict) -> None:
    r = api.request('statuses/update', updateContent)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(r.json()) 
    pass

#get status for air temps and post it
def airTempTweet(data: DataFrame) -> None:
    newstatus = buoy_data.airTempStatus(data)
    updateContent = {'status': newstatus, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def waterTempTweet(data: DataFrame) -> None:
    newstatus = buoy_data.waterTempStatus(data)+' #HurricaneDorian'
    updateContent = {'status': newstatus, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def windSpeedTweet(data: DataFrame) -> None:
    newstatus = buoy_data.windSpeedStatus(data)+' #HurricaneDorian'
    updateContent = {'status': newstatus, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def postStationInfo() -> None:
    newstatus = 'Station 44011 (LLNR 825) - GEORGES BANK 170 NM East of Hyannis, MA\nOwned and maintained by National Data Buoy Center\n3-meter foam buoy\nSCOOP payload\n41°4\'12\" N 66°35\'16\" W\nhttps://www.ndbc.noaa.gov/station_page.php?station=44011'
    updateContent = {'status': newstatus, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def postGeneralMessage(message: str) -> None:
    updateContent = {'status': message, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

#postGeneralMessage('NOAA Buoy 44011 is testing some new python functions tonight. Prepping for #HurricaneDorian later this week.')
waterTempTweet(data)
windSpeedTweet(data)

#geo/search not returning anything for oceanic Lat/Long locations?
#r = api.request('geo/search', {'lat': buoy_data.buoyLat(), 
#    'long': buoy_data.buoyLong()
#    },None,'GET')