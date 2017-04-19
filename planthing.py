import sensors
import pump

from loss_functions import waterSM
from loss_functions import fertLossSM

import log_functions

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
import time
import math

screen_width = 800
screen_height = 500

brown_color = Color(0.7059, 0.6549, 0.5373)
dark_brown_color = Color(0.3608, 0.2863, 0.251)
brown_button_background = [0.6784, 0.5804, 0.5333, 1]
light_brown_background_color = [0.5216, 0.5843, 0.4039, 1]

# Initialize state machines
waterSM = waterSM()
waterSM.start()

fertSM1 = fertLossSM()
fertSM1.start()
fertSM2 = fertLossSM()
fertSM2.start()
fertSM3 = fertLossSM()
fertSM3.start()
fertSM4 = fertLossSM()
fertSM4.start()
fertSM = [fertSM1, fertSM2, fertSM3, fertSM4]

class ImageButton(ButtonBehavior, Image):
    ''' Custom class for image buttons '''
    pass

class MainMenu(Screen): 
    ''' Main Menu of the application '''

    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)

        self.addPlant = None # This will be set to the addPlants Screen later on
        self.pump_command_for_water='stop'
        self.pump_command_for_fertiliser=['stop'] * len(plants)

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
        layout_left.canvas.add(brown_color)
        layout_left.canvas.add(Rectangle(pos=(0,0),size=(screen_width/2,screen_height),orientation='horizontal'))
        layout_left.add_widget(Label(text="[b][size=42][color=#5C4940]PLANTHING[/color][/size][/b]", 
            markup=True,
            size_hint=(.5, .5), 
            pos_hint={'x':.25, 'y':.4}))

        # reading humidity and temp using sensors.get_humidity_temp()
        temp_humidity = sensors.get_humidity_temp() #{'temperature': 0, 'humidity': 0 }

        temperature_string = "[b][size=18][color=#5C4940]Temperature: {0} C[/color][/size][/b]".format(temp_humidity["temperature"])
        humidity_string = "[b][size=18][color=#5C4940]Humidity: {0}%[/color][/size][/b]".format(temp_humidity["humidity"])

        # temperature display
        self.temperature_widget = Label(text=temperature_string, 
            markup=True, 
            size_hint=(.5, .05), 
            pos_hint={'x':.25, 'y':0.2})
        layout_left.add_widget(self.temperature_widget)
        
        # humidity display
        self.humidity_widget = Label(text=humidity_string, 
            markup=True, 
            size_hint=(.5, .05), 
            pos_hint={'x':.25, 'y':0.15})
        layout_left.add_widget(self.humidity_widget)
        
        # four plants on display
        layout_right = FloatLayout(cols=2, 
            row_force_default=True, 
            row_default_height=screen_height/2)
        layout_right.canvas.add(Color(1, 1, 1))
        layout_right.canvas.add(Rectangle(pos=(screen_width/2,0),
            size=(screen_width/2,screen_height),
            orientation='horizontal'))

        # initialize the plants
        plant_size = 0.3 # plant image width is 30% of width
        plant_padding = (0.5 - plant_size)/2 # total space for each plant is 50%
        positions = [(plant_padding, 0.5 + plant_padding), (0.5 + plant_padding, 0.5 + plant_padding), (plant_padding, plant_padding), (0.5 + plant_padding, plant_padding)]

        total_plants = 4
        for i in range(total_plants):
            # Position of this button
            (x, y) = positions[i]

            # Add brown background for each plant
            layout_right.canvas.add(brown_color)
            layout_right.canvas.add(Rectangle(pos=(screen_width/2 + (x-0.035) * screen_width/2, (y-0.08) * screen_height),
                size=(150, 210),
                orientation='horizontal'))

            # If plant exists, add it
            if i < len(plants):
                plant = plants[i]

                # each plant icon is a button
                plant_button = ImageButton(source=plant["plant_image"], 
                    on_press=partial(self.view_detail,
                    plant_id=plant["plant_id"]),
                    size_hint=(plant_size, plant_size), 
                    pos_hint={'x': x, 'y': y})

                layout_right.add_widget(plant_button)

                # adding in names of plants
                plant_text = "[b][color=#5C4940]{0}[/color][/b]".format(plant['name'])
                label_height = 0.05
                label_offset = 0.09
                layout_right.add_widget(Label(text=plant_text, 
                    markup=True, 
                    size_hint=(plant_size, label_height), 
                    pos_hint={'x': x, 'y': y - plant_size/2 + label_offset}))
            else:
                # Plant doesn't exist, allow users to add new plant
                plant_button = Button(text="[b][size=18][color=#5C4940]Add Plant[/color][/size][/b]", 
                    markup=True,
                    background_color=[0,0,0,0],
                    on_press=self.add_plant,
                    size_hint=(plant_size, plant_size), 
                    pos_hint={'x': x, 'y': y - 0.035})
                layout_right.add_widget(plant_button)
                plant_background = Rectangle(pos=(x, y), 
                    size=(plant_size,plant_size), 
                    orientation='horizontal')
                layout_right.canvas.add(plant_background)

        # add left and right screens
        grid_layout.add_widget(layout_left)
        grid_layout.add_widget(layout_right)

        self.add_widget(grid_layout)
        self.grid_layout = grid_layout

    def add_plant(self, *args):
        ''' Move to the add plant screen '''
        self.manager.transition.direction = "left"
        self.manager.current = "add"

        self.addPlant.reset()

    def update(self, *args):
        ''' Update data from all sensors '''
        temp_humidity = sensors.get_humidity_temp() #{'temperature': 0, 'humidity': 0 }

        # formatting humidity and temperature text
        self.temperature_widget.text = "[b][size=18][color=#5C4940]Temperature: {0} C[/color][/size][/b]".format(temp_humidity["temperature"])
        self.humidity_widget.text = "[b][size=18][color=#5C4940]Humidity: {0}%[/color][/size][/b]".format(temp_humidity["humidity"])

        # Log the humidity and temperature values to file
        log_functions.log_data()

        last_water_time = plants[0]["last_watered"]
        self.pump_command_for_water = waterSM.step(last_water_time)
        if self.pump_command_for_water == 'auto_water':
            pump.pump(1,5)
            plants[0]["water"] += 5
            plants[0]["water"] = min(plants[0]["water"], 100)
            plants[0]["last_watered"] = time.time()
            log_functions.save_data(plants)

        # Check fertilizer SM in the case of auto fertilization
        for i in range(len(plants)):
            last_fertilized = plants[i]["last_fertilized"]
            self.pump_command_for_fertiliser[i] = fertSM[i].step(last_fertilized)
            if self.pump_command_for_fertiliser[i] == 'auto_fertilise':
                pump_number = i + 2
                pump.pump(pump_number, 1)
                # update plant stats
                plants[i]["fertilizer"] += 5
                plants[i]["fertilizer"] = min(plants[i]["fertilizer"], 100)
                plants[i]["last_fertilized"] = time.time()
                log_functions.save_data(plants)

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
        left_layout.canvas.add(brown_color)
        left_layout.canvas.add(Rectangle(pos=(0,0),
            size=(screen_width/2,screen_height),
            orientation='horizontal'))

        # plant image
        plant_size = 0.6
        self.plant_image = Image(source="", 
            size_hint=(plant_size, plant_size), 
            pos_hint={'x': (1 - plant_size)/2, 'y': (1 - plant_size)/2})
        left_layout.add_widget(self.plant_image)

        left_layout.add_widget(Button(text="Back", 
            on_press=self.back,
            background_color=brown_button_background, 
            size_hint=(1, .05), 
            pos_hint={'x': 0, 'y': 0.95}))

        # plant name and owner labels
        self.plant_name_label = Label(text="[b][size=18][color=#5C4940]Name: Plant[/color][/size][/b]", 
            markup=True, 
            size_hint=(1, 0.1), 
            pos_hint={'x': 0, 'y': 0.05})
        self.owner_name_label = Label(text="[b][size=18][color=#5C4940]Owned By: Person[/color][/size][/b]", 
            markup=True, 
            size_hint=(1, 0.1), 
            pos_hint={'x': 0, 'y': 0})
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

        self.water_btn = ImageButton(source="Graphics/water_btn.png", 
            size_hint=(btn_size, btn_size), 
            pos_hint={'x': 0.5 - btn_gap/2 - btn_size, 'y': 0.2}, 
            on_press=self.water)
        self.fertilizer_btn = ImageButton(source="Graphics/fertilizer_btn.png", 
            size_hint=(btn_size, btn_size), 
            pos_hint={'x': 0.5 + btn_gap/2, 'y': 0.2}, 
            on_press=self.fertilize)

        right_layout.add_widget(self.water_btn)
        right_layout.add_widget(self.fertilizer_btn)

        progress_start_y = 0.8
        progress_bar_height = 0.1

        # temperature bar
        right_layout.add_widget(ImageButton(source="Graphics/light_icon.png",
            size_hint=(0.1, progress_bar_height), 
            pos_hint={'x': 0.2, 'y': progress_start_y}))
        self.temperature_bar = ProgressBar(max=100, 
            size_hint=(0.3, progress_bar_height), 
            pos_hint={'x': 0.5, 'y': progress_start_y})
        right_layout.add_widget(self.temperature_bar)

        # water bar
        right_layout.add_widget(ImageButton(source="Graphics/water_icon.png",
            markup=True, 
            size_hint=(0.1, progress_bar_height), 
            pos_hint={'x': 0.2, 'y': progress_start_y - progress_bar_height}))
        self.water_bar = ProgressBar(max=100, 
            size_hint=(0.3, progress_bar_height), 
            pos_hint={'x': 0.5, 'y': progress_start_y - progress_bar_height})
        right_layout.add_widget(self.water_bar)

        # fertilizer bar
        right_layout.add_widget(ImageButton(source="Graphics/fertilizer_icon.png", 
            markup=True, 
            size_hint=(0.1, progress_bar_height), 
            pos_hint={'x': 0.2, 'y': progress_start_y - 2*progress_bar_height}))
        self.fertilizer_bar = ProgressBar(max=100, 
            size_hint=(0.3, progress_bar_height), 
            pos_hint={'x': 0.5, 'y': progress_start_y - 2*progress_bar_height})
        right_layout.add_widget(self.fertilizer_bar)

        # delete button
        right_layout.add_widget(ImageButton(source="Graphics/delete.png", on_press=self.remove_plant, 
            markup=True, 
            size_hint=(0.25, progress_bar_height), 
            pos_hint={'x': 0.5 - 0.25/2, 'y': 0.05}))

        grid_layout.add_widget(left_layout)
        grid_layout.add_widget(right_layout)
        self.add_widget(grid_layout)

    def update(self, plant_id):
        ''' grabbing plant data from dictionary as user interacts  and every 3 seconds'''
        for plant in plants:
            if plant["plant_id"] == plant_id:
                self.plant = plant
                break

        self.plant_name_label.text = "[size=18][color=#5C4940][b]Name:[/b] {0}[/color][/size]".format(self.plant["name"])
        self.owner_name_label.text = "[size=18][color=#5C4940][b]Owned by:[/b] {0}[/color][/size]".format(self.plant["owner"])

        # update plant image
        self.plant_image.source = self.plant["plant_image"]

        # update temperature to current temp
        self.temperature_bar.value = self.plant["temp"]

    def update_data(self): 
        ''' update data on water or fertilization of plant '''
        self.temperature_bar.value = self.plant["temp"]
        self.water_bar.value = plants[0]["water"]
        self.fertilizer_bar.value = self.plant["fertilizer"]

    def water(self, object):
        ''' water plants '''
        print("Trying to water")
        
        # turn on water pump for 2 seconds
        if self.mainMenu.pump_command_for_water == 'available':
            print ("Watering")
            pump.pump(1, 5)
            # update plant stats
            plants[0]["water"] += 5
            plants[0]["water"] = min(plants[0]["water"], 100)
            plants[0]["last_watered"] = time.time()
            self.update_data()

            # update plant stats
            log_functions.save_data(plants)

    def fertilize(self, object):
        # turn on fertilizer pump for the appropriate plant (id + 2, as pump 1 is the water pump)
        plant_id = self.plant["plant_id"] - 1
        # self.mainMenu.pump_command_for_fertiliser[plant_id] = fertSM[plant_id].step(self.plant["last_fertilized"])
        if self.mainMenu.pump_command_for_fertiliser[plant_id] == 'available':
            print ("Fertilizer")
            pump_number = self.plant["plant_id"] + 2
            print pump_number
            pump.pump(pump_number, 1)
            # update plant stats
            self.plant["fertilizer"] += 5
            self.plant["fertilizer"] = min(self.plant["fertilizer"], 100)

            self.plant["last_fertilized"] = time.time()
            self.update_data()
            log_functions.save_data(plants)

        # self.fertilizer_btn.disabled = True

    def remove_plant(self, object):
        # Delete current plant
        plants.remove(self.plant)

        log_functions.save_data(plants)

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
        
        # main layout is made of 2 columns
        grid_layout = BoxLayout(orientation='horizontal')
        grid_layout.canvas.add(brown_color)
        grid_layout.canvas.add(Rectangle(size=(screen_width/2,screen_height)))

        # back button takes up left side of screen
        back_button = BoxLayout()
        back_button.add_widget(Button(text="[size=32][color=#5C4940]BACK[/color][/size]", 
            markup=True,
            on_press=self.back, 
            background_color=brown_button_background))

        grid_layout.add_widget(back_button)

        # adding plant details takes up right side of screen
        add_plant_det = BoxLayout(orientation='vertical')

        # giving the plant a name
        self.name_label = TextInput(text="Plant name", )
        add_plant_det.add_widget(self.name_label)
        
        # indicating owner
        self.owner_label = TextInput(text="Owner name")
        add_plant_det.add_widget(self.owner_label)
                
        self.plant_type = 0 # default no plant type selected
        self.plant_types = ["Parsley", "Cactus", "Basil"] # available types of plants 
        
        # making the dropdown button
        plant_type_dropdown = DropDown()

        # Add different plant options to the dropdown
        for plant_type in self.plant_types:
            btn = Button(text=plant_type,
                        size_hint_y=None, 
                        background_color=light_brown_background_color,
                        height=40)
            btn.bind(on_release=lambda btn: plant_type_dropdown.select(btn.text)) 
            plant_type_dropdown.add_widget(btn) # adding button in dropdown

        self.plant_dropdown_btn = Button(text='[size=18][color=#5C4940]Select a Plant Type[/color][/size]', 
            markup=True,
            size_hint=(1, None),
            background_color=brown_button_background)
        self.plant_dropdown_btn.bind(on_release=plant_type_dropdown.open)

        plant_type_dropdown.bind(on_select=self.selectPlantType) # On selection of plant type, set button text and enable add plant button

        add_plant_det.add_widget(self.plant_dropdown_btn)

        # add plant button is disabled by default
        self.add_plant_btn = Button(text="[b][size=18][color=#FFF]Add Plant[/color][/size][/b]", 
            markup=True,
            background_color=[0.4039, 0.5843, 0.4667, 1],
            on_press=self.add, 
            disabled=True)
        add_plant_det.add_widget(self.add_plant_btn)

        grid_layout.add_widget(add_plant_det)

        self.add_widget(grid_layout)

    def selectPlantType(self, object, btn_text):
        setattr(self.plant_dropdown_btn, 'text', btn_text)
        self.plant_type = btn_text # setting button text
        self.add_plant_btn.disabled = False # enabling add plant button

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

        log_functions.save_data(plants)

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
        update_interval = 5

        # Initialize update first
        main.update()
        Clock.schedule_interval(main.update, update_interval)

        return sm

if __name__ == '__main__':
    plants = log_functions.load_data()
    log_functions.save_data(plants)
    MyApp().run()


