#!/usr/bin/python

import paho.mqtt.client as mqtt
import requests
import time


def iterate_devices():
    r = requests.get('http://api.iot.svc.cluster.local/devices')
    devices = r.json()
    for device in devices:
        if ('objective' in device.keys()) and ('command_topic' in device.keys()):
            device_id = device["_id"].split('_')[-1]
            topic = "commands/{}/{}".format(device["command_topic"], device_id)
            mqttc.publish(topic, device["objective"])
            print (topic+"/"+ str(device["objective"]))

mqttc = mqtt.Client()

mqttc.connect("broker.iot.svc.cluster.local", 1883, 60)

mqttc.subscribe("drivers/#", 0)
mqttc.loop_start()

while True:
    time.sleep(10)
    iterate_devices()

    
