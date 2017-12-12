#!/usr/bin/python

import paho.mqtt.client as mqtt
import requests
import time
import re

def on_message(mqttc, obj, msg):
    topic = msg.topic.split("/")
    data = re.findall('\d+', msg.payload.decode())
    measure = {"type": topic[1], "device_id": topic[1]+"_"+data[0], "value": data[1]}
    try:
        ret = requests.post('http://api.iot.svc.cluster.local/measure', json = measure)
        print(ret)
    except:
        print("unreachable server")




mqttc = mqtt.Client()
mqttc.on_message = on_message

mqttc.connect("broker.iot.svc.cluster.local", 1883, 60)

mqttc.subscribe("drivers/#", 0)
mqttc.loop_start()

while True:
    time.sleep(1)
    
