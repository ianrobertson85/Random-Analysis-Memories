'''
Manipulates some files to pull out the winning numbers.
'''

from bs4 import BeautifulSoup
import os

def handle_file(filename):
    txt = open(filename).read()

    soup = BeautifulSoup(txt)
    dicto = {}

    dl = soup.dl
    for tr in soup.dl.find_all('tr')[1::]:
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
        sales = soup.find('em', text='Total Sales').parent.nextSibling.nextSibling.nextSibling.text
        sales = int(float(sales.replace(',', '').replace('$', '')) / 5)
    except:
        #There's a couple times where the total sales is missing.  Use odds of hitting 3 numbers there.
        sales = dicto['3_winners'] * 8.1
    dicto['sales'] = sales

    return dicto

if __name__ == '__main__':
    overall_dict = {}

    for filename in ['files/' + f for f in os.listdir('files')]:
        d = filename[6:16]
        print d,
        overall_dict[d] = handle_file(filename)
        print 'done'
    with open('fileout.out', 'w') as f:
        f.write(str(overall_dict))

