import requests
import re

r = requests.post(url='https://gb.lgappstv.com/api/common/retrieveNation.ajax')
data = r.json()
countries_info = [(country['cntryCode'], country['javaLocaleName']) for country in data['cntryList']]
countries_info = sorted(dict(sorted(countries_info, key=lambda x: x[1], reverse=True)).items())

countries = []
for country in countries_info:
    r = requests.post(
        url='https://gb.lgappstv.com/api/common/retrieveNationUrl.ajax',
        params={
            'cntryCode': country[0],
            'locale': country[1],
        }
    )
    data = r.json()
    if data.get('mainUrl'):
        countries.append((country[0], country[1], re.split(r'/+', data['mainUrl'])[1]))

with open('output/countries.txt', 'w') as file:
    file.write('\n'.join([f'{country[0]}, {country[1]}, {country[2]}' for country in countries]))
