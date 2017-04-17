import libdw.sm as sm
import time
class loss_functions(sm.SM):
    startState = [0]
    def __init__(self):
        self.state = self.startState

    def getNextValues(self,state,last_water_time):
        water_interval = 5
        auto_water_interval = water_interval * 100

        if state == [0]:
            pump_command = 'stop'
            past_time = time.time() - last_water_time
            if past_time <= water_interval:
                nextState = [0]
            else:#elif past_time >= water_interval:
                nextState = [1]

        elif state == [1]:
            pump_command = 'available'
            past_time = time.time() - last_water_time
            if past_time <= auto_water_interval and past_time > water_interval:
                nextState = [1]
            elif past_time > auto_water_interval:
                nextState = [2]
            else:#elif past_time <= water_interval:
                nextState = [0]

        elif state == [2]:
            pump_command = 'auto_water'
            past_time = time.time() - last_water_time
            if past_time <= auto_water_interval and past_time > water_interval:
                nextState = [1]
            else:#elif past_time <= water_interval:
                nextState = [0]
                
        return nextState,pump_command


#    def calculate_water_loss(water, last_water_time):
#	    #''' Takes in the previous water level, and the last time the plant was watered, and calculate its new estimated water level '''
#	    time_passed = time.time() - last_water_time
#	    water = math.exp(-time_passed/10000) * water
#	    print(water)
#	    return water
#
#    def calculate_fertilizer_loss(fertilizer, last_fertilized_time):
#        #''' Takes in the previous fertilizer level, and the last time the plant was fertilized, and calculate its new estimated fertilizer level '''
#        time_passed = time.time() - last_fertilized_time
#        fertilizer = math.exp(-time_passed/10000) * fertilizer
#        print(fertilizer)
#        return fertilizer

class loss_functions2(sm.SM):
    startState = [0]

    def __init__(self):
        self.state = self.startState

    def getNextValues(self, state, last_water_time):
        fertilise_interval = 5 #604800
        auto_fertilise_interval = fertilise_interval * 100

        if state == [0]:
            pump_command = 'stop'
            past_time = time.time() - last_water_time
            if past_time <= fertilise_interval:
                nextState = [0]
            else:#elif past_time >= fertilise_interval:
                nextState = [1]

        elif state == [1]:
            pump_command = 'available'
            past_time = time.time() - last_water_time
            if past_time <= auto_fertilise_interval and past_time > fertilise_interval:
                nextState = [1]
            elif past_time > auto_fertilise_interval:
                nextState = [2]
            else:#elif past_time <= fertilise_interval:
                nextState = [0]

        elif state == [2]:
            pump_command = 'auto_fertilise'
            past_time = time.time() - last_water_time
            if past_time <= auto_fertilise_interval and past_time > fertilise_interval:
                nextState = [1]
            else:#elif past_time <= fertilise_interval:
                nextState = [0]
        return nextState, pump_command

# def calculate_water_loss(water, last_water_time):
#	    #''' Takes in the previous water level, and the last time the plant was watered, and calculate its new estimated water level '''
#	    time_passed = time.time() - last_water_time
#	    water = math.exp(-time_passed/10000) * water
#	    print(water)
#	    return water
#
#    def calculate_fertilizer_loss(fertilizer, last_fertilized_time):
#        #''' Takes in the previous fertilizer level, and the last time the plant was fertilized, and calculate its new estimated fertilizer level '''
#        time_passed = time.time() - last_fertilized_time
#        fertilizer = math.exp(-time_passed/10000) * fertilizer
#        print(fertilizer)
#        return fertilizer

