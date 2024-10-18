import requests
import csv

with open('output/countries.txt', 'r') as file:
    countries = [line.split(',') for line in file.read().splitlines()]

for country in countries:
    country_code = country[0].strip()
    country_url = country[2].strip()

    apps = []
    r = requests.post(
        url=f'https://{country_url}/api/tvapp/retrieveMoreAppList.ajax',
        params={
            'moreYn': 'Y',
            'orderType': '4',  # by name
            'prodCode': 'P000000030',
            'plfmCode': 'W23P',
            'curPage': '1',
            'rowCount': '5000'
        }
    )
    data = r.json()
    apps += [
        [app['appId'], app['appName'], app['avgSscr'], app['sellrUsrName'], app['catName'], app['preFlag']]
        for app in data.get('appList', {})
    ]

    # write it to a file
    with open(f'output/apps/{country_code}.csv', 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(['ID', 'Name', 'Average Score', 'Vendor', 'Category', 'Pre-Installed'])
        csv_writer.writerows(apps)
