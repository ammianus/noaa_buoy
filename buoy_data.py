import pandas as pd
import numpy as np
#import scipy as sp
import sys
import requests
import shutil
import hashlib
import os
import platform
import matplotlib
import matplotlib.pyplot as plt
#from datetime import timedelta

DEFAULT_BUOY = 44011

def convertCToF(celsius: float) -> float:
    if pd.isna(celsius):
        farenheit = -1
        pass
    else:
        farenheit = round(((celsius * 1.8) + 32.0),1)
        pass
    
    return farenheit

def convertMetricSpeedToImperial(metersPerSecond: float) -> float:
    if pd.isna(metersPerSecond):
        milesPerHour = -1
        pass
    else:
        milesPerHour = round((metersPerSecond * 3600) * 0.000621371)
        pass
    
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
    date = '{} UTC'.format(buoydata.at[0,'temp_timestamp'])
    print('{} Wind Speed {}'.format(date,windSpeed))
    calcs = buoydata.agg({'WSPD' : ['median','min','max']})#, 'WTMP' : ['median','min', 'max'], 'WSPD' : ['median','min', 'max']})
    print(calcs)
    maxSpeed = calcs.at['max','WSPD']

    maxSpeedRelativeDescription = ''    
    if windSpeed == maxSpeed:
        maxSpeedRelativeDescription = 'equal to'
        pass
    elif windSpeed < maxSpeed:
        maxSpeedRelativeDescription = 'lower than'
        pass

    #get wind data frame for last 7 days only
    print(buoydata.last_valid_index())
    #end = buoydata.at[buoydata.last_valid_index(),'temp_timestamp']
    #delta = timedelta(days=7)
    #start = end + delta
    start = 0
    end = 1008
    windDF1 = buoydata.iloc[ start : end]
    windDF = windDF1[['temp_timestamp','WSPD']]
    windDF.columns = ['date','WSPD']
    windDF = windDF.sort_values('date', ascending=True)
    windDF = windDF.dropna(how='any')
    print(windDF.describe)
    
    windSpeedPlot(windDF[::-1])

    #each measurement is about every 10 minutes, 7 days means 7 x 24 x 6 = 720
    # print('make timeseries')
    # lookback = 1008
    # dates = windDF['date']
    # speeds = list(windDF['WSPD'].values)
    # counter_ = -1
    # speed_series = []
    # for tenminute in dates:
    #     counter_ += 1
    #     # if counter_ % 1000 == 0: print(counter_)
    #     if counter_ >= lookback:
    #         print('counter {}, tenminute {}'.format(counter_,tenminute))
    #         speed_series.append(speeds[counter_-lookback:counter_])
    #         #reset counter
    #         counter_=-1
                    
    # timeseries_df = pd.DataFrame(speed_series)    
    
    # print(timeseries_df.dtypes)




    # counter = 5
    # complexity = 7
    # for idx,row in timeseries_df[::-1].iterrows():
    #     counter -= 1
    #     # look for desired shape
    #     #plt.plot([np.mean(r) for r in split_seq(list(row.values), complexity)])
    #     #plt.grid()
    #     #plt.show()
    #     if counter < 0:
    #         break

    

    # let's single out the shape we want
    #correlate_against = [0,0,1,1,2,2,3] 
    #correlate_against = [3,2,1,1,1,1,0] 
    #xplt.plot(correlate_against)
    #plt.grid()
    #plt.show()


#correlate function
    #complexity = 7
   # outcome_list = []
    #for index, row in timeseries_df.iterrows():
    #    simplified_values = []
    #    for r in split_seq(list(row.values), complexity):
    #        simplified_values.append(np.mean(r))
    #    correz = pearson(simplified_values,correlate_against)
    #    if correz > 0.5:
    #        outcome_list.append(1)
    #    else:
    #        outcome_list.append(0)

    #timeseries_df['outcome'] = outcome_list
    #print(np.mean(outcome_list))
    #print(timeseries_df.tail(30)['outcome'])

    text = 'The latest wind speed at Station {} on {} is {} and is {} the maximum speed for the past 45 days of {}.'.format(buoyId, date, friendlyFormatSpeed(windSpeed), maxSpeedRelativeDescription, friendlyFormatSpeed(maxSpeed))
    print(text)
    return text

