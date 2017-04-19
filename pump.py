import RPi.GPIO as GPIO
import time


def pump(pumpnumber,duration):
    GPIO.setmode(GPIO.BCM)

    in1_pin = 5 #waterpump #pump1
    in2_pin = 17
    in3_pin = 23
    in4_pin = 26
    en = 18

    GPIO.setup(en, GPIO.OUT)
    GPIO.output(en, GPIO.HIGH)
    
    if pumpnumber == 1: #waterpump
        GPIO.setup(in1_pin, GPIO.OUT)
        p1=GPIO.PWM(in1_pin, 150)

        p1.start(100)
        time.sleep(duration)
        p1.stop()
    elif pumpnumber == 2:
        GPIO.setup(in2_pin, GPIO.OUT)
        p2=GPIO.PWM(in2_pin, 150)

        p2.start(100)
        time.sleep(duration)
        p2.stop()
    elif pumpnumber == 3:
        GPIO.setup(in3_pin, GPIO.OUT)
        p3=GPIO.PWM(in3_pin, 150)

        p3.start(100)
        time.sleep(duration)
        p3.stop()
    elif pumpnumber == 4:
        GPIO.setup(in4_pin, GPIO.OUT)

        p4=GPIO.PWM(in4_pin, 150)

        p4.start(50)
        time.sleep(duration)
        p4.stop()
    GPIO.cleanup()        
    
#try:
#    while 1:
#        for dc in range(0, 101, 5):
#            p1.ChangeDutyCycle(dc)
#            time.sleep(0.1)
#
#except KeyboardInterrupt:
#    pass
