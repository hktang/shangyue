'''
Retrieves the daily moonrise data based on lat long coordinates.
This is called by the crontab regularly to generate annual data.
'''

from datetime import date, timedelta
import os
import requests
from dotenv import load_dotenv


def main():
    '''
    Retrieves the daily moonrise data for lat long coordinates, and
    saves data in the 'data' directory.
    '''

    # Coordinates of a reasonably close-by location.
    lat = 34.6906934556
    long = 135.2785830232

    current_year = date.today().year
    # current_year = 2021

    next_year = current_year + 1
    start_date = date(next_year, 1, 1)
    end_date = date(next_year + 1, 1, 1)
    data_path = make_path('data')

    with open('%s/%s.csv' % (data_path, next_year), 'wb') as file:
        load_dotenv()
        for single_date in daterange(start_date, end_date):

            date_string = single_date.strftime("%Y-%m-%d")
            params = (
                ('apiKey', os.getenv('KEY')),
                ('date', date_string),
                ('lat', lat),
                ('long', long)
            )

            response = requests.get(
                'https://api.ipgeolocation.io/astronomy', params=params)
            data = response.json()

            file.write((date_string + "," + data['moonrise'] + "\n").encode())


def daterange(start, end):
    '''
    Creates a generator for a range of dates.
    '''
    for days in range(int((end - start).days)):
        yield start + timedelta(days)


def make_path(sub_path):
    '''
    Creates directory under the root directory.
    '''
    data_path = os.path.dirname(os.path.abspath(__file__)) + '/' + sub_path

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    return data_path


if __name__ == "__main__":
    main()
