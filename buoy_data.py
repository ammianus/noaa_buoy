import pandas as pd
import numpy
import sys
import requests
import shutil
import hashlib
import os
import platform

DEFAULT_BUOY = 44011

def convertCToF(celsius: float) -> float:
    farenheit = round(((celsius * 1.8) + 32.0),1)
    return farenheit

def convertMetricSpeedToImperial(metersPerSecond: float) -> float:
    milesPerHour = round((metersPerSecond * 3600) * 0.000621371)
    return milesPerHour 

def friendlyFormatTemp(celsiusTemp: float) -> str:
    farenheit = convertCToF(celsiusTemp)
    return '{}°F ({}°C)'.format(farenheit, celsiusTemp)

def friendlyFormatSpeed(metersPerSecond: float) -> str:
    mph = convertMetricSpeedToImperial(metersPerSecond)
    return '{} mph ({} m/s)'.format(mph, metersPerSecond)

#calculate the current air temp at the station and it's relation to the max temp
def airTempStatus(buoydata: pd.DataFrame) -> str:
    airTemp = buoydata.at[0,'ATMP']
    date = '{}-{}-{} {}:{} UTC'.format(buoydata.at[0,'#YY'],buoydata.at[0,'MM'],buoydata.at[0,'DD'],buoydata.at[0,'hh'],buoydata.at[0,'mm'])
    print('{} Air Temp {}'.format(date,airTemp))
    calcs = buoydata.agg({'ATMP' : ['median','min','max']})#, 'WTMP' : ['median','min', 'max'], 'WSPD' : ['median','min', 'max']})
    print(calcs)
    maxTemp = calcs.at['max','ATMP']

    maxTempRelativeDesc = ''    
    if airTemp == maxTemp:
        maxTempRelativeDesc = 'equal to'
        pass
    elif airTemp < maxTemp:
        maxTempRelativeDesc = 'lower than'
        pass

    text = 'The latest air temperature at Station {} is {}°C and is {} the maximum temperature for the past 45 days of {}°C.'.format(buoyId, airTemp,maxTempRelativeDesc,maxTemp)
    print(text)
    return text

def waterTempStatus(buoydata: pd.DataFrame) -> str:
    waterTemp = buoydata.at[0,'WTMP']
    date = '{}-{}-{} {}:{} UTC'.format(buoydata.at[0,'#YY'],buoydata.at[0,'MM'],buoydata.at[0,'DD'],buoydata.at[0,'hh'],buoydata.at[0,'mm'])
    print('{} Water Temp {}'.format(date,waterTemp))
    calcs = buoydata.agg({'WTMP' : ['median','min','max']})#, 'WTMP' : ['median','min', 'max'], 'WSPD' : ['median','min', 'max']})
    print(calcs)
    maxTemp = calcs.at['max','WTMP']

    maxTempRelativeDesc = ''    
    if waterTemp == maxTemp:
        maxTempRelativeDesc = 'equal to'
        pass
    elif waterTemp < maxTemp:
        maxTempRelativeDesc = 'lower than'
        pass

    text = 'The latest water temperature at Station {} is {}°C and is {} the maximum temperature for the past 45 days of {}°C.'.format(buoyId, waterTemp,maxTempRelativeDesc,maxTemp)
    print(text)
    return text

def windSpeedStatus(buoydata: pd.DataFrame) -> str:
    windSpeed = buoydata.at[0,'WSPD']
    date = '{}-{}-{} {}:{} UTC'.format(buoydata.at[0,'#YY'],buoydata.at[0,'MM'],buoydata.at[0,'DD'],buoydata.at[0,'hh'],buoydata.at[0,'mm'])
    print('{} Water Temp {}'.format(date,windSpeed))
    calcs = buoydata.agg({'WSPD' : ['median','min','max']})#, 'WTMP' : ['median','min', 'max'], 'WSPD' : ['median','min', 'max']})
    print(calcs)
    maxSpeed = calcs.at['max','WSPD']

    maxTempRelativeDesc = ''    
    if windSpeed == maxSpeed:
        maxTempRelativeDesc = 'equal to'
        pass
    elif windSpeed < maxSpeed:
        maxTempRelativeDesc = 'lower than'
        pass

    text = 'The latest wind speed at Station {} is {} m/s and is {} the maximum speed for the past 45 days of {} m/s.'.format(buoyId, windSpeed, maxTempRelativeDesc, maxSpeed)
    print(text)
    return text

