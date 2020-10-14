import json
import os
import requests
from datetime import timedelta, date

def daterange(start_date, end_date):
  for n in range(int((end_date - start_date).days)):
    yield start_date + timedelta(n)

year = date.today().year

start_date = date(year, 10, 13)

end_date = date(year + 1, 10, 14)

data_path = os.path.dirname(os.path.abspath(__file__)) + '/data'

if not os.path.exists(data_path):
  os.makedirs(data_path)

with open(data_path + '/%s.csv' % year, 'wb') as f:

  for single_date in daterange(start_date, end_date):

    date_string = single_date.strftime("%Y-%m-%d")
    params = (
      ('apiKey', 'e4937f61b2f445498d7db27f407db18e'),
      ('date', date_string) 
    )

    response = requests.get('https://api.ipgeolocation.io/astronomy', params=params)
    data = response.json()

    f.write((date_string + "," + data['moonrise'] + "\n").encode())
