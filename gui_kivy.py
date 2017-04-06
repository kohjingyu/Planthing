import sensors
import pump
import loss_functions

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.config import Config

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

from kivy.uix.progressbar import ProgressBar

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.clock import Clock

from functools import partial

import random
import json
import time
import math

screen_width = 800
screen_height = 500

Config.set('graphics', 'width', screen_width)
Config.set('graphics', 'height', screen_height)

humidity_log_file = "logs/humidity.txt"
temperature_log_file = "logs/temperature.txt"

def load_data():
    try:
        with open("plants.json", "r") as f:
            try:
                plants = json.load(f)
            except ValueError:
                plants = {}

            f.close()
    except IOError:
        # Default data
        plants = [{"plant_id": 0, "plant_image": "Graphics/plants/plant1.png", "name": "Sunny", "owner": "Caleb", "water": 10, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()},
        {"plant_id": 1, "plant_image": "Graphics/plants/plant2.png", "name": "Me", "owner": "Samuel", "water": 10, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()},
        {"plant_id": 2, "plant_image": "Graphics/plants/plant3.png", "name": "Mr Wu", "owner": "Shangjing", "water": 10, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()},
        {"plant_id": 3, "plant_image": "Graphics/plants/plant4.png", "name": ":D", "owner": "Jeremy", "water": 30, "temp": 30, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()}]
        
    return plants

def save_data():
    with open("plants.json", "w") as f:
        json.dump(plants, f)
        f.close()

def log_data():
    temp_humidity = sensors.get_humidity_temp()
    temperature, humidity = temp_humidity["temperature"], temp_humidity["humidity"]

    with open(humidity_log_file, "a") as f:
        f.write("{0}: {1}".format(time.time(), humidity))
        f.close()

    with open(temperature_log_file, "a") as f:
        f.write("{0}: {1}".format(time.time(), temperature))
        f.close()

class ImageButton(ButtonBehavior, Image):
    pass

class MainMenu(Screen):
    ''' Main Menu of the application '''

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        grid_layout = GridLayout(cols=2)

        layout_left=FloatLayout()

        # Colored background for left side of main menu
        layout_left.canvas.add(Color(0.8314, 0.7569, 0.4824))
        layout_left.canvas.add(Rectangle(pos=(0,0),size=(screen_width/2,screen_height),orientation='horizontal'))
        layout_left.add_widget(Label(text="[b][size=42][color=#594a42]PLANTHING[/color][/size][/b]", markup=True,
            size_hint=(.5, .5), pos_hint={'x':.25, 'y':.4}))

        temp_humidity = sensors.get_humidity_temp()

        temperature_string = "[b][size=18][color=#594a42]Temperature: {0} C[/color][/size][/b]".format(temp_humidity["temperature"])
        humidity_string = "[b][size=18][color=#594a42]Humidity: {0}%[/color][/size][/b]".format(temp_humidity["humidity"])
        # light_string = "Light: 10 lumens"

        self.temperature_widget = Label(text=temperature_string, markup=True, size_hint=(.5, .05), pos_hint={'x':.25, 'y':0.2})
        layout_left.add_widget(self.temperature_widget)
        self.humidity_widget = Label(text=humidity_string, markup=True, size_hint=(.5, .05), pos_hint={'x':.25, 'y':0.15})
        layout_left.add_widget(self.humidity_widget)
        # self.light_widget = Label(text=light_string, size_hint=(.5, .5), pos_hint={'x':.25, 'y':0.0})
        # layout_left.add_widget(light_widget)

        layout_right = FloatLayout(cols=2, row_force_default=True, row_default_height=screen_height/2)
        layout_right.canvas.add(Color(1, 1, 1))
        layout_right.canvas.add(Rectangle(pos=(screen_width/2,0),size=(screen_width/2,screen_height),orientation='horizontal'))

        # Initialize the plants
        plant_size = 0.3
        plant_padding = (0.5 - plant_size)/2
        positions = [(plant_padding, plant_padding), (0.5 + plant_padding, plant_padding), (plant_padding, 0.5 + plant_padding), (0.5 + plant_padding, 0.5 + plant_padding)]
        for i in range(len(plants)):
            plant = plants[i]
            (x, y) = positions[i]

            plant_button = ImageButton(source=plant["plant_image"], on_press=partial(self.view_detail, plant_id=plant["plant_id"]),
                size_hint=(plant_size, plant_size), pos_hint={'x': x, 'y': y})
            layout_right.add_widget(plant_button)
            plant_background = Rectangle(pos=(x, y), size=(plant_size,plant_size), orientation='horizontal')
            layout_right.canvas.add(plant_background)

            plant_text = "[b][color=#594a42]{0}[/color][/b]".format(plant['name'])
            label_height = 0.05
            label_offset = 0.09
            layout_right.add_widget(Label(text=plant_text, markup=True, size_hint=(plant_size, label_height), pos_hint={'x': x, 'y': y - plant_size/2 + label_offset}))

        grid_layout.add_widget(layout_left)
        grid_layout.add_widget(layout_right)

        self.add_widget(grid_layout)

    def update(self, *args):
        ''' Update data from all sensors '''
        temp_humidity = sensors.get_humidity_temp()

        self.temperature_widget.text = "[b][size=18][color=#594a42]Temperature: {0} C[/color][/size][/b]".format(temp_humidity["temperature"])
        self.humidity_widget.text = "[b][size=18][color=#594a42]Humidity: {0}%[/color][/size][/b]".format(temp_humidity["humidity"])

        # Log the humidity and temperature values to file
        log_data()

    def view_detail(self, object, plant_id):
        self.manager.transition.direction = "left"
        self.manager.get_screen("detail").update(plant_id)
        self.manager.current = "detail"

