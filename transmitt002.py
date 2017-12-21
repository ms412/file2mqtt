import paho.mqtt.client as mqtt  # import the client1

import base64
import math
import json
import zlib
import binascii
import os
import time


class sendfile(object):
    def __init__(self):
        self._packetSize = 128
        self._callback = None
        self._encodedfile = None

    def crc32(self, file):
      #  return (hex(zlib.crc32(file)% 2**32))
       # print(hex(binascii.crc32(file) & 0xffffffff))
        return (binascii.crc32(file.encode('utf-8')))

    def convert(self,filename):
        print('convert')
        with open(filename,"rb") as image_file:
            encoded = base64.b64encode(image_file.read())
            # encoded ='ert'
            # for x in encoded:
            self._encodedfile= encoded.decode('ascii')
            return

    def packet(self):

        _end = self._packetSize
        _start = 0
        _length = len(self._encodedfile)
        _packetID = 0
        _no_packets= round(_length/self._packetSize+0.5)
        print( round(_length/self._packetSize+0.5))
        print(_length)

        data = { "packet": _no_packets,"type":"START","crc": self.crc32(self._encodedfile)}
        self._callback(data)

        while _start <= _length:
            data = {"data": self._encodedfile[_start:_end], "type":"DATA","packetID": _packetID, "crc": self.crc32(self._encodedfile[_start:_end])}
           # data = {"data": file[_start:_end], "packetID": _packetID}
         #   print('DAATA',data)
            self._callback(data)
            _end += self._packetSize
            _start += self._packetSize
            _packetID = _packetID + 1
        print(_packetID)
        data = {"packet":_packetID,"type":"END","crc": self.crc32(self._encodedfile)}
        self._callback(data)

    def sendfile(self,filename):
        self.convert(filename)

    def register_callback(self,callback):
        self._callback= callback



class mqttclient(object):
    def __init__(self):
        print('uuu')
        self._client = mqtt.Client('ggg')


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

  #  def on_publish(self, mosq, userdata, mid):
     #   print('Publish')

    def publish(self, data):
      #  print('ddd',data)
     #   print(type(json.dumps(data)))
        self._client.publish("/photo", json.dumps(data), 1)
       # print(data)
        time.sleep(0.01)

    def connect(self):
        print('test',self._client)
      #  self._client = mqtt.Client("image-send")
        self._client.on_connect = self.on_connect
#        self._client.on_publish = self.on_publish
        self._client.connect("192.168.2.50", 1883, 60)
     #   self._client.loop_forever()
        self._client.loop_start()


if __name__ == '__main__':

    mqtt = mqttclient()
    mqtt.connect()

    sf = sendfile()
    sf.register_callback(mqtt.publish)
  #  x = sf.sendfile('Tulips.jpg')
    x = sf.sendfile('Jellyfish.jpg')
    print(x)
    sf.packet()