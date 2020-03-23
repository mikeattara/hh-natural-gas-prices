from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv


def fetch_page(url):
    base_url = 'https://www.eia.gov/dnav/ng/hist/'
    response = requests.get(base_url + url)
    return BeautifulSoup(response.content, 'html.parser')


data_folder = Path('./../data/')

soup = fetch_page('rngwhhdm.htm')

links = [(a.get_text().lower(), a['href'])
         for a in soup.find_all(class_='NavChunk')]


def get_daily_data(link):
    daily_page = fetch_page(link)
    dates = daily_page.find_all(class_='B6')
    data_rows = [td.find_parent('tr') for td in dates]

    with open('daily.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Price'])
        for data_row in data_rows:
            row = [td.get_text() for td in data_row.find_all('td')]
            week, *values = row
            week = week.strip()
            values = [x if x != '' else '0.00' for x in values]
            year = week[:4]
            start_month = week[5:8]
            start_date = int(week[9:11])
            end_month = week[-6:-3]
            end_date = int(week[-2:])
            if start_month == end_month:
                for i, date in enumerate(range(start_date, end_date + 1)):
                    data_date = f'{year} {start_month} {date}'
                    writer.writerow([data_date, values[i]])
            else:
                range_end = (4 - end_date) + start_date + 1
                for i, date in enumerate(range(start_date, range_end)):
                    data_date = f'{year} {start_month} {date}'
                    writer.writerow([data_date, values[i]])
                date = 1
                while date <= end_date:
                    index = date - (end_date + 1)
                    data_date = f'{year} {end_month} {date}'
                    writer.writerow([data_date, values[index]])
                    date = date + 1


get_daily_data(links[0][1])


# pages = [fetch_page(link[1]) for link in links]
# daily_page = fetch_page(links[0][1])
# dates = daily_page.find_all(class_='B6')
# data_rows = [td.find_parent('tr') for td in dates]

# with open(data_folder/'daily.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['Date', 'Price'])
#     for data_row in data_rows:
#         row = [td.get_text() for td in data_row.find_all('td')]
#         week, *values = row
#         week = week.strip()
#         values = [x if x != '' else '0.00' for x in values]
#         year = week[:4]
#         start_month = week[5:8]
#         start_date = int(week[9:11])
#         end_month = week[-6:-3]
#         end_date = int(week[-2:])
#         if start_month == end_month:
#             for i, date in enumerate(range(start_date, end_date + 1)):
#                 data_date = f'{year} {start_month} {date}'
#                 writer.writerow([data_date, values[i]])
#         else:
#             range_end = (4 - end_date) + start_date + 1
#             for i, date in enumerate(range(start_date, range_end)):
#                 data_date = f'{year} {start_month} {date}'
#                 writer.writerow([data_date, values[i]])
#             date = 1
#             while date <= end_date:
#                 index = date - (end_date + 1)
#                 data_date = f'{year} {end_month} {date}'
#                 writer.writerow([data_date, values[index]])
#                 date = date + 1