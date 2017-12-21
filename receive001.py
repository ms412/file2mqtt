#!/usr/bin/python

import time


import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connect" + str(rc))
    client.subscribe("/photo")

def on_message(client, userdata, msg):
    print ("Topic : ", msg.topic,msg.payload)
    f = open("output.jpg", "w")  #there is a output.jpg which is different
   # f.write(msg.payload)
    f.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.2.50", 1883, 60)

client.loop_forever()
