# import sensors
# import pump
from loss_functions import loss_functions
from loss_functions import loss_functions2
# from plant_detail_screen import Detail

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.clock import Clock

from functools import partial

import random
import json
import time
import math

loss_functions().start()
loss_functions2().start()

screen_width = 800
screen_height = 500

# Config.set('graphics', 'width', screen_width)
# Config.set('graphics', 'height', screen_height)

Window.size = (screen_width, screen_height)

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

def save_data(): # saving new plant data to external file dump
    with open("plants.json", "w") as f:
        json.dump(plants, f)
        f.close()

def log_data():
    temp_humidity = {'temperature': 0, 'humidity': 0 } #sensors.get_humidity_temp()
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

        self.addPlant = None # This will be set to the addPlants Screen later on
        self.update_plants()

    def update_plants(self, *args):
        try:
            self.remove_widget(self.grid_layout)
        except:
            pass

        grid_layout = GridLayout(cols=2)

        # left side of display
        layout_left=FloatLayout()

        # colored background for left side of main menu
        layout_left.canvas.add(Color(0.968627451, 0.8274509804, 0.5490196078))
        layout_left.canvas.add(Rectangle(pos=(0,0),size=(screen_width/2,screen_height),orientation='horizontal'))
        layout_left.add_widget(Label(text="[b][size=42][color=#1c222a]PLANTHING[/color][/size][/b]", markup=True,
            size_hint=(.5, .5), pos_hint={'x':.25, 'y':.4}))

        # reading humidity and temp using sensors.get_humidity_temp()
        temp_humidity = {'temperature': 0, 'humidity': 0 } #sensors.get_humidity_temp()

        temperature_string = "[b][size=18][color=#1c222a]Temperature: {0} C[/color][/size][/b]".format(temp_humidity["temperature"])
        humidity_string = "[b][size=18][color=#1c222a]Humidity: {0}%[/color][/size][/b]".format(temp_humidity["humidity"])

        # temperature display
        self.temperature_widget = Label(text=temperature_string, markup=True, size_hint=(.5, .05), pos_hint={'x':.25, 'y':0.2})
        layout_left.add_widget(self.temperature_widget)
        
        # humidity display
        self.humidity_widget = Label(text=humidity_string, markup=True, size_hint=(.5, .05), pos_hint={'x':.25, 'y':0.15})
        layout_left.add_widget(self.humidity_widget)
        
        # self.light_widget = Label(text=light_string, size_hint=(.5, .5), pos_hint={'x':.25, 'y':0.0})
        # layout_left.add_widget(light_widget)
        # light_string = "Light: 10 lumens"

        # four plants on display
        layout_right = FloatLayout(cols=2, row_force_default=True, row_default_height=screen_height/2)
        layout_right.canvas.add(Color(1, 1, 1))
        layout_right.canvas.add(Rectangle(pos=(screen_width/2,0),size=(screen_width/2,screen_height),orientation='horizontal'))

        # initialize the plants
        plant_size = 0.3 # plant image width is 30% of width
        plant_padding = (0.5 - plant_size)/2 # total space for each plant is 50%
        positions = [(plant_padding, 0.5 + plant_padding), (0.5 + plant_padding, 0.5 + plant_padding), (plant_padding, plant_padding), (0.5 + plant_padding, plant_padding)]

        total_plants = 4
        for i in range(total_plants):
            # Position of this button
            (x, y) = positions[i]

            # If plant exists, add it
            if i < len(plants):
                plant = plants[i]

                # each plant icon is a button
                plant_button = ImageButton(source=plant["plant_image"], on_press=partial(self.view_detail, plant_id=plant["plant_id"]),
                    size_hint=(plant_size, plant_size), pos_hint={'x': x, 'y': y})
                layout_right.add_widget(plant_button)
                plant_background = Rectangle(pos=(x, y), size=(plant_size,plant_size), orientation='horizontal')
                layout_right.canvas.add(plant_background)

                # adding in names of plants
                plant_text = "[b][color=#1c222a]{0}[/color][/b]".format(plant['name'])
                label_height = 0.05
                label_offset = 0.09
                layout_right.add_widget(Label(text=plant_text, markup=True, size_hint=(plant_size, label_height), pos_hint={'x': x, 'y': y - plant_size/2 + label_offset}))
            else:
                # Plant doesn't exist, allow users to add new plant
                plant_button = Button(text="Add Plant", on_press=self.add_plant,
                    size_hint=(plant_size, plant_size), pos_hint={'x': x, 'y': y})
                layout_right.add_widget(plant_button)
                plant_background = Rectangle(pos=(x, y), size=(plant_size,plant_size), orientation='horizontal')
                layout_right.canvas.add(plant_background)

        # add left and right screens
        grid_layout.add_widget(layout_left)
        grid_layout.add_widget(layout_right)

        self.add_widget(grid_layout)
        self.grid_layout = grid_layout

        self.pump_command_for_water='stop'
        self.pump_command_for_fertiliser='stop'

    def add_plant(self, *args):
        ''' Move to the add plant screen '''
        self.manager.transition.direction = "left"
        self.manager.current = "add"

        self.addPlant.reset()

    def update(self, *args):
        ''' Update data from all sensors '''
        temp_humidity = {'temperature': 0, 'humidity': 0 } #sensors.get_humidity_temp()

        # formatting humidity and temperature text
        self.temperature_widget.text = "[b][size=18][color=#1c222a]Temperature: {0} C[/color][/size][/b]".format(temp_humidity["temperature"])
        self.humidity_widget.text = "[b][size=18][color=#1c222a]Humidity: {0}%[/color][/size][/b]".format(temp_humidity["humidity"])

        # Log the humidity and temperature values to file
        log_data()

        last_water_time = plants[0]["last_watered"]

        self.pump_command_for_water = loss_functions().step(last_water_time)
        if self.pump_command_for_water == 'auto_water':
            pump.pump(1,2)
            self.plant["water"] += 5
            self.plant["last_watered"] = time.time()
            self.update_data()
            save_data()
        self.pump_command_for_fertiliser = loss_functions2().step(last_water_time)
        if self.pump_command_for_fertiliser == 'auto_fertilise':
            pump_number = self.plant["plant_id"] + 2
            print pump_number
            pump.pump(pump_number, 2)
            # update plant stats
            self.plant["fertilizer"] += 5
            self.plant["last_fertilized"] = time.time()
            self.update_data()
            save_data()

        self.grid_layout.do_layout()

    def view_detail(self, object, plant_id):
        ''' specific plant view '''
        self.manager.transition.direction = "left"
        self.manager.get_screen("detail").update(plant_id)
        self.manager.current = "detail"

