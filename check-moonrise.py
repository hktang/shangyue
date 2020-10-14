import os 
import random
import requests
from datetime import datetime, timedelta, date

data_path = os.path.dirname(os.path.abspath(__file__)) + '/data'

today = date.today()

year = today.year

date_string = today.strftime("%Y-%m-%d")

datetime_string = ''

start = datetime.strptime(
  today.strftime("%Y-%m-%d") + ' 17:00', '%Y-%m-%d %H:%M'
)

end = datetime.strptime(
  today.strftime("%Y-%m-%d") + ' 21:30', '%Y-%m-%d %H:%M'
)

def notify_moonrise(time):
  messages = [
  'Look! A fairly super moon has risen at %s:%s.' % (time.hour, time.minute),
  'Did you know the moon has just risen at %s:%s?' % (time.hour, time.minute),
  'Pssst, the moon just rose at %s:%s!' % (time.hour, time.minute),
  'Watch out for the rising moon! Today\'s moonrise was at %s:%s.' % (time.hour, time.minute),
  'Slipping softly through the sky, at %s:%s the moon shall rise.' % (time.hour, time.minute),
  'Behold! The mighty moon has risen at %s:%s.' % (time.hour, time.minute)
  ]

  headers = {'Content-Type': 'application/json'}
  data = '{"command":"%s", "user":"hktang", "broadcast":true}' % random.choice(messages)
  url = 'http://127.0.0.1:3000/assistant'

  response = requests.post(url, headers=headers, data=data)

  if response.status_code == 200:
    print('Notify moonrise successfully!')
  else:
    print('Nofify moonrise failed.')

for line in open(data_path + '/%s.csv' % year):
  if line.startswith(date_string):
    if '-:-' not in line:
      datetime_string = line.replace(',',' ').replace('\n', '')
  
if len(datetime_string) > 0:
  moonrise = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')

if start < moonrise < end:
  time_delta = datetime.now() - moonrise
  if timedelta(minutes = 10) < time_delta < timedelta(minutes = 20):
    notify_moonrise(moonrise)

