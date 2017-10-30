#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import paho.mqtt.client as mqtt
import time


mqttServer = "localhost"
mqttTopic = "sensor/phone/motion"
mqttUserId = "openhabian"
mqttPassword = "7017slg"


IO_PIN_MOTION = 16


GPIO.setmode(GPIO.BCM)  

GPIO.setup(IO_PIN_MOTION, GPIO.IN)


def cb_motion(pin):
    motionDetected = GPIO.input(IO_PIN_MOTION)
    print motionDetected
    mqttc.publish(mqttTopic, motionDetected)


GPIO.add_event_detect(IO_PIN_MOTION, GPIO.BOTH, callback=cb_motion)


mqttc = mqtt.Client()
mqttc.username_pw_set(mqttUserId, mqttPassword)
mqttc.connect(mqttServer, 1883)
mqttc.loop_start()

cb_motion(0)

while True:
    time.sleep(60*5)


mqttc.loop_stop()
mqttc.disconnect()
GPIO.cleanup()

sys.exit(0)

