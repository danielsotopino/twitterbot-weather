# /etc/init.d/mqtt-temp.py
### BEGIN INIT INFO
# Provides:          mqtt-temp.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

import paho.mqtt.client as mqtt
from twython import Twython, TwythonError, TwythonRateLimitError
from datetime import datetime
import pytz
import zc.lockfile
lock = zc.lockfile.LockFile('lock')

from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("$SYS/#")
    client.subscribe("esp/#", qos=0)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == "esp/temp":
        print(msg.topic+" "+str(msg.payload))
        post_twitter(msg.payload)

    if msg.topic == "esp/temp1":
        print(msg.topic+" "+str(msg.payload))
        post_twitter_temp1(msg.payload)

    if msg.topic == "esp/humid1":
        print(msg.topic+" "+str(msg.payload))
        post_twitter_humid1(msg.payload)


def post_twitter(temp):
    twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Chile/Continental"))
    message = 'Hello! Soy el sensor DHT11 y hay ' + temp + ' a las: ' + pst_now.strftime("%H:%M:%S")
    response = twitter.update_status(status=message)
    print("Tweeted: {}".format(message))

def post_twitter_temp1(temp):
    twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Chile/Continental"))
    message = 'Hello! Soy el sensor DHT11 y hay ' + temp + ' a las: ' + pst_now.strftime("%H:%M:%S") + ' en el balcon'
    response = twitter.update_status(status=message)
    print("Tweeted: {}".format(message))

def post_twitter_humid1(temp):
    twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret)
    utc_now = pytz.utc.localize(datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Chile/Continental"))
    message = 'Hello! Soy el sensor HW80 y hay ' + temp + ' de humedad a las: ' + pst_now.strftime("%H:%M:%S") + ' en la plantita Purpurilla que esta en el balcon'
    response = twitter.update_status(status=message)
    print("Tweeted: {}".format(message))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)



# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()