class Detail(Screen):
    def __init__(self, **kwargs):
        super(Detail, self).__init__(**kwargs)
        grid_layout = GridLayout(cols=2)

        self.plant = None

        left_layout = FloatLayout()
        left_layout.canvas.add(Color(0.8314, 0.7569, 0.4824))
        left_layout.canvas.add(Rectangle(pos=(0,0),size=(screen_width/2,screen_height),orientation='horizontal'))

        left_layout.canvas.add(Color(1, 1, 1))
        left_layout.canvas.add(Rectangle(pos=(screen_width/2,0),size=(screen_width/2,screen_height),orientation='horizontal'))

        left_layout.add_widget(Button(text="Back", on_press=self.back, size_hint=(1, .05), pos_hint={'x': 0, 'y': 0.95}))

        self.plant_name_label = Label(text="[b][size=18][color=#594a42]Name: Plant[/color][/size][/b]", markup=True, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.05})
        left_layout.add_widget(self.plant_name_label)

        self.owner_name_label = Label(text="[b][size=18][color=#594a42]Owned By: Person[/color][/size][/b]", markup=True, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        left_layout.add_widget(self.owner_name_label)

        right_layout = FloatLayout()

        # Add plant image
        plant_size = 0.6
        self.plant_image = Image(source="", size_hint=(plant_size, plant_size), pos_hint={'x': (1 - plant_size)/2, 'y': (1 - plant_size)/2})
        left_layout.add_widget(self.plant_image)

        # Water and fertilizer buttons
        btn_size = .3
        btn_gap = 0.05

        self.water_btn = ImageButton(source="Graphics/water_btn.png", size_hint=(btn_size, btn_size), pos_hint={'x': 0.5 - btn_gap/2 - btn_size, 'y': 0.05}, on_press=self.water)
        self.fertilizer_btn = ImageButton(source="Graphics/fertilizer_btn.png", size_hint=(btn_size, btn_size), pos_hint={'x': 0.5 + btn_gap/2, 'y': 0.05}, on_press=self.fertilize)

        right_layout.add_widget(self.water_btn)
        right_layout.add_widget(self.fertilizer_btn)

        progress_start_y = 0.8
        progress_bar_height = 0.1

        right_layout.add_widget(Label(text="[b][size=18][color=#594a42]Temperature: [/color][/size][/b]", markup=True, size_hint=(0.1, progress_bar_height), pos_hint={'x': 0.2, 'y': progress_start_y}))
        self.temperature_bar = ProgressBar(max=100, size_hint=(0.3, progress_bar_height), pos_hint={'x': 0.5, 'y': progress_start_y})
        self.temperature_bar.value = 80
        right_layout.add_widget(self.temperature_bar)

        right_layout.add_widget(Label(text="[b][size=18][color=#594a42]Water: [/color][/size][/b]", markup=True, size_hint=(0.1, progress_bar_height), pos_hint={'x': 0.2, 'y': progress_start_y - progress_bar_height}))
        self.water_bar = ProgressBar(max=100, size_hint=(0.3, progress_bar_height), pos_hint={'x': 0.5, 'y': progress_start_y - progress_bar_height})
        self.water_bar.value = 55
        right_layout.add_widget(self.water_bar)

        right_layout.add_widget(Label(text="[b][size=18][color=#594a42]Fertilizer: [/color][/size][/b]", markup=True, size_hint=(0.1, progress_bar_height), pos_hint={'x': 0.2, 'y': progress_start_y - 2*progress_bar_height}))
        self.fertilizer_bar = ProgressBar(max=100, size_hint=(0.3, progress_bar_height), pos_hint={'x': 0.5, 'y': progress_start_y - 2*progress_bar_height})
        self.fertilizer_bar.value = 90
        right_layout.add_widget(self.fertilizer_bar)

        grid_layout.add_widget(left_layout)
        grid_layout.add_widget(right_layout)
        self.add_widget(grid_layout)

    def update(self, plant_id):
        self.plant = plants[plant_id]
        self.plant_name_label.text = "[size=18][color=#594a42][b]Name:[/b] {0}[/color][/size]".format(self.plant["name"])
        self.owner_name_label.text = "[size=18][color=#594a42][b]Owned by:[/b] {0}[/color][/size]".format(self.plant["owner"])

        # Update plant image
        self.plant_image.source = self.plant["plant_image"]

        self.temperature_bar.value = self.plant["temp"]

        # Adjust water based on last water level
        self.water_bar.value = loss_functions.calculate_water_loss(self.plant["water"], self.plant["last_watered"])

        # Adjust fertilizer based on last fertilizer level
        self.fertilizer_bar.value = loss_functions.calculate_fertilizer_loss(self.plant["fertilizer"], self.plant["last_fertilized"])

    def update_data(self):
        self.plant_name_label.text = "[size=18][color=#594a42][b]Name:[/b] {0}[/color][/size]".format(self.plant["name"])
        self.owner_name_label.text = "[size=18][color=#594a42][b]Owned by:[/b] {0}[/color][/size]".format(self.plant["owner"])

        self.temperature_bar.value = self.plant["temp"]

        self.water_bar.value = self.plant["water"]
        self.fertilizer_bar.value = self.plant["fertilizer"]

    def water(self, object):
        # Turn on water pump for 2 seconds
        pump.pump(1, 2)

        # Update plant stats
        self.plant["water"] += 5
        self.plant["last_watered"] = time.time()
        self.update_data()
        save_data()

        # self.water_btn.disabled = True

    def fertilize(self, object):
        # Turn on fertilizer pump for the appropriate plant (id + 2, as pump 1 is the water pump)
        pump_number = self.plant["plant_id"] + 2
    	print pump_number
        pump.pump(pump_number, 2)

        # Update plant stats
        self.plant["fertilizer"] += 5
        self.plant["last_fertilized"] = time.time()
        self.update_data()
        save_data()

        # self.fertilizer_btn.disabled = True

    def back(self, object):
        self.manager.transition.direction = "right"
        self.manager.current = "main"

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        main = MainMenu(name="main")
        
        detail = Detail(name="detail")

        sm.add_widget(main)
        sm.add_widget(detail)
        sm.current = "main"

        # Update temperature data every 3 seconds
        update_interval = 3
        Clock.schedule_interval(main.update, update_interval)

        return sm

if __name__ == '__main__':
    plants = load_data()
    save_data()
    MyApp().run()


