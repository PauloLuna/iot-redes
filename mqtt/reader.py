#!/usr/bin/python

import paho.mqtt.client as mqtt
import requests
import time

def on_message(mqttc, obj, msg):
    topic = msg.topic.split("/")
    data = msg.payload.decode().split("::")
    measure = {"type": topic[1], "device_id": topic[1]+"_"+data[0], "value": data[1]}
    try:
        ret = requests.post('http://localhost:5000/measure', json = measure)
        print(ret)
    except:
        print("unreachable server")


mqttc = mqtt.Client()
mqttc.on_message = on_message

mqttc.connect("localhost", 1883, 60)

mqttc.subscribe("drivers/#", 0)
mqttc.loop_forever()
    
