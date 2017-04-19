import json
import time
import sensors

humidity_log_file = "logs/humidity.txt"
temperature_log_file = "logs/temperature.txt"

def load_data(): # reading plant data from external file dump
    try:
        with open("plants.json", "r") as f: 
            try:
                plants = json.load(f)
            except ValueError:
                plants = {}
            f.close()
    except IOError: # setting default data if cannot read from file
        plants = [{"plant_id": 0, "plant_image": "Graphics/plants/plant1.png", "name": "Sunny", "owner": "Caleb", "water": 10, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()},
        {"plant_id": 1, "plant_image": "Graphics/plants/plant2.png", "name": "Me", "owner": "Samuel", "water": 10, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()},
        {"plant_id": 2, "plant_image": "Graphics/plants/plant3.png", "name": "Mr Wu", "owner": "Shangjing", "water": 10, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()},
        {"plant_id": 3, "plant_image": "Graphics/plants/plant4.png", "name": ":D", "owner": "Jeremy", "water": 30, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()}]

    return plants

def save_data(plants): # saving new plant data to external file dump
    with open("plants.json", "w") as f:
        json.dump(plants, f)
        f.close()

def log_data():
    ''' Log humidity and temperature data and store into a file '''
    temp_humidity = sensors.get_humidity_temp() #{'temperature': 0, 'humidity': 0 }  
    temperature, humidity = temp_humidity["temperature"], temp_humidity["humidity"]

    with open(humidity_log_file, "a") as f:
        f.write("{0}: {1}\n".format(time.time(), humidity))
        f.close()

    with open(temperature_log_file, "a") as f:
        f.write("{0}: {1}\n".format(time.time(), temperature))
        f.close()
