#!/usr/bin/env python
import paho.mqtt.publish as publish
from Adafruit_BME280 import *
from periphery import GPIO
from time import sleep

SPI_BUS = 0
SPI_DEV_1 = 1
SPI_DEV_2 = 2
SPI_DEV_3 = 3
SPI_DEV_4 = 4
SPI_DEV_5 = 5
RALAY_1_GPIO = 138
RALAY_2_GPIO = 137
RALAY_3_GPIO = 36
RALAY_4_GPIO = 35
SPI_DEV_RELAY_STATE = {SPI_DEV_1:((RALAY_1_GPIO, True),
								  (RALAY_2_GPIO, True),
								  (RALAY_3_GPIO, True),
								  (RALAY_4_GPIO, True)),
					   SPI_DEV_2:((RALAY_1_GPIO, False),
					   			  (RALAY_2_GPIO, True),
					   			  (RALAY_3_GPIO, True),
					   			  (RALAY_4_GPIO, True)),
					   SPI_DEV_3:((RALAY_1_GPIO, False),
					   			 (RALAY_2_GPIO, False),
					   			 (RALAY_3_GPIO, True),
					   			 (RALAY_4_GPIO, True)),
					   SPI_DEV_4:((RALAY_1_GPIO, False),
					    		 (RALAY_2_GPIO, False),
					    		 (RALAY_3_GPIO, False),
					    		 (RALAY_4_GPIO, True)),
					   SPI_DEV_5:((RALAY_1_GPIO, False),
					   			  (RALAY_2_GPIO, False),
					   			  (RALAY_3_GPIO, False),
					   			  (RALAY_4_GPIO, False))}

class relayModule():
	def __init__(self):
		self.relaysDict = {}
		for relayGPIO in [RALAY_1_GPIO, RALAY_2_GPIO, RALAY_3_GPIO, RALAY_4_GPIO]:
			self.relaysDict[relayGPIO] = GPIO(relayGPIO, "out")

	def enableDeviceLine(self, device):
		for relayGPIO, state in SPI_DEV_RELAY_STATE[device]:
			self.relaysDict[relayGPIO].write(state)

	def close(self):
		for relay in self.relaysDict:
			self.relaysDict[relay].write(True)
			self.relaysDict[relay].close()

class bme280Sensor():
	def __init__(self, spiDev, spiBus = SPI_BUS):
		self.sensorInstance = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8, spi_bus=SPI_BUS, spi_dev=spiDev)

	@property
	def _temperature(self):
		return self.sensorInstance.read_temperature()

	@property
	def _pressure(self):
		pascals = self.sensorInstance.read_pressure()
		hectopascals = pascals / 100
		return hectopascals
		
	@property
	def _humidity(self):
		return self.sensorInstance.read_humidity()

	@property
	def temperaturePressureHumidityJSON(self):
		return '''{{
    	"temperature": "{0:0.3f}" ,
    	"pressure": "{1:0.2f}" ,
    	"humidity": "{2:0.2f}"
		}}'''.format(self._temperature, self._pressure, self._humidity)

if __name__ == "__main__":
	relayModuleInstance = relayModule()
	relayModuleInstance.enableDeviceLine(SPI_DEV_1)
	sleep(1)
	relayModuleInstance.enableDeviceLine(SPI_DEV_2)
	sleep(1)
	relayModuleInstance.enableDeviceLine(SPI_DEV_3)
	sleep(1)
	relayModuleInstance.enableDeviceLine(SPI_DEV_4)
	sleep(1)
	relayModuleInstance.enableDeviceLine(SPI_DEV_5)
	sleep(1)
	relayModuleInstance.close()
	#payload = param_json(degrees,hectopascals,humidity)
	#single(topic, payload=None, qos=0, retain=False, hostname="localhost",
	#    port=1883, client_id="", keepalive=60, will=None, auth=None, tls=None,
	#    protocol=mqtt.MQTTv311, transport="tcp")
	#publish.single("sensor/spi/{0}/{1}".format(sensor._spi_bus,sensor._spi_dev), payload)
	#print(payload)