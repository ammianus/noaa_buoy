import pandas as pd
import numpy

#realtime data for station 44011
url = 'https://www.ndbc.noaa.gov/data/realtime2/44011.txt'

print('reading data from: '+url)
buoydata = pd.read_table(url,delim_whitespace=True,header=[0], skiprows=[1])
print('done')

#tests printing the raw data from the tabler
print(buoydata.columns)
print(buoydata.dtypes)
print(buoydata.head(1))
print(buoydata.describe())
airTemp = buoydata.at[0,'ATMP']
print('Current Air Temp', airTemp)