class Detail(Screen):
    ''' plant details screen ''' 
    def __init__(self, **kwargs):
        super(Detail, self).__init__(**kwargs) # detail superclass
        grid_layout = GridLayout(cols=2)

        self.mainMenu = kwargs['main']

        self.plant = None

        # left side
        left_layout = FloatLayout()

        # background colour
        left_layout.canvas.add(Color(0.968627451, 0.8274509804, 0.5490196078))
        left_layout.canvas.add(Rectangle(pos=(0,0),size=(screen_width/2,screen_height),orientation='horizontal'))

        # plant image
        plant_size = 0.6
        self.plant_image = Image(source="", size_hint=(plant_size, plant_size), pos_hint={'x': (1 - plant_size)/2, 'y': (1 - plant_size)/2})
        left_layout.add_widget(self.plant_image)

        left_layout.add_widget(Button(text="Back", on_press=self.back, size_hint=(1, .05), pos_hint={'x': 0, 'y': 0.95}))

        # plant name and owner labels
        self.plant_name_label = Label(text="[b][size=18][color=#1c222a]Name: Plant[/color][/size][/b]", markup=True, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0.05})
        self.owner_name_label = Label(text="[b][size=18][color=#1c222a]Owned By: Person[/color][/size][/b]", markup=True, size_hint=(1, 0.1), pos_hint={'x': 0, 'y': 0})
        left_layout.add_widget(self.plant_name_label)
        left_layout.add_widget(self.owner_name_label)

        # right side
        right_layout = FloatLayout()

        # background colour
        right_layout.canvas.add(Color(1, 1, 1))
        right_layout.canvas.add(Rectangle(pos=(screen_width/2,0),size=(screen_width/2,screen_height),orientation='horizontal'))

        # Water and fertilizer buttons
        btn_size = .3
        btn_gap = 0.05

        self.water_btn = ImageButton(source="Graphics/water_btn.png", size_hint=(btn_size, btn_size), pos_hint={'x': 0.5 - btn_gap/2 - btn_size, 'y': 0.05}, on_press=self.water)
        self.fertilizer_btn = ImageButton(source="Graphics/fertilizer_btn.png", size_hint=(btn_size, btn_size), pos_hint={'x': 0.5 + btn_gap/2, 'y': 0.05}, on_press=self.fertilize)

        right_layout.add_widget(self.water_btn)
        right_layout.add_widget(self.fertilizer_btn)

        progress_start_y = 0.8
        progress_bar_height = 0.1

        # temperature bar
        right_layout.add_widget(Label(text="[b][size=18][color=#1c222a]Temperature: [/color][/size][/b]", markup=True, size_hint=(0.1, progress_bar_height), pos_hint={'x': 0.2, 'y': progress_start_y}))
        self.temperature_bar = ProgressBar(max=100, size_hint=(0.3, progress_bar_height), pos_hint={'x': 0.5, 'y': progress_start_y})
        self.temperature_bar.value = 80
        ## model to be corrected
        right_layout.add_widget(self.temperature_bar)

        # water bar
        right_layout.add_widget(Label(text="[b][size=18][color=#1c222a]Water: [/color][/size][/b]", markup=True, size_hint=(0.1, progress_bar_height), pos_hint={'x': 0.2, 'y': progress_start_y - progress_bar_height}))
        self.water_bar = ProgressBar(max=100, size_hint=(0.3, progress_bar_height), pos_hint={'x': 0.5, 'y': progress_start_y - progress_bar_height})
        self.water_bar.value = 55
        ## model to be corrected
        right_layout.add_widget(self.water_bar)

        # fertilizer bar
        right_layout.add_widget(Label(text="[b][size=18][color=#1c222a]Fertilizer: [/color][/size][/b]", markup=True, size_hint=(0.1, progress_bar_height), pos_hint={'x': 0.2, 'y': progress_start_y - 2*progress_bar_height}))
        self.fertilizer_bar = ProgressBar(max=100, size_hint=(0.3, progress_bar_height), pos_hint={'x': 0.5, 'y': progress_start_y - 2*progress_bar_height})
        self.fertilizer_bar.value = 90
        ## model to be corrected
        right_layout.add_widget(self.fertilizer_bar)

        # delete button
        right_layout.add_widget(Button(text="[b][size=18][color=#1c222a]Delete[/color][/size][/b]", on_press=self.remove_plant, markup=True, size_hint=(0.25, progress_bar_height), pos_hint={'x': 0.5 - 0.25/2, 'y': progress_start_y - 4*progress_bar_height}))
        self.fertilizer_bar = ProgressBar(max=100, size_hint=(0.3, progress_bar_height), pos_hint={'x': 0.5, 'y': progress_start_y - 2*progress_bar_height})
        self.fertilizer_bar.value = 90
        ## model to be corrected
        right_layout.add_widget(self.fertilizer_bar)

        grid_layout.add_widget(left_layout)
        grid_layout.add_widget(right_layout)
        self.add_widget(grid_layout)

    def update(self, plant_id):
        ''' grabbing plant data from dictionary as user interacts  and every 3 seconds'''
        for plant in plants:
            if plant["plant_id"] == plant_id:
                self.plant = plant
                break

        self.plant_name_label.text = "[size=18][color=#1c222a][b]Name:[/b] {0}[/color][/size]".format(self.plant["name"])
        self.owner_name_label.text = "[size=18][color=#1c222a][b]Owned by:[/b] {0}[/color][/size]".format(self.plant["owner"])

        # update plant image
        self.plant_image.source = self.plant["plant_image"]

        # update temperature to current temp
        self.temperature_bar.value = self.plant["temp"]

        # adjust water based on last water level
        # self.water_bar.value = loss_functions.calculate_water_loss(self.plant["water"], self.plant["last_watered"])

        # adjust fertilizer based on last fertilizer level
        # self.fertilizer_bar.value = loss_functions.calculate_fertilizer_loss(self.plant["fertilizer"], self.plant["last_fertilized"])

    def update_data(self): 
        ''' update data on water or fertilization of plant '''

        self.temperature_bar.value = self.plant["temp"]
        self.water_bar.value = self.plant["water"]
        self.fertilizer_bar.value = self.plant["fertilizer"]

    def water(self, object):
        ''' water plants '''
        
        # turn on water pump for 2 seconds
        if self.pump_command_for_water == 'available':
            pump.pump(1, 2)
            # update plant stats
            self.plant["water"] += 5
            self.plant["last_watered"] = time.time()
            self.update_data()

            # update plant stats
            save_data()

    def fertilize(self, object):
        # turn on fertilizer pump for the appropriate plant (id + 2, as pump 1 is the water pump)
        if self.pump_command_for_fertiliser == 'available':
            pump_number = self.plant["plant_id"] + 2
            print pump_number
            pump.pump(pump_number, 2)
            # update plant stats
            self.plant["fertilizer"] += 5
            self.plant["last_fertilized"] = time.time()
            self.update_data()
            save_data()

        # self.fertilizer_btn.disabled = True

    def remove_plant(self, object):
        # Delete current plant
        plants.remove(self.plant)

        save_data()

        # Return the main menu and update plants
        self.manager.transition.direction = "right"
        self.manager.current = "main"
        self.mainMenu.update_plants()

    def back(self, object):
        self.manager.transition.direction = "right"
        self.manager.current = "main"

