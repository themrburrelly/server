from django.shortcuts import render
from time import sleep
# check if the code is running on the raspberry pi
try:
    import RPi.GPIO as GPIO
    plataform = "rbpi"
    relay_pin = 9
    sensor_pin = 10
    # set up raspberry pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(sensor_pin, GPIO.BOTH, callback=sensor, bouncetime=150)
except:
    plataform = "mac"


def sensor(channel):
    if GPIO.input(sensor_pin):
        GPIO.output(relay_pin, GPIO.LOW)


def index(request, state=1):
    """Return the responce for the request."""
    if int(state) == 0 or GPIO.input(sensor_pin):
        if plataform == "rbpi":
            GPIO.output(relay_pin, GPIO.LOW)
        context = {"msg": "La llum esta oberta"}
    else:
        if plataform == "rbpi":
            GPIO.output(relay_pin, GPIO.HIGH)
        context = {"msg": "La llum esta apagada"}
    return render(request, 'family/index.html', context)

try:
    while True:
        sleep(1)

finally:
    GPIO.output(relay_pin, GPIO.HIGH)
