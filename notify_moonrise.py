'''
Sends a public announcement to Google Assistant
if the moon rises in the evening.
'''

from datetime import datetime, timedelta, date
import os
import random
import requests
from dotenv import load_dotenv


def main():
    '''
    Sends announcement if the moon has risen between 10 and 20 minutes ago.
    The announcement is sent only between `notify_start` and `notify_end` times.
    A cron job is set up to run this script at 10-min intervals between
    15:00 and 23:00 daily.
    '''

    notify_start = '17:00'
    notify_end = '21:30'

    # sends announcement if: (now - m_max) < moon_rise < (now - m_min)
    m_min = 10
    m_max = 20

    date_string = date.today().strftime("%Y-%m-%d")
    start = parse_date_time(date_string, notify_start)
    end = parse_date_time(date_string, notify_end)
    moonrise = get_today_moonrise_datetime(date_string)

    if start < moonrise < end:
        time_delta = datetime.now() - moonrise
        if timedelta(minutes=m_min) < time_delta < timedelta(minutes=m_max):
            notify_moonrise(moonrise)


def parse_date_time(d_str, t_str):
    '''
    Returns datetime Object based on date (d) and time (t) parts.
    '''

    return datetime.strptime('%s %s' % (d_str, t_str), '%Y-%m-%d %H:%M')


def get_today_moonrise_datetime(date_string):
    '''
    Returns formatted datetime Object for today.
    '''

    current_year = date.today().year
    data_path = os.path.dirname(os.path.abspath(__file__)) + '/data'
    datetime_string = ''

    for line in open(data_path + '/%s.csv' % current_year):
        if line.startswith(date_string):
            if '-:-' not in line:
                datetime_string = line.replace(',', ' ').strip()

    if datetime_string:
        moonrise = datetime.strptime(datetime_string, '%Y-%m-%d %H:%M')
        return moonrise
    else:
        return False


def notify_moonrise(the_time):
    '''
    Sends random notification to Google Assistant.
    '''
    load_dotenv()
    hour = the_time.hour
    minute = the_time.minute

    messages = [
        'Look! A fairly super moon has risen at %s:%s.' % (hour, minute),
        'Did you know the moon has just risen at %s:%s?' % (hour, minute),
        'Pssst, the moon just rose at %s:%s!' % (hour, minute),
        'Hey you,today\'s moonrise was at %s:%s.' % (hour, minute),
        'At %s:%s the moon shall rise.' % (hour, minute),
        'Behold! The mighty moon has risen at %s:%s.' % (hour, minute)
    ]

    headers = {'Content-Type': 'application/json'}

    data = '{"command":"%s", "user":"%s", "broadcast":true}' % (
        random.choice(messages), os.getenv('GA_USER'))

    url = 'http://127.0.0.1:3000/assistant'

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print('Notify moonrise successfully!')
    else:
        print('Nofify moonrise failed.')


if __name__ == "__main__":
    main()
