import os
import nexmo
import requests
from datetime import datetime


NEXMO_API_KEY = os.getenv('NEXMO_API_KEY')
NEXMO_API_SECRET = os.getenv('NEXMO_API_SECRET')
MYNUM = os.getenv('MYNUM')
OWMAP_KEY = os.getenv('OWMAP_KEY')
CITY_ID = 1701947
OWMAP_API_ENDPOINT = 'https://api.openweathermap.org/data/2.5/forecast?id=%s&appid=%s&units=metric'

client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)


def send_messages(message):
    print('Sending messages')
    for m in message.split('\n'):
        send_message(m)

def send_message(message='Hello self'):
    print('Sending message')
    client.send_message({
        'from': 'aldnav',
        'to': MYNUM,
        'text': message
    })

def get_forecast(city=CITY_ID):
    print('Getting forecast')
    r = requests.get(OWMAP_API_ENDPOINT % (city, OWMAP_KEY))
    results = r.json()['list']
    forecast = [
      "%s %s %s" % (
          datetime.fromtimestamp(x['dt']).strftime('%m-%d %I %p'),
          x['weather'][0]['description'],
          x['main']['temp'])
      for x in list(results)
    ]
    return '\n'.join(forecast)


if __name__ == '__main__':
    forecast = get_forecast()
    send_messages(forecast)

