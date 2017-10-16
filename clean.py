import csv
import json
import pandas as pd

f = open('nowpeace-settlements.csv')

new = []

for i in csv.DictReader(f):
    location = i['location'].replace('\'', '"')
    location_json = json.loads(location)

    x = {
        'name': i['name'],
        'longitude': location_json['longitude'],
        'latitude': location_json['latitude']
    }

    new.append(x)

df = pd.DataFrame(new)
df.to_csv('nowpeace-settlements-new.csv', index=False, columns=['name', 'longitude', 'latitude'])
