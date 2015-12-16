'''
Manipulates some files to pull out the winning numbers.
'''

from bs4 import BeautifulSoup
import os
import glob
import re

def handle_file(filename):
    txt = open(filename).read()

    soup = BeautifulSoup(txt)
    dicto = {}

    #Change to finding the 6 + bonus because I think it's unique.
    for tr in soup(text = '6 + bonus')[0].parent.parent.parent.find_all('tr'):
        match = tr.find_all('td')[0].text
        if match == '3 + bonus':
            match = '3_bonus'
        elif match == '6 + bonus':
            match = '6_bonus'
        val = int(tr.find_all('td')[1].text.replace(',', ''))
        dicto[match + '_winners'] = val

        if match <> '3':
            prize = int(float(tr.find_all('td')[2].text.replace(',', '').replace('$', '')))
            dicto[match + '_prize'] = prize

    try:
        tab = soup.findAll('table', {'class': 'max-millions'})[0]
        dicto['millions'] = len(tab.find_all('tr')) - 1
    except:
        dicto['millions'] = 0

    dicto['jackpot'] = dicto['7_prize'] + dicto['millions'] * 1000000

    try:
        sales = soup.find('td', text=re.compile('Total Sales')).findNext('td').text.strip()
        sales = int(float(sales.replace(',', '').replace('$', '')) / 5)
        print 'found total sales'
    except:
        #There's a couple times where the total sales is missing.  Use odds of hitting 3 numbers there.
        sales = dicto['3_winners'] * 8.1
        print 'no find total sales'
    dicto['sales'] = sales

    return dicto

if __name__ == '__main__':
    overall_dict = {}

    for filename in glob.glob('files/*html'):
        d = filename[6:16]
        print d,
        overall_dict[d] = handle_file(filename)
        print 'done'
    with open('fileout.out', 'w') as f:
        f.write(str(overall_dict))

