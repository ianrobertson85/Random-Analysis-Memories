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
        val = int(tr.find_all('td')[1].text.replace(',', ''))
        dicto[match] = val

    return dicto

if __name__ == '__main__':
    overall_dict = {}

    for filename in ['files/' + f for f in os.listdir('files')]:
        d = filename[6:16]
        overall_dict[d] = handle_file(filename)
        print d
    with open('fileout.out', 'w') as f:
        f.write(str(overall_dict))

