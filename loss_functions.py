import time
import math

def calculate_water_loss(water, last_water_time):
	''' Takes in the previous water level, and the last time the plant was watered, and calculate its new estimated water level '''
	time_passed = time.time() - last_water_time
	water = math.exp(-time_passed/10000) * water
	print(water)
	return water

def calculate_fertilizer_loss(fertilizer, last_fertilized_time):
	''' Takes in the previous fertilizer level, and the last time the plant was fertilized, and calculate its new estimated fertilizer level '''
	time_passed = time.time() - last_fertilized_time
	fertilizer = math.exp(-time_passed/10000) * fertilizer
	print(fertilizer)
	return fertilizer

