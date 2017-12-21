import paho.mqtt.client as mqtt  # import the client1

import base64
import math
import json
import zlib
import binascii
import time
import os
import sys

class receive(object):
    def __init__(self,filename):
        self._callback = None
        self._f = None

        self._state = 0

        self._file =""
        self._filename = filename

    def __del__(self):
        self._f.close()

    def crc32(self, file):
      #  print('y',file)
      #  return bytes(file, encoding="UTF-8")
        return (binascii.crc32(bytes(file, encoding="UTF-8")))
      #  return (hex(zlib.crc32(file)% 2**32))
       # print(hex(binascii.crc32(file) & 0xffffffff))
      #  return (binascii.crc32(file.encode('utf-8')))

    def on_message1(self,msg):
        jj = json.loads(msg)
        print('msg',jj)

        if'START' in jj['type']:
            _packets = jj['packet']
            _crc_data = jj['crc']
            self._f = open(self._filename, 'wb')
        elif 'DATA' in jj['type']:
            if jj['crc'] == self.crc32(jj['data']):
            #    print('OK')
                encoded = jj['data']
                self._f.write(base64.b64decode(encoded))
                self._file += encoded
            else:
                print('NOK')
                sys.exit('NOK')
        elif 'END' in jj['type']:
            print('END')
            self._f.close()
            if jj['crc'] == self.crc32(self._file):
                print('END_crc',jj['crc'],self.crc32(self._file))
            else:
                print('FAIL')


    def on_message(self, message):

        jj = json.loads(message)
        print('message',jj)

        if self._state == 0:
            print('first')
            self._state = 1
            _total_pack = jj["packet"]
            _total_crc = jj["crc"]
        else:

       # print('x',message)
     #   jj = json.loads(message)
   #     print('cc',jj)
    #    crc = self.crc32(jj['data'])
     #   print('crc',crc, jj['crc'])
            if jj['crc'] == self.crc32(jj['data']):
              #  print('OK')
                encoded = jj['data']
              #  print('fff',encoded)
               # print(jj['packetID'])
                self._f.write(base64.b64decode(encoded))
            #    print('Type',type(encoded))
                self._file += encoded
                #for i in range(encoded):
                 #   self._file += str(i)
              #  self._file = self._file + base64.b64decode(encoded)
            else:
                print('NOK')
                sys.exit('NOK')

   #     print(_total_crc)

    def register_callback(self,callback):
        self._callback= callback

class mqttclient(object):
    def __init__(self):
        print('uuu')
        self._callback = None
        self._client = mqtt.Client('ffff')


    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    def on_message(self,client, userdata, msg):
      #  print("Topic : ", msg.topic, msg.payload)
        self._callback(msg.payload)
       # f = open("output.jpg", "w")  # there is a output.jpg which is different
        # f.write(msg.payload)
        #f.close()

    def on_subscribe(self,client, userdata, mid, granted_qos):
        print('Subscribe:',userdata,mid,granted_qos)

  #  def on_publish(self, mosq, userdata, mid):
     #   print('Publish')

    def publish(self, data):
      #  print('ddd',data)
     #   print(type(json.dumps(data)))
        self._client.publish("/photo", json.dumps(data), 0)
      #  time.sleep(0.01)

    def subscribe(self,channel):
        self._client.subscribe(channel,0)

    def register_callback(self,callback):
        self._callback = callback

    def message_callback_add(self,sub, callback):
        print('callback',callback)
        self._client.message_callback_add(sub,callback)


    def connect(self):
        print('test',self._client)
      #  self._client = mqtt.Client("image-send")
        self._client.on_message = self.on_message
        self._client.on_connect = self.on_connect
        self._client.on_subscribe = self.on_subscribe
#        self._client.on_publish = self.on_publish
        self._client.connect("192.168.2.50", 1883, 60)
     #   self._client.loop_forever()
    def start(self):
      #  self._client.loop_start()
        self._client.loop_forever()



if __name__ == '__main__':

    rec = receive('output1.jpg')
    mqtt = mqttclient()
    mqtt.connect()
  #  mqtt.start()
    mqtt.register_callback(rec.on_message1)
    mqtt.subscribe('/photo')
    mqtt.start()
 #   mqtt.message_callback_add('/photo',rec.on_message)

    time.sleep(30)

