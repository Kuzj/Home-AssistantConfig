#!/usr/bin/env python
from Adafruit_BME280 import *
import paho.mqtt.publish as publish

def param_json(t,p,h):
	return '''{{
    "temperature": "{0:0.3f}" ,
    "pressure": "{1:0.2f}" ,
    "humidity": "{2:0.2f}"
}}'''.format(t,p,h)

sensor0 = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8, spi_bus=0, spi_dev=0)
sensors = [sensor0]
for sensor in sensors:
	degrees = sensor.read_temperature()
	pascals = sensor.read_pressure()
	hectopascals = pascals / 100
	humidity = sensor.read_humidity()
	payload = param_json(degrees,hectopascals,humidity)
	#single(topic, payload=None, qos=0, retain=False, hostname="localhost",
	#    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
	#    protocol=mqtt.MQTTv311, transport="tcp")
	publish.single("sensor/spi/{0}/{1}".format(sensor._spi_bus,sensor._spi_dev), payload)
	print(payload)
#print('Temp      = {0:0.3f} deg C'.format(degrees))
#print('Pressure  = {0:0.2f} hPa'.format(hectopascals))
#print('Humidity  = {0:0.2f} %'.format(humidity))