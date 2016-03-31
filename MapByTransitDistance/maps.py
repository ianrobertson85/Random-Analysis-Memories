"""
This is some code to pull data out of google maps directions API.  I'm going
to use it to colour a map all nifty colours!

Author: Ian Robertson
"""

import requests
import time
import numpy as np
import matplotlib.path as mplPath
import config
import random
import json
import logging
from logging import debug, info
import sys
import glob


def get_one_point(origLat, origLon, destLat, destLon, arrivalTime, apiKey):
    """Grabs the data for a specified setup and returns the json output"""
    
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    payload = {
        'origin': '{0},{1}'.format(origLat, origLon),
        'destination': '{0},{1}'.format(destLat, destLon),
        'key': apiKey,
        'arrival_time': arrivalTime, 
        'mode': 'transit',
        'alternatives': 'true'
    }

    r = requests.get(url, params=payload)
    return r.json()


def get_toronto():
    """Grabs a matplotlib path which outlines Toronto (defined elsewhere)"""
    with open('toronto.json') as f:
        t = eval(f.read())
    #Converts to an array
    n = np.array([[i['lat'], i['lon']] for i in t])
    return mplPath.Path(n)


def point_in_toronto(toronto, lat, lon):
    """Checks a point and returns a boolean true if it is in Toronto, false
    otherwise
    """
    return bool(toronto.contains_point((lat, lon)))

def pull_data(totalCount, sleepTime=1):
    """Pulls totalCount random records"""
    minLat = 43.579536
    maxLat = 43.856951
    minLon = -79.641739
    maxLon = -79.113709
    #destination = '43.670235,-79.386757' #Bloor & Yonge
    #destination = '43.645753,-79.380532' #Union Station
    #destination = '43.706758,-79.398301' #Yonge & Eglinton
    destLat = 43.648692
    destLon = -79.380253 #King & Bay (Financial District)
    arrivalTime = '1459774800' #Apr 4 9 am
    apiKey = config.apiKey

    toronto = get_toronto()
    counter = 0

    while counter < totalCount:
        #Loop through and pull a bunch of random points!
        randLat = round(random.uniform(minLat, maxLat), 6)
        randLon = round(random.uniform(minLon, maxLon), 6)

        debug('counter: {0}, randLat: {1}, randLon: {2}'.format(counter,
                                                                randLat, 
                                                                randLon)
        )

        if point_in_toronto(toronto, randLat, randLon):
            counter += 1
            output = get_one_point(randLat, randLon, destLat, destLon, 
                arrivalTime, apiKey)
            filename = 'data/out_{0}_{1}'.format(randLat, randLon)
            with open(filename, 'w') as f:
                json.dump(output, f)

            #Sleep to let the API settle down.
            time.sleep(sleepTime)

def get_time(filename):
    """For a given file, pulls out the fastest time."""
    with open(filename) as f:
        j = json.load(f)
        debug('Opened {0}'.format(filename))
    
    #What's the quickest route in the list?  Return that one (sum of all legs)
    routeTimes = []
    for route in j['routes']:
        routeTime = 0
        for leg in route['legs']:
            routeTime += leg['duration']['value']
        routeTimes.append(routeTime)

    debug('Times: {0}'.format(routeTimes))
    if routeTimes == []:
        return None
    else:
        return min(routeTimes)

def get_lat_lon(filename):
    """Gets a lat/lon pair based on the filename."""
    return (filename.split('_')[-2],
            filename.split('_')[-1])

def process_files():
    """Pulls everything into an output file"""
    records = []
    for filename in glob.glob('data/out*'):
        routeTime = get_time(filename)
        info(routeTime)
        lat, lon = get_lat_lon(filename)
        debug('Lat {0}, Lon {1}'.format(lat, lon))
        if routeTime:
            records.append({
                'lat': lat, 'lon': lon, 'rt': routeTime
                }
            )
    with open('points.json', 'w') as f:
        json.dump(records, f)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    pull_data(900)