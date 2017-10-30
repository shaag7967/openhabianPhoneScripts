#!/usr/bin/python
import sys
import Adafruit_DHT
import paho.mqtt.client as mqtt
    

sensorType = Adafruit_DHT.AM2302
sensorPin = 4

mqttServer = "localhost"
mqttTopicTemperature = "sensor/phone/temperature"
mqttTopicHumidity = "sensor/phone/humidity"
mqttUserId = "openhabian"
mqttPassword = "7017slg"



humidity, temperature = Adafruit_DHT.read_retry(sensorType, sensorPin)

if humidity is not None and temperature is not None:
  humidityString = '{0:0.1f}'.format(humidity)
  temperatureString = '{0:0.1f}'.format(temperature)

  print(temperatureString)
  print(humidityString)

  mqttc = mqtt.Client()
  mqttc.username_pw_set(mqttUserId, mqttPassword)
  mqttc.connect(mqttServer, 1883)
  mqttc.loop_start()

  mqttc.publish(mqttTopicTemperature, temperatureString)
  mqttc.publish(mqttTopicHumidity, humidityString)
 
  mqttc.loop_stop()
  mqttc.disconnect()
else:
  sys.exit(1)

sys.exit(0)
