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
from kivy.uix.screenmanager import Screen

screen_width = 800
screen_height = 500

class ImageButton(ButtonBehavior, Image):
    pass

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
        self.water_bar.value = loss_functions.calculate_water_loss(self.plant["water"], self.plant["last_watered"])

        # adjust fertilizer based on last fertilizer level
        self.fertilizer_bar.value = loss_functions.calculate_fertilizer_loss(self.plant["fertilizer"], self.plant["last_fertilized"])

    def update_data(self): 
        ''' update data on water or fertilization of plant '''

        self.temperature_bar.value = self.plant["temp"]
        self.water_bar.value = self.plant["water"]
        self.fertilizer_bar.value = self.plant["fertilizer"]

    def water(self, object):
        ''' water plants '''
        
        # turn on water pump for 2 seconds
        pump.pump(1, 2)

        # update plant stats
        self.plant["water"] += 5
        self.plant["last_watered"] = time.time()
        self.update_data()
        save_data()

        # self.water_btn.disabled = True

    def fertilize(self, object):
        # turn on fertilizer pump for the appropriate plant (id + 2, as pump 1 is the water pump)
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

        self.manager.transition.direction = "right"
        self.manager.current = "main"
        self.mainMenu.update_plants()
        print plants

    def back(self, object):
        self.manager.transition.direction = "right"
        self.manager.current = "main"
