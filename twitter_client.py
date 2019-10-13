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

#general post tweet
def postMedia(imagePath: str,updateContent: dict) -> None:
    # STEP 1 - upload image
    file = open(imagePath, 'rb')
    data = file.read()
    r = api.request('media/upload', None, {'media': data})
    print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE: ' + r.text)

# STEP 2 - post tweet with a reference to uploaded image
    if r.status_code == 200:
        media_id = r.json()['media_id']
        updateContent.update({'media_ids': media_id})
        r = api.request('statuses/update', updateContent)
        print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE: ' + r.text)

#get status for air temps and post it
def airTempTweet(data: DataFrame) -> None:
    newstatus = buoy_data.airTempStatus(data)+''
    updateContent = {'status': newstatus, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def waterTempTweet(data: DataFrame) -> None:
    newstatus = buoy_data.waterTempStatus(data)+''
    updateContent = {'status': newstatus, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def windSpeedTweet(data: DataFrame) -> None:
    newstatus = buoy_data.windSpeedStatus(data)+''
    updateContent = {'status': newstatus, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def latestMeasurementTweet(data: DataFrame) -> None:
    newstatus = buoy_data.measurementStatus(data)+'\n'
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

def postReply(message: str, inReplyTo: str) -> None:
    updateContent = {'status': message, 'in_reply_to_status_id': inReplyTo, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def postBuoyCam(message: str) -> None:
    updateContent = {'status': message, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postMedia('buoycam/Z12A_2019_10_11_1910.jpg',updateContent)
    pass

#example of posting to twitter different data
#TODO figure out how to make this a general purpose CLI
#postGeneralMessage('NOAA Buoy 44011 is testing some new python functions tonight. Prepping for #HurricaneDorian later this week.')
#postReply('@NWSBoston https://twitter.com/AltBuoy44011/status/1170298502125146112?s=20', '1170285282928644096')
latestMeasurementTweet(data)
postBuoyCam('Subtropical Storm Melissa churning the water at Station 44011 on Georges Bank as it moves off the U.S. East Coast. \n\n Image Credit NOAA/NWS/NDBC\n@NOAA @NWSBoston @NHC_Atlantic' )
waterTempTweet(data)
#windSpeedTweet(data)
airTempTweet(data)


#geo/search not returning anything for oceanic Lat/Long locations?
#r = api.request('geo/search', {'lat': buoy_data.buoyLat(), 
#    'long': buoy_data.buoyLong()
#    },None,'GET')