# -*- coding: utf-8 -*-

def pull_data(num_votes, total_pages=368, sleep_secs=5, output='outlist.out'):
    '''
    Pulls data from the site and converts to a dataframe
    '''
    import requests
    from bs4 import BeautifulSoup
    import time

    baseurl = 'http://www.imdb.com/search/title?num_votes='
    baseurl += str(num_votes) + ',0'
    baseurl += '&sort=user_rating,desc'
    baseurl += '&title_type=feature'
    baseurl += '&year=1950,2015'
    
    #Initialize a list.  I'm going to pass back a list of dictionaries.
    ls = []

    for i in range(0,total_pages + 1):
    
        url = baseurl + '&start=' + str((i * 50) + 1)
        page = requests.get(url)
        txt = page.text
        
        #I changed this to use html.parser due to an issue with the default parse.
        soup = BeautifulSoup(txt, 'html.parser')
    
        res = soup.find('table')
        for tr in res.find_all('tr')[1:]:
            ls.append(dic_soup(tr))
        
        f = open(output, 'w')
        f.write(str(ls))
        f.close()
        
        #Sleeps a few seconds to give it time
        time.sleep(sleep_secs)
    
    return ls
        
def dic_soup(tr):
    '''
    Converts a tr into a dictionary
    '''
    # Initialize a dictionary 
    md = {}
    
    # Now pull the variables from the website
    md['title'] = tr.a['title']
    md['titlelink'] = tr.a['href']
    md['pic'] = tr.a.img['src']
    md['rank'] = tr.td.text
    for span in tr.find_all('span'):
        if span.has_attr('class'):
            if span['class'][0] == 'year_type':
                md['year'] = span.text
            if span['class'][0] == 'outline':
                md['outline'] = span.text
            if span['class'][0] == 'genre':
                md['genre'] = span.text
            if span['class'][0] == 'certificate':
                for sp in span.find_all('span'):
                    md['cert'] = sp['title']
            if span['class'][0] == 'credit':
                md['credit'] = span.text
                md['links'] = ''
                for a in span.find_all('a'):
                    md['links'] += '|' + a['href']
    for div in tr.find_all('div'):
        for div1 in div.find_all('div'):
            if div1.has_attr('class'):
                if div1['class'][0] == 'rating':
                    md['rating'] = div1['title']
        
    
    
    # return the dictionary
    return md

if __name__ == '__main__':
    ls = pull_data(num_votes=1000, total_pages=368, sleep_secs=6, output='outlist.out')
    

