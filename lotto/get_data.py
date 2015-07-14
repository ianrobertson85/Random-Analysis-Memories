import requests
import datetime
import time

first_date = datetime.date(2009, 12, 18)
last_date = datetime.date.today()
delay = 20

ranger = (last_date - first_date).days / 7

date_range = [first_date + datetime.timedelta(days = x * 7) for x in range(ranger)]

base_url = 'http://www.lotterycanada.com/lotto-max/'

for d in date_range:
    url = base_url + d.isoformat()
    r = requests.get(url)
    filename = 'files/' + d.isoformat() + '.html'

    if r.ok:
        print d.isoformat(), 'OK!'
        t = r.text.encode('utf8')
        with open(filename, 'w') as f:
            f.write(t)
    else:
        print d.isoformat(), 'Woah what happened!?'

    time.sleep(delay)
