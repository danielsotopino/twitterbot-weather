import requests
import socket
from papirus import PapirusText
from datetime import datetime
import pytz
from twython import Twython

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

def main():
    res = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Santiago,CL&lang=es&units=metric&APPID=7de73ddd95cb94e57612e1676343132f')
    print(res.json())
    main_data = res.json()['main']
    actual_temp = main_data['temp']
    humidity = main_data['humidity']
    temp_min = main_data['temp_min']
    temp_max = main_data['temp_max']
    clouds = res.json()['clouds']['all']
    print_papyrus(actual_temp, temp_min, temp_max, humidity, clouds)
    post_twitter(actual_temp, temp_min, temp_max, humidity, clouds)

def print_papyrus(temp, temp_min, temp_max, humidity, clouds):
    screen = PapirusText(rotation=90)
    ip = get_ip()
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Chile/Continental"))
    screen.write('T: ' + str(temp) + '\nT.min: ' + str(temp_min) + '\nT.max: ' + str(temp_max) + '\nHum: ' + str(humidity) + '\nNub: ' + str(clouds) + '\nHora: ' + pst_now.strftime("%H:%M:%S") + '\nIP: ' + ip)
    
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def post_twitter(temp, temp_min, temp_max, humidity, clouds):
    twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Chile/Continental"))
    message = 'T: ' + str(temp) + '\nT.min: ' + str(temp_min) + '\nT.max: ' + str(temp_max) + '\nHum: ' + str(humidity) + '\nNub: ' + str(clouds) + '\nHora: ' + pst_now.strftime("%H:%M:%S")
    twitter.update_status(status=message)
    print("Tweeted: {}".format(message))
	
if __name__ == '__main__':
   main()