def windSpeedPlot(windDF: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(16, 8))
    #x_new = np.linspace(0, 45, 180)
    #a_BSpline = sp.interpolate.make_interp_spline(windDF['date'], windDF['WSPD'])
    #y_new = a_BSpline(x_new)
    #plt.plot(x_new, y_new, label='WSPD (m/s)', color='blue')
    plt.plot(windDF['date'], windDF['WSPD'], label='WSPD (m/s)', color='blue')
    plt.title('WindSpeed ' + str(np.min(windDF['date'])) + ' - ' + str(np.max(windDF['date'])))
    plt.legend(loc='upper left')
    plt.grid()
    #if dir 
    if os.path.exists('plots')!=True:
        os.mkdir('plots')
        pass
    fig.savefig('plots/windspeed.png')

def measurementStatus(buoydata: pd.DataFrame) -> str:
    #date = '{}-{}-{} {}:{} UTC'.format(buoydata.at[0,'#YY'],buoydata.at[0,'MM'],buoydata.at[0,'DD'],buoydata.at[0,'hh'],buoydata.at[0,'mm'])
    date = '{} UTC'.format(buoydata.at[0,'temp_timestamp'])
    text = 'Latest buoy measurements at Georges Bank:\n({})\nWDIR: {} \nWSPD: {} \nGST: {} \nWVHT: {} m\nPRES: {} hPa\nATMP: {}\nWTMP: {}'.format(date,buoydata.at[0,'WDIR'],friendlyFormatSpeed(buoydata.at[0,'WSPD']),friendlyFormatSpeed(buoydata.at[0,'GST']),buoydata.at[0,'WVHT'],buoydata.at[0,'PRES'],friendlyFormatTemp(buoydata.at[0,'ATMP']),friendlyFormatTemp(buoydata.at[0,'WTMP']))
    print(text)
    return text

def fetchRealTime2Data(theBuoyId: int) -> pd.DataFrame:
    #realtime data for station 44011
    url = 'https://www.ndbc.noaa.gov/data/realtime2/{}.txt'.format(theBuoyId)

    print('reading data from: '+url)
    buoydata = pd.read_table(url,delim_whitespace=True,header=[0], skiprows=[1], na_values=['MM'])
    #enrich data with date
    #buoydata.assign(temp_timestamp=lambda x: pd.to_datetime('{}-{}-{} {}:{}'.format(x['#YY'],x['MM'],x['DD'],x['hh'],x['mm']),format='%Y-%m-%d %H:%M', exact=True, utc=None, infer_datetime_format=False, yearfirst=True))
    buoydata = buoydata.assign(temp_timestamp=lambda x: pd.to_datetime(dict(year=x['#YY'], month=x['MM'], day=x['DD'], hour=x['hh'], minute=x['mm'])))
    buoydata = buoydata.sort_values('temp_timestamp', ascending=False)
    print('done')

    #tests printing the raw data from the tabler
    #print(buoydata.columns)
    #print(buoydata.dtypes)
    print(buoydata.head(1))
    #print(buoydata.describe())
    return buoydata

#https://www.viralml.com/video-content.html?fm=yt&v=zBVQvVCZPCM
def split_seq(seq, num_pieces):
    # https://stackoverflow.com/questions/54915803/automatically-split-data-in-list-and-order-list-elements-and-send-to-function
    start = 0
    for i in range(num_pieces):
        stop = start + len(seq[i::num_pieces])
        yield seq[start:stop]
        start = stop
        
def pearson(s1, s2):
    """take two pd.Series objects and return a pearson corrleation"""
    s1_c=s1-np.mean(s1)
    s2_c=s2-np.mean(s2)
    return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

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
        print('old image exists in buoycam/ dir')
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

#
#print('This is the name of the script: ', sys.argv[0])
#
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
#buoydata = fetchRealTime2Data(buoyId)
#print(buoydata.describe())

#testing
#airTempStatus(buoydata)
#waterTempStatus(buoydata)
#windSpeedStatus(buoydata)
#measurementStatus(buoydata)

#imagefile = fetchBuoyCamImage(buoyId)
#print(imagefile)
def detectBrokenSensor(buoydata: pd.DataFrame) -> str:
    result = pd.Series(list(zip(buoydata['ATMP'], buoydata['ATMP'][1:])))
    #.value_counts()
    
    print(result)
    return 'detected'

#detectBrokenSensor(buoydata)
print('done')