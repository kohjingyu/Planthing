import RPi.GPIO as GPIO
import time

humidity_sensor = 21

def get_humidity_temp():
	'''
	Returns temperature (in Celsius) and humidity (in %) from DHT11 sensor
	This function is modified from https://github.com/touchEngine/micro-meteorological-station/tree/master/DHT11 (free use license)
	'''
	num_bits = 40

	channel = humidity_sensor
	data = []
	j = 0
	GPIO.setmode(GPIO.BCM)
	# Sleep for 1 second for the sensor to set up
	time.sleep(1)
	GPIO.setup(channel, GPIO.OUT)
	GPIO.output(channel, GPIO.LOW)
	time.sleep(0.02)
	GPIO.output(channel, GPIO.HIGH)
	GPIO.setup(channel, GPIO.IN)
	while GPIO.input(channel) == GPIO.LOW:
		continue
	while GPIO.input(channel) == GPIO.HIGH:
		continue
	while j < num_bits:
		k = 0
		while GPIO.input(channel) == GPIO.LOW:
			continue
		while GPIO.input(channel) == GPIO.HIGH:
			k += 1
			if k > 100:
				break

		if k < 8:
			data.append(0)
		else:
			data.append(1)
			j += 1

	humidity = bin_to_dec(data[0:8])
	humidity_point = bin_to_dec(data[8:16])
	temperature = bin_to_dec(data[16:24])
	temperature_point = bin_to_dec(data[24:32])
	check = bin_to_dec(data[32:40])

	tmp = humidity + humidity_point + temperature + temperature_point
	if check == tmp:
		return {"temperature": temperature, "humidity": humidity }
	else:
		print("Error in reading temperature and humidity. May be inaccurate.")
		return {"temperature": temperature, "humidity": humidity }

def bin_to_dec(bin_value):
	result = 0
	for i in range(8):
		result += bin_value[i] * 2 ** (7 - i)
	return result

