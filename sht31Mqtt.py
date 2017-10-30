#!/usr/bin/python
import sys
import smbus
import time
import paho.mqtt.client as mqtt

mqttServer = "localhost"
mqttTopicTemperature = "sensor/phone/temperature"
mqttTopicHumidity = "sensor/phone/humidity"
mqttUserId = "openhabian"
mqttPassword = "7017slg"


# Get I2C bus
bus = smbus.SMBus(1)

# SHT31 address, 0x44(68)
bus.write_i2c_block_data(0x44, 0x2C, [0x06])

time.sleep(0.5)

# SHT31 address, 0x44(68)
# Read data back from 0x00(00), 6 bytes
# Temp MSB, Temp LSB, Temp CRC, Humididty MSB, Humidity LSB, Humidity CRC
data = bus.read_i2c_block_data(0x44, 0x00, 6)

# Convert the data
temp = data[0] * 256 + data[1]
temperature = -45 + (175 * temp / 65535.0)
humidity = 100 * (data[3] * 256 + data[4]) / 65535.0


humidityString = '{0:0.2f}'.format(humidity)
temperatureString = '{0:0.2f}'.format(temperature)

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

sys.exit(0)

