def data_pull(min_year = 1980, max_year = 2015, file_types = ['.csv'],
    sleep_secs = 4):
    '''
    Pulls some data files
    '''
    import requests
    from bs4 import BeautifulSoup
    import time
    import codecs

    baseurl = 'http://wichita.ogs.ou.edu/eq/catalog/'
    
    for i in range(min_year, max_year + 1):
        for file_type in file_types:
            print str(i) + file_type,
            url = baseurl + str(i) + '/' + str(i) + file_type
            page = requests.get(url)
            output_file = 'data/' + str(i) + file_type        
            
            if file_type in ['.dbf','.prj','.shp','.shx','.xsd']:
                page.encoding = 'ISO-8859-1'
                txt = page.text
                f = codecs.open(output_file, 'w', 'ISO-8859-1')
            else:
                txt = page.text    
                f = open(output_file, 'w')
            
            f.write(txt)
            f.close()
            
            #Sleeps a few seconds to give it time
            time.sleep(sleep_secs)

if __name__ == '__main__':
    data_pull(file_types=['.dbf','.prj','.shp','.shx','.xsd'])
