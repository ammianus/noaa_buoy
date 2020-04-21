from TwitterAPI import TwitterAPI
from twitter_creds import *
from pandas import DataFrame
from clint import arguments
from clint.textui import puts, colored, indent
import buoy_data
import pprint

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

    latestImage = 'plots/windspeed.png'
    postMedia(latestImage,updateContent)

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
    updateContent = {'status': message.replace("\\n", "\n"), 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def postReply(message: str, inReplyTo: str) -> None:
    updateContent = {'status': message, 'in_reply_to_status_id': inReplyTo, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
    postTweet(updateContent)
    pass

def postBuoyCam(message: str) -> None:
    latestImage = buoy_data.fetchBuoyCamImage(44011)
    if latestImage != 'n/a':
        updateContent = {'status': message, 'lat': buoy_data.buoyLat(), 'long': buoy_data.buoyLong(), }
        postMedia('buoycam/latest.jpg',updateContent)
        pass
    else:
        #do nothing
        pass
    pass

def retweet(tweetId) -> None:
    r = api.request('statuses/retweet/:%s' % tweetId)
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(r.json()) 
    pass

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

#example of posting to twitter different data
#TODO figure out how to make this a general purpose CLI
#postGeneralMessage('NOAA Buoy 44011 is testing some new python functions tonight. Prepping for #HurricaneDorian later this week.')
#postReply('@NWSBoston https://twitter.com/AltBuoy44011/status/1170298502125146112?s=20', '1170285282928644096')
#latestMeasurementTweet(data)
#postBuoyCam('#BuoyCam from Station 44011. \n\n Image Credit NOAA/NWS/NDBC\n@NOAA' )
#waterTempTweet(data)
#windSpeedTweet(data)
#airTempTweet(data)


#geo/search not returning anything for oceanic Lat/Long locations?
#r = api.request('geo/search', {'lat': buoy_data.buoyLat(), 
#    'long': buoy_data.buoyLong()
#    },None,'GET')

#
# start CLI program
#
args = arguments.Args()

with indent(4, quote='>>>'):
    puts(colored.red('Aruments passed in: ') + str(args.all))
    #puts(colored.red('Flags detected: ') + str(args.flags))
    #puts(colored.red('Files detected: ') + str(args.files))
    #puts(colored.red('NOT Files detected: ') + str(args.not_files))
    puts(colored.red('Grouped Arguments: ') + str(dict(args.grouped)))

commands = args.grouped.get('_')
puts(colored.cyan('Commands: ')+str(commands))

if commands != None and len(commands) > 0:
    primaryCommand = commands[0]
    secondaryCommand = commands[1]
    #post buoycam - post buoycam image with message
    if primaryCommand.casefold() == 'post'.casefold() and secondaryCommand.casefold() == 'buoycam'.casefold():
        #init TwitterAPI with your own credentials
        puts(colored.cyan('Access TwitterAPI'))
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

        defaultMessage = '#BuoyCam from Station 44011. \n\n Image Credit NOAA/NWS/NDBC\n@NOAA'
        if args.grouped.get('-m') != None:
            message = args.grouped.get('-m')[0]
            pass
        else:
            message = defaultMessage
            pass

        with indent(4, quote='>>>'):
            puts(colored.blue('post buoycam'))
            puts(colored.blue(message))
        postBuoyCam('#BuoyCam from Station 44011 Georges Bank, Atlantic Ocean. \n\nImage Credit NOAA/NWS/NDBC\n@NOAA' )
        pass
    #post latest - latst buoy measurements
    elif primaryCommand.casefold() == 'post'.casefold() and secondaryCommand.casefold() == 'latest'.casefold():
        #init TwitterAPI with your own credentials
        puts(colored.cyan('Access TwitterAPI'))
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

        #get new data for buoy 44011
        puts(colored.cyan('Fetch Data For: ')+str(44011))
        data = buoy_data.fetchRealTime2Data(44011)
        
        puts(colored.blue('post latest'))
        latestMeasurementTweet(data)
        pass
    #post tweet - general messages, no data from buoy 
    elif primaryCommand.casefold() == 'post'.casefold() and secondaryCommand.casefold() == 'tweet'.casefold():
        #init TwitterAPI with your own credentials
        puts(colored.cyan('Access TwitterAPI'))
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

        if args.grouped.get('-m') != None:
            message = args.grouped.get('-m')[0]
            pass
        else:
            puts(colored.red('Message argument (-m) is required'))
            raise InputError

        with indent(4, quote='>>>'):
            puts(colored.blue('post tweet'))
            puts(colored.blue(message))
        postGeneralMessage(message)
        pass 
    #post reply - reply to another tweet 
    elif primaryCommand.casefold() == 'post'.casefold() and secondaryCommand.casefold() == 'reply'.casefold():
        #init TwitterAPI with your own credentials
        puts(colored.cyan('Access TwitterAPI'))
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

        if args.grouped.get('-m') != None:
            message = args.grouped.get('-m')[0]
            pass
        else:
            puts(colored.red('Message argument (-m) is required'))
            raise InputError

        if args.grouped.get('-r') != None:
            inReplyTo = args.grouped.get('-r')[0]
            pass
        else:
            puts(colored.red('Reply to argument (-r) is required'))
            raise InputError

        with indent(4, quote='>>>'):
            puts(colored.blue('post reply'))
            puts(colored.blue(message))
            puts(colored.blue(inReplyTo))
        
        postReply(message, inReplyTo)
        pass 
    elif primaryCommand.casefold() == 'post'.casefold() and secondaryCommand.casefold() == 'windspeed'.casefold():
        #init TwitterAPI with your own credentials
        puts(colored.cyan('Access TwitterAPI'))
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

        #get new data for buoy 44011
        puts(colored.cyan('Fetch Data For: ')+str(44011))
        data = buoy_data.fetchRealTime2Data(44011)

        with indent(4, quote='>>>'):
            puts(colored.blue('post windspeed'))
            
        windSpeedTweet(data)
    elif primaryCommand.casefold() == 'retweet':
        #init TwitterAPI with your own credentials
        puts(colored.cyan('Access TwitterAPI'))
        api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

        if args.grouped.get('-id') != None:
            tweetId = args.grouped.get('-id')[0]
            puts(colored.blue('retweet id: '+tweetId+'.json'))
            retweet(tweetId)
            pass
        else:
            puts(colored.red('Retweet argument id (-id) is required'))
            raise InputError   
        pass
    else:
        puts(colored.red('Unknown command argument'))
        raise InputError
    pass
else:
    puts(colored.red('Must provide command arguments'))
    raise InputError





#TODO use tasks
#latestMeasurementTweet(data)
#postBuoyCam('#BuoyCam from Station 44011. \n\n Image Credit NOAA/NWS/NDBC\n@NOAA' )

puts(colored.cyan('Task Complete'))