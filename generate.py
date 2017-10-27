#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

HEADERS = {'User-Agent': 'Mozilla/5.0'}
SETTLEMENT_URL = 'http://peacenow.org.il/en/settlements-watch/israeli-settlements-at-the-west-bank-the-list'

def scrape():
    req = Request(SETTLEMENT_URL, headers=HEADERS)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'lxml')

    listing = soup.find(id='settlements-list')


    settlements = []

    for item in listing.findAll('a'):
        link = item['href']

        req = Request(link, headers=HEADERS)
        page = urlopen(req)
        soup = BeautifulSoup(page, 'lxml')

        container = soup.find('article')
        name = container.find(class_='page-title').text
        location = container.find(id='settleLocation')['location-data']

        body = container.find('section', class_='entry-content cf')
        type_ = body.find('span', class_='right natun').text

        if (type_.replace(' ', '').lower() != 'settlement'):
            continue

        list_items = container.findAll('li')

        for itemSub in list_items:
            if (itemSub.find('span').text == "Establishment"):
                year = int(itemSub.findAll('span')[2].text)


        settlement = {
            'name': name,
            'longitude': float(location.split(' ')[0]),
            'latitude': float(location.split(' ')[1]),
            'establishment': year
        }

        settlements.append(settlement)

    return settlements

all_settlements = scrape()
print (all_settlements)

df = pd.DataFrame(all_settlements)
df.to_csv('nowpeace-settlements.csv', index=False)
