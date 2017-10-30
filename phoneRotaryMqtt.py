#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import paho.mqtt.client as mqtt
import time


mqttServer = "localhost"
mqttTopicHook = "sensor/phone/hook"
mqttTopicRotary = "sensor/phone/rotary"
mqttUserId = "openhabian"
mqttPassword = "7017slg"


IO_PIN_DIAL_VALID = 21
IO_PIN_NUM_0 = 26
IO_PIN_NUM_1 = 19
IO_PIN_NUM_2 = 13
IO_PIN_NUM_3 = 6
IO_PIN_HOOK = 20


GPIO.setmode(GPIO.BCM)  

GPIO.setup(IO_PIN_HOOK, GPIO.IN)
GPIO.setup(IO_PIN_DIAL_VALID, GPIO.IN)
GPIO.setup(IO_PIN_NUM_0, GPIO.IN)
GPIO.setup(IO_PIN_NUM_1, GPIO.IN)
GPIO.setup(IO_PIN_NUM_2, GPIO.IN)
GPIO.setup(IO_PIN_NUM_3, GPIO.IN)



def cb_dial(pin):
    numberValid = GPIO.input(IO_PIN_DIAL_VALID)

    if numberValid == 1:
        binStr = str(GPIO.input(IO_PIN_NUM_3)) + str(GPIO.input(IO_PIN_NUM_2)) + \
                    str(GPIO.input(IO_PIN_NUM_1)) + str(GPIO.input(IO_PIN_NUM_0))
        mqttc.publish(mqttTopicRotary, int(binStr,2))

def cb_hook(pin):
    hangUp = GPIO.input(IO_PIN_HOOK)
    mqttc.publish(mqttTopicHook, hangUp)



GPIO.add_event_detect(IO_PIN_DIAL_VALID, GPIO.RISING, callback=cb_dial)
GPIO.add_event_detect(IO_PIN_HOOK, GPIO.BOTH, callback=cb_hook)


mqttc = mqtt.Client()
mqttc.username_pw_set(mqttUserId, mqttPassword)
mqttc.connect(mqttServer, 1883)
mqttc.loop_start()

cb_hook(0)

while True:
    time.sleep(60*5)


mqttc.loop_stop()
mqttc.disconnect()
GPIO.cleanup()

sys.exit(0)

