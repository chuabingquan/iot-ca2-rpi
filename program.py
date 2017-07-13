import paho.mqtt.client as mqtt
import time
import helper
import sys
import json

hubAddress = deviceId = sharedAccessKey = None

def config_defaults():
    global hubAddress, deviceId, sharedAccessKey
    print('Loading default config settings')

    hubAddress = 'IOT-CA2-IOTHUB.azure-devices.net'
    deviceId = 'raspberrypi3'
    sharedAccessKey = '8ubN3VIq+LAme9xJLJ0mYHyyfxUlKIe5oPCExuPL4t0='

# callback function when client receives a response from server
def on_connect(client, userdata, flags, rc):
  print("Connected to MQTT!")
  client.subscribe(help.hubTopicSubscribe)

# callback function to receive subscribed message
def on_message(client, userdata, message):
  print("in on-message")

# callback function to send message to mqtt
def on_publish(client, userdata, mid):
    print "in on-publish"
    print("Message {0} sent from {1}".format(str(mid), deviceId))

config_defaults()

help = helper.Helper(hubAddress, deviceId, sharedAccessKey)

# Instatiate MQTT Client
client = mqtt.Client(deviceId, mqtt.MQTTv311)

client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.username_pw_set(help.hubUser, help.generate_sas_token(help.endpoint, sharedAccessKey))

print(help.generate_sas_token(help.endpoint, sharedAccessKey))

client.connect(hubAddress, 8883)
client.loop_start()
