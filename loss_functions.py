import libdw.sm as sm
import time

class waterSM(sm.SM):
    ''' State machine for water '''
    startState = [0]
    def __init__(self):
        self.state = self.startState

    def getNextValues(self,state,last_water_time):
        water_interval = 5
        auto_water_interval = water_interval * 10

        if state == [0]:
            pump_command = 'stop'
            past_time = time.time() - last_water_time
            if past_time <= water_interval:
                nextState = [0]
            else:
                nextState = [1]

        elif state == [1]:
            pump_command = 'available'
            past_time = time.time() - last_water_time
            if past_time <= auto_water_interval and past_time > water_interval:
                nextState = [1]
            elif past_time > auto_water_interval:
                nextState = [2]
            else:
                nextState = [0]

        elif state == [2]:
            pump_command = 'auto_water'
            past_time = time.time() - last_water_time
            if past_time <= auto_water_interval and past_time > water_interval:
                nextState = [1]
            else:
                nextState = [0]
                
        return nextState,pump_command

class fertLossSM(sm.SM):
    ''' State machine for fertilizer '''

    startState = [0]

    def __init__(self):
        self.state = self.startState

    def getNextValues(self, state, last_water_time):
        fertilise_interval = 5 #604800
        auto_fertilise_interval = fertilise_interval * 10

        if state == [0]:
            pump_command = 'stop'
            past_time = time.time() - last_water_time
            if past_time <= fertilise_interval:
                nextState = [0]
            else:
                nextState = [1]

        elif state == [1]:
            pump_command = 'available'
            past_time = time.time() - last_water_time
            if past_time <= auto_fertilise_interval and past_time > fertilise_interval:
                nextState = [1]
            elif past_time > auto_fertilise_interval:
                nextState = [2]
            else:
                nextState = [0]

        elif state == [2]:
            pump_command = 'auto_fertilise'
            past_time = time.time() - last_water_time
            if past_time <= auto_fertilise_interval and past_time > fertilise_interval:
                nextState = [1]
            else:
                nextState = [0]
        return nextState, pump_command