class AddPlant(Screen):
    def __init__(self, **kwargs):
        super(AddPlant, self).__init__(**kwargs)
        self.mainMenu = kwargs["main"]
        grid_layout = GridLayout(cols=2)

        left_layout = GridLayout(cols=1)
        left_layout.add_widget(Button(text="Back", on_press=self.back, size_hint=(1, .05), pos_hint={'x': 0, 'y': 0.95}))

        right_layout = GridLayout(cols=1)
        self.name_label = TextInput(text="Plant name here")
        right_layout.add_widget(self.name_label)

        self.owner_label = TextInput(text="Owner name")
        right_layout.add_widget(self.owner_label)

        self.plant_type = 0
        plant_type_dropdown = DropDown()
        self.plant_types = ["Parsley", "Cactus"]
        for plant_type in self.plant_types:
            btn = Button(text=plant_type, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: plant_type_dropdown.select(btn.text)) # Set button to select text on clicking of the dropdown options
            plant_type_dropdown.add_widget(btn)
        plant_type_dropdown.bind(on_select=self.selectPlantType) # On selection of a plant type, set the text of the button

        self.plant_dropdown_btn = Button(text='Select a Plant Type', size_hint=(None, None))
        self.plant_dropdown_btn.bind(on_release=plant_type_dropdown.open)

        right_layout.add_widget(self.plant_dropdown_btn)

        self.add_plant_btn = Button(text="Add Plant", on_press=self.add, disabled=True)
        right_layout.add_widget(self.add_plant_btn)

        grid_layout.add_widget(left_layout)
        grid_layout.add_widget(right_layout)

        self.add_widget(grid_layout)

    def selectPlantType(self, object, btn_text):
        setattr(self.plant_dropdown_btn, 'text', btn_text)
        self.plant_type = btn_text
        self.add_plant_btn.disabled = False

    def back(self, object):
        self.manager.transition.direction = "right"
        self.manager.current = "main"

    def add(self, object):
        possible_plant_ids = range(0, 4)

        # Find plant ids we can use
        for plant in plants:
            if plant["plant_id"] in possible_plant_ids:
                possible_plant_ids.remove(plant["plant_id"])
        plant_id = possible_plant_ids[0]

        # Add plant data to the list
        plant_image = "Graphics/plants/plant{0}.png".format(self.plant_type)
        plant_name = self.name_label.text
        owner = self.owner_label.text
        print  self.plant_type
        new_plant = {"plant_id": plant_id, "plant_image": plant_image, "name": plant_name, "owner": owner, "water": 50, "temp": 50, "fertilizer": 50, "last_watered": time.time(), "last_fertilized": time.time()}
        plants.append(new_plant)

        save_data()

        # Return the main menu, update plants
        self.manager.transition.direction = "right"
        self.manager.current = "main"
        self.mainMenu.update_plants()

    def reset(self):
        self.name_label.text = "Plant name"
        self.owner_label.text = "Owner name"
        self.plant_dropdown_btn.text = "Select a Plant Type"
        self.add_plant_btn.disabled = True

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        main = MainMenu(name="main")
        detail = Detail(name="detail", main=main)
        addPlant = AddPlant(name="add", main=main)

        main.addPlant = addPlant

        sm.add_widget(main)
        sm.add_widget(detail)
        sm.add_widget(addPlant)
        sm.current = "main"

        # Update temperature data every 3 seconds
        update_interval = 3
        Clock.schedule_interval(main.update, update_interval)

        return sm

if __name__ == '__main__':
    plants = load_data()
    save_data()
    MyApp().run()


