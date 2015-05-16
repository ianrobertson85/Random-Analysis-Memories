import mechanize
import cookielib
from time import sleep
import time
import xml.etree.ElementTree as ET

route = '504'
url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r=' + route + '&t=0'

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

#Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

while True <> False:
#if True <> False:
    localtime = time.localtime()
    timeString  = time.strftime("%m%d%H%M%S", localtime)
    r = br.open(url)
    html = r.read()
    root = ET.fromstring(html)
    
    strOut = ''

    # Loop through all vehicles and pull out the interesting bits    
    for child in root:
        if child.tag == 'vehicle':
            strOut = strOut + timeString


            # I'm checking each key before calling it.  I'm sure there's a 
            # better way...
            if 'routeTag' in child.attrib.keys():
                strOut = strOut + '|' + child.attrib['routeTag'] 
            else:
                strOut = strOut + '|'
                
            if 'id' in child.attrib.keys():
                strOut = strOut + '|' + child.attrib['id'] 
            else:
                strOut = strOut + '|'

            if 'lat' in child.attrib.keys():
                strOut = strOut + '|' + child.attrib['lat'] 
            else:
                strOut = strOut + '|'

            if 'lon' in child.attrib.keys():
                strOut = strOut + '|' + child.attrib['lon'] 
            else:
                strOut = strOut + '|'

            if 'secsSinceReport' in child.attrib.keys():
                strOut = strOut + '|' + child.attrib['secsSinceReport'] 
            else:
                strOut = strOut + '|'
            
            if 'dirTag' in child.attrib.keys():
                strOut = strOut + '|' + child.attrib['dirTag']
            else:
                strOut = strOut + '|'

            if 'heading' in child.attrib.keys():
                strOut = strOut + '|' + child.attrib['heading'] + '\n'
            else:
                strOut = strOut + '|\n'
                
        elif child.tag == 'Error':
            strOut = strOut + timeString + '|' + 'ERROR!' + '\n'

    # Now open the file and write it out.    
    f = open('/home/ian/code/python/ttc/files/file_out.dat', 'a')
    f.write(strOut)
    f.close()
    
    sleep(30)


