#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17
LED = 27
 
#set GPIO direction (IN / OUT)
#GPIO.setmode(GPIO.BOARD) 
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT) 

# 50Hz PWM Frequency  
pwm_led = GPIO.PWM(LED, 50)  
# Full Brightness, 100% Duty Cycle  
pwm_led.start(0) 

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
	    #if dist < 20:	    
	    #	GPIO.output(GPIO_TRIGGER, True)
 
            print ("Measured Distance = %.1f cm" % dist)
            if dist < 100:           
                pwm_led.ChangeDutyCycle(100 - dist)   
            if dist > 100:
                pwm_led.ChangeDutyCycle(0)
	    time.sleep(0.2)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

