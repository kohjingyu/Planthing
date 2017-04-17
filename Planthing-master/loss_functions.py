import libdw.sm as sm
import time
class loss_functions(sm.SM):
    startState = [0]
    def __init__(self):
        self.time = time.time()
        self.state = self.startState

    def getNextValues(self,state,last_water_time):
        if state == [0]:
            pump_command = 'stop'
            past_time = self.time -last_water_time
            if past_time <= 43200:
                nextState = [0]
            elif past_time >= 43200:
                nextState = [1]

        elif state == [1]:
            pump_command = 'available'
            past_time = self.time - last_water_time
            if past_time <= 86400 and past_time > 43200:
                nextState = [1]
            elif past_time > 86400:
                nextState = [2]
            elif past_time <= 43200:
                nextState = [0]

        elif state == [2]:
            pump_command = 'auto_water'
            past_time = self.time - last_water_time
            if past_time <= 86400 and past_time > 43200:
                nextState = [1]
            elif past_time <= 43200:
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
        self.time = time.time()
        self.state = self.startState

    def getNextValues(self, state, last_water_time):
        if state == [0]:
            pump_command = 'stop'
            past_time = self.time - last_water_time
            if past_time <= 604800:
                nextState = [0]
            elif past_time >= 604800:
                nextState = [1]

        elif state == [1]:
            pump_command = 'available'
            past_time = self.time - last_water_time
            if past_time <= 1209600 and past_time > 604800:
                nextState = [1]
            elif past_time > 1209600:
                nextState = [2]
            elif past_time <= 604800:
                nextState = [0]

        elif state == [2]:
            pump_command = 'auto_fertilise'
            past_time = self.time - last_water_time
            if past_time <= 1209600 and past_time > 604800:
                nextState = [1]
            elif past_time <= 604800:
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

