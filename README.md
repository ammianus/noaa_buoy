# noaa_buoy

noaa_buoy a very simple hobby example of using Python to automate taking data from public, open data set (NOAA National Buoy Data Center real time data) and use it to interact with social media accounts on Twitter.

Written in Python using some OS libraries:
- pandas
- TwitterAPI

This project is in a very early stage and likely to see many changes.

## Install

Requires Python 3 and pip installed.

1. Clone repository
2. `pip install pandas`
3. `pip install TwitterAPI`

## Running

1. To run buoy_data.py it takes as a parameter the station id for the NDBC buoy. In my case I'm doing this for Station 44011 George's Bank buoy.: 
    `python buoy_data.py 44011`

This will not tweet anything just print data.

2. To run for social media posting on Twitter if you register your own Twitter app at developer.twitter.com
    1. Edit `twitter_creds.py` and put in your Twitter App
    2. Run the `twitter_client.py`:
    `python twitter_client.py`
