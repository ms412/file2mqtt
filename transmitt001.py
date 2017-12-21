#!/usr/bin/python
import paho.mqtt.client as mqtt  # import the client1

import base64
import math
import json
import zlib


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
   # client.subscribe("$SYS/#")

packet_size=265


def publishEncodedImage(encoded):
    end = packet_size
    start = 0
    length = len(encoded)
    print(length)
    picId = 'x'
    pos = 0
    no_of_packets = math.ceil(length / packet_size)
    print(no_of_packets)

    while start <= len(encoded):
    #    print(encoded[start:end])
        data = {"data": encoded[start:end], "pic_id": picId, "pos": pos, "size": no_of_packets}
        print(data)
        client.publish("/photo", json.dumps(data))
      #  client.publish("Image-Data", json.JSONEncoder().encode(data))
        end += packet_size
        start += packet_size
        pos = pos + 1

def convertImageToBase64():
    print('convert')
    with open("Tulips.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
        #encoded ='ert'
       # for x in encoded:

        return encoded.decode('ascii')

def on_publish(mosq, userdata, mid):
    print('Publish')
  # Disconnect after our message has been sent.
 #   mosq.disconnect()

# Specifying a client id here could lead to collisions if you have multiple
# clients sending. Either generate a random id, or use:
#client = mosquitto.Mosquitto()
client = mqtt.Mosquitto("image-send")
client.on_connect = on_connect
client.on_publish = on_publish
client.connect("192.168.2.50",1883,60)

#f = open("Tulips.jpg")
#imagestring = f.read()
#byteArray = bytes(imagestring)
print(convertImageToBase64())
publishEncodedImage(convertImageToBase64())
client.publish("photo",convertImageToBase64() ,0)
# If the image is large, just calling publish() won't guarantee that all
# of the message is sent. You should call one of the mosquitto.loop*()
# functions to ensure that happens. loop_forever() does this for you in a
# blocking call. It will automatically reconnect if disconnected by accident
# and will return after we call disconnect() above.
client.loop_forever()