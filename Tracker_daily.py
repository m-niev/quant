from lxml import html
from pymongo import MongoClient
import pymongo.errors
import requests
import datetime, time

TIME_INTERVAL = 20
CUR_NUMBER = 20
INIT_DATE = '20141231'
d=INIT_DATE

try:
    client = MongoClient(' ', )
    db = client[' ']
    col = db['top20_daily']

    try:
        d = col.find().sort('_id', -1).limit(1)[0]['date']
        dat = datetime.datetime.strptime(d, "%Y%m%d")
        dat = dat + datetime.timedelta(days=1)
        d = dat.strftime("%Y%m%d")
        if d == time.strftime("%Y%m%d"):
            print('Data up-to-date.')
        else:
            print('Resuming from: ', d)
    except:
        print('Database is empty. Starting from:', INIT_DATE)
        d = INIT_DATE

    while True:

            while d < time.strftime("%Y%m%d"):

                try:
                    page = requests.get(' ' + d)
                    print('Downloaded from:', d)
                    tree = html.fromstring(page.content)

                    # create lists of names, symbols, market caps, prices, circulating supplies, volume (24h), %1h, 24h, 7d changes
                    nam = tree.xpath('//a[@class="currency-name-container link-secondary"]/text()')
                    sym = tree.xpath('//td[@class="text-left col-symbol"]/text()')
                    cap = tree.xpath('//td[@class="no-wrap market-cap text-right"]/text()')
                    pri = tree.xpath('//a[@class="price"]/text()')
                    cir = tree.xpath('//span[@data-supply-container]/text()')
                    vol = tree.xpath('//a[@class="volume"]/text()')
                    one = tree.xpath('//td[@data-timespan="1h"]/text()')
                    twe = tree.xpath('//td[@data-timespan="24h"]/text()')
                    sev = tree.xpath('//td[@data-timespan="7d"]/text()')

                    for i in range(CUR_NUMBER):
                        dict = {'date' : d, 'name' : nam[i], 'symbol' : sym[i], 'price' : pri[i] , 'market_cap' : cap[i],
                                'circulating_supply' : cir[i], 'volume_24h' : vol[i], 'delta_perc_1h' : one[i],
                                'delta_perc_24h' : twe[i], 'delta_perc_7d' : sev[i]}
                        col.insert_one(dict)

                    dat = datetime.datetime.strptime(d, "%Y%m%d")
                    dat = dat + datetime.timedelta(days=1)
                    d = dat.strftime("%Y%m%d")

                except requests.exceptions.RequestException as e:
                    print(e)
                except:
                    print('Something went wrong. Trying again with: ', d)

                time.sleep(TIME_INTERVAL)

except pymongo.errors.ConnectionFailure as e:
    print(e)