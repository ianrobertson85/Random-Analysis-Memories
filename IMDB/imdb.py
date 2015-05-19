# -*- coding: utf-8 -*-

#can i convert this to just load to a dataframe and save it as a dataframe blob? 


from bs4 import BeautifulSoup
import requests
import xlwt
import time

filename = 'output.xls'

baseurl = 'http://www.imdb.com/search/title?num_votes=1000,&sort=user_rating,'
baseurl += 'desc&title_type=feature&year=1950,2014'

book = xlwt.Workbook()
sheet = book.add_sheet("Data")

sheet.write(0,0,'Title')
sheet.write(0,1,'Title Link')
sheet.write(0,2,'Picture')
sheet.write(0,3,'Rank')
sheet.write(0,4,'Year')
sheet.write(0,5,'Outline')
sheet.write(0,6,'Genre')
sheet.write(0,7,'Credit')
sheet.write(0,8,'Links')
sheet.write(0,9,'Rating')
sheet.write(0,10,'Certificate')

xlrow = 0

iternum = 347

for i in range(0,iternum + 1):
    
    url = baseurl + '&start=' + str((i * 50) + 1)
    page = requests.get(url)
    txt = page.text
    
    soup = BeautifulSoup(txt)
    
    res = soup.find('table')    
    tr = res.find_all('tr')
    for j in range(1,len(tr)):
        # Initialize all of the variables
        title = ''
        titlelink = ''
        pic = ''
        rank = ''
        year = ''
        outline = ''
        genre = ''
        credit = ''
        links = ''
        rating = ''
        cert = ''
        
        #Iterate the Excel row        
        xlrow += 1
        
        # Now pull the variables from the website
        title = tr[j].a['title']
        titlelink = tr[j].a['href']
        pic = tr[j].a.img['src']
        rank = tr[j].td.text
        for span in tr[j].find_all('span'):
            if span.has_attr('class'):
                if span['class'][0] == 'year_type':
                    year = span.text
                if span['class'][0] == 'outline':
                    outline = span.text
                if span['class'][0] == 'genre':
                    genre = span.text
                if span['class'][0] == 'certificate':
                    for sp in span.find_all('span'):
                        cert = sp['title']
                if span['class'][0] == 'credit':
                    credit = span.text
                    links = ''                
                    for a in span.find_all('a'):
                        links += '|' + a['href']
        for div in tr[j].find_all('div'):
            for div1 in div.find_all('div'):
                if div1.has_attr('class'):
                    if div1['class'][0] == 'rating':
                        rating = div1['title']
        sheet.write(xlrow,0,title)
        sheet.write(xlrow,1,titlelink)
        sheet.write(xlrow,2,pic)
        sheet.write(xlrow,3,rank)
        sheet.write(xlrow,4,year)
        sheet.write(xlrow,5,outline)
        sheet.write(xlrow,6,genre)
        sheet.write(xlrow,7,credit)
        sheet.write(xlrow,8,links)
        sheet.write(xlrow,9,rating)
        sheet.write(xlrow,10,cert)
    
    
    # Save the Excel
    book.save(filename)
    
    #Sleeps a few seconds so the internet doesnt hate me    
    time.sleep(10)