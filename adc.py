import busio
import digitalio 
import board 
import adafruit_mcp3xxx.mcp3008 as MCP 
from adafruit_mcp3xxx.analog_in import AnalogIn

import threading
import time
import datetime
import RPi.GPIO as GPIO
import math

#pins used
SCLK = 23
MISO = 21
MOSI = 19
CE0 = 24
BTN = 4
sampling = [10, 5, 1] #different time intervals
global i
i = 0 #sampling index for different time intervals

def read_adc():
	global spi, cs, mcp, chan, chan1, chan3 
	# create the spi bus
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

	# create the cs (chip select)
	cs = digitalio.DigitalInOut(board.D5)

	# create the mcp object
	mcp = MCP.MCP3008(spi, cs)

	# create an analog input channel on pin 0
	chan = AnalogIn(mcp, MCP.P2)

	# create analog input channel on pin 1
	chan1 = AnalogIn(mcp, MCP.P1)

	#attempt at creating interrupt
	chan3 = AnalogIn(mcp, MCP.P3)

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(BTN, GPIO.OUT)
#GPIO.output(BTN, GPIO.HIGH)
#GPIO.add_event_detect(BTN, GPIO.RISING, callback=my_callback, bouncetime=300)

#attempt at implementing interrupt
def my_callback(BTN):
	""" 
	THIS CHANGES THE SAMPLING INTERVALS; 10s, 5s, 1s
	"""
	print("Button pressed!!")

#GPIO.add_event_detect(BTN, GPIO.FALLING, callback=my_callback, bouncetime=300)


def sensor_temp(adc_value):
	"""Temperature calculation"""

	voltage = adc_value*(3.3/1024.0)
	temp = ((voltage - 0.5)/10)
	#temp = temp - 0.5    # calibrating to 0 degrees C (500mV)
	#temp = temp/0.01   # temperature coefficient (10mV/C)
	t = (temp - 500)/10
	return temp

#setup()
print("{:<15} {:<15} {:<15} {:>2} {:<15}".format('Runtime','Temp Reading','Temp',"",'Light Reading'))
start = time.time()

while True:
	x = threading.Thread(target=read_adc)
	x.start()
	x.join()
	end = time.time()
	print("{:<15} {:<15} {:<15.1f} {:>2} {:<15}".format(str(math.floor((end-start)))+"s", chan.value,sensor_temp(chan.value), "C", chan1.value))
	if i >= 2:
		i=0

	#if chan.value == 0:
	#	print("Button pressed!!")
	#	i += 1
	#time.sleep(sampling[i])
	time.sleep(1)
	pass
