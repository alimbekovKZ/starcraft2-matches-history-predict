# -*- coding: utf-8 -*-
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

start = 1
end = 49
datapl = []

for i in range(start, end):
    response = requests.get('http://aligulac.com/earnings/?page=' + str(i) + '&year=all&country=all&currency=all')
    soup = BeautifulSoup(response.text)
    table = soup.find('table', attrs={'class': 'table table-striped table-hover'})
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td', attrs={'class': 'ea_name'})
        for col in cols:
            for href in col.find_all('a'):
                datapl.append(href['href'].strip())



data = []
for i in range(len(datapl)):
# for i in range(len(datapl)-39):
     print 'http://aligulac.com'+datapl[i]+'results/'
     response = requests.get('http://aligulac.com'+datapl[i]+'results/')
     # response = requests.get('http://aligulac.com/players/48-INnoVation/results/')
     soup = BeautifulSoup(response.text)

     table = soup.find('table', attrs={'class': 'table table-hover'})

     rows = table.find_all('tr')

     for row in rows:
         cols = row.find_all('td')
         for col in cols:
             data.append(col.text.strip())
             data.append(col['class'])
         for img in row.find_all('img'):
             if img.get('alt') != None and "flag" not in img.get('src') and "unrated" not in img.get('alt'):
                 data.append(img['alt'])

data = [data[i:i + 18] for i in range(0, len(data), 18)]

for i in range(len(data)):
        data[i].pop(1)
        data[i].pop(1)
        data[i].pop(1)
        data[i].pop(4)
        data[i].pop(6)
        data[i].pop(6)
        data[i].pop(6)
        data[i].pop(6)
        # print data[i]
        # print data[i][2]
        data[i][2].pop(0)
        data[i][5].pop(0)

df = pd.DataFrame(data, columns=["match_date", "player_1", "player_1_match_status", "score", "player_2","player_2_match_status", "player_1_race", "player_2_race", "addon", "tournament_type"])

df.to_csv('C:/1.csv', index=False, encoding='utf-8')