def measurementStatus(buoydata: pd.DataFrame) -> str:
    date = '{}-{}-{} {}:{} UTC'.format(buoydata.at[0,'#YY'],buoydata.at[0,'MM'],buoydata.at[0,'DD'],buoydata.at[0,'hh'],buoydata.at[0,'mm'])
    text = 'Latest buoy measurements at Georges Bank:\n({})\nWDIR: {} \nWSPD: {} \nGST: {} \nWVHT: {} m\nPRES: {} hPa\nATMP: {}\nWTMP: {}'.format(date,buoydata.at[0,'WDIR'],friendlyFormatSpeed(buoydata.at[0,'WSPD']),friendlyFormatSpeed(buoydata.at[0,'GST']),buoydata.at[0,'WVHT'],buoydata.at[0,'PRES'],friendlyFormatTemp(buoydata.at[0,'ATMP']),friendlyFormatTemp(buoydata.at[0,'WTMP']))
    print(text)
    return text

def fetchRealTime2Data(theBuoyId: int) -> pd.DataFrame:
    #realtime data for station 44011
    url = 'https://www.ndbc.noaa.gov/data/realtime2/{}.txt'.format(theBuoyId)

    print('reading data from: '+url)
    buoydata = pd.read_table(url,delim_whitespace=True,header=[0], skiprows=[1], na_values=['MM'])
    print('done')

    #tests printing the raw data from the tabler
    #print(buoydata.columns)
    #print(buoydata.dtypes)
    print(buoydata.head(1))
    #print(buoydata.describe())
    return buoydata

def hashFile(path: str) -> str:
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def fetchBuoyCamImage(theBuoyId: int) -> str:
    #backup current file if exists
    
    latestFilePath = 'buoycam/latest.jpg'
    tempFilePath = 'buoycam/temp_latest.jpg'
    latestFileExists = os.path.exists(latestFilePath)
    previousHash = '' 
    if latestFileExists == True:
        print('image exists')
        date = os.path.getmtime(latestFilePath)
        print('mtime: '+str(date))
        prevFilePath = 'buoycam/previous-{}.jpg'.format(date)
        previousHash = hashFile(latestFilePath)
        pass
    else:
        previousHash = '-1'
        pass
    
    print('prev hash: '+previousHash)

    #download latest file from noaa servers
    image_url = 'https://www.ndbc.noaa.gov/buoycam.php?station={}'.format(theBuoyId)
    img_data = requests.get(image_url).content
    with open(tempFilePath, 'wb') as handler:
        handler.write(img_data)

    newHash = hashFile(tempFilePath)
    print('new hash: '+newHash)

    if previousHash != newHash:
        print('new image found copying to '+latestFilePath)
        if latestFileExists == True:
            shutil.move(latestFilePath,prevFilePath)
            pass
        shutil.move(tempFilePath,latestFilePath)
        return latestFilePath
    else:
        print('image unchanged')
        return 'n/a'

def buoyLat() -> float:
    return 41.070000

def buoyLong() -> float:
    return -66.588000

#print('This is the name of the script: ', sys.argv[0])
print('Number of arguments: ', len(sys.argv))
print('The arguments are: ' , str(sys.argv))
buoyId = -1
if len(sys.argv)==2:
    buoyId = sys.argv[1]
    pass
else:
    buoyId = DEFAULT_BUOY
    pass

#realtime data for station 44011
buoydata = fetchRealTime2Data(buoyId)
#print(buoydata.describe())

#testing
#airTempStatus(buoydata)
#waterTempStatus(buoydata)
#windSpeedStatus(buoydata)
#measurementStatus(buoydata)

imagefile = fetchBuoyCamImage(buoyId)
print(imagefile)
