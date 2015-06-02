def get_response(route='504'):
    '''
    Tries to pull the data for a specific route, retursn the HTTP code and text.
    '''
    import requests
    
    #This is the URL for the site that I'm using.
    url = 'http://webservices.nextbus.com/service/publicXMLFeed'
    url += '?command=vehicleLocations&a=ttc&r=' + route + '&t=0'

    r = requests.get(url)

    if r.status_code == 200:
        return (r.status_code, r.text)
    else:
        return (r.status_code, '')

def html_to_csv(html, time_stamp):
    '''
    Extracts the things I care about.  Send a text and it'll split out into a csv
    '''
    import xml.etree.ElementTree as ET

    #These are the keys I care about for each vehicle
    mykeys = ['routeTag','id','lat','lon','secsSinceReport','dirTag','heading']
    txt = ''

    #Just loop through each of the keys that I care about for each vehicle
    root = ET.fromstring(html)
    for vehicle in [v for v in root if v.tag == 'vehicle']:
        txt = txt + time_stamp + ',200'
        for k in mykeys:
            try:
                txt += ',' + str(vehicle.attrib[k])
            except:
                txt += ','
        txt += '\n'

    return txt

def get_data(route='504', filename='output.out'):
    '''
    Takes a route number and returns the data dump from the site, 
    and the html response code, all in a dictionary.
    '''
    import time

    localtime = time.localtime()
    timeString  = time.strftime("%y%m%d%H%M%S", localtime)

    status, html = get_response(route)
    if status == 200:
        csv = html_to_csv(html,timeString)
        to_sleep = 30
    else:
        csv = timeString + status + ',,,,,,,'
        to_sleep = 300

    # Now open the file and write it out.    
    f = open(filename, 'a')
    f.write(csv)
    f.close()

    #Send back the amount of time to sleep
    return to_sleep

if __name__ == '__main__':
    from time import sleep

    i = 0
    while False != True:
        sleep(get_data('504', 'files/output.out'))
        i += 1
        if i >= 5:
            break
