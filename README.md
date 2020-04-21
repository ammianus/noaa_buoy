# noaa_buoy

noaa_buoy a very simple hobby example of using Python to automate taking data from public, open data set (NOAA National Buoy Data Center real time data) and use it to interact with social media accounts on Twitter.

Written in Python using some OS libraries:
- pandas
- TwitterAPI
- matplotlib
- clint

This project is in a very early stage and likely to see many changes.

## Releases
0.1 (2020-04-20) - Basic functioning CLI for reading data and sending tweets
- Posting buoycam, messages, latest measurements, retweets
- Windspeed with plot of last 7 days
- has been 'live' for a while, still semi-automated, need a user to take actions

## Install

Requires Python 3 and pip installed.

1. Clone repository
2. `pip install pandas`
3. `pip install TwitterAPI`
4. `pip install clint`
5. `pip install matplotlib`

## Running

1. To run buoy_data.py it takes as a parameter the station id for the NDBC buoy. In my case I'm doing this for Station 44011 George's Bank buoy.: 
    `python buoy_data.py 44011`

This will not tweet anything just print data.

2. To run for social media posting on Twitter if you register your own Twitter app at developer.twitter.com
    1. Edit `twitter_creds.py` and put in your Twitter App
    2. Run the `twitter_client.py`:
    Post a message
    `python twitter_client.py post tweet -m "Hello World"`
    Post the latest buoy data measurements
    `python twitter_client.py post latest`
    Post the most recent buoycam image
    `python twitter_client.py post buoycam`

