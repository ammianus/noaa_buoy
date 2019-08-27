import pandas as pd
import numpy
import sys

DEFAULT_BUOY = 44011

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
url = 'https://www.ndbc.noaa.gov/data/realtime2/{}.txt'.format(buoyId)

print('reading data from: '+url)
buoydata = pd.read_table(url,delim_whitespace=True,header=[0], skiprows=[1], na_values=['MM'])
print('done')

#tests printing the raw data from the tabler
#print(buoydata.columns)
#print(buoydata.dtypes)
print(buoydata.head(1))
#print(buoydata.describe())
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

text = 'The latest air temperature at Station {} is {}°C is {} the maximum temperature for the past 45 days of {}°C.'.format(buoyId, airTemp,maxTempRelativeDesc,maxTemp)
print(text)

