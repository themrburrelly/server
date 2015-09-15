import RPi.GPIO as GPIO
from time import sleep
from pymongo import MongoClient
import Adafruit_DHT as dht

# SETUP
# ---------------------------------
# Database setup
client = MongoClient()
db = client.db
outputs = db.family_outputs
inputs = db.family_inputs
settings = db.family_settings

# Raspberry Setup
GPIO.setmode(GPIO.BCM)
for pin in range(2, 10):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

motion_sensor_pin = setting.find_one({"name": "motion_sensor_pin"})['value']
GPIO.setup(motion_sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# LOOP
# ---------------------------------
count = 0
while True:
    if GPIO.input(motion_sensor_pin):
        count = 0
        outputs.update({'name': 'right_light'}, {"$set": {'state': 1}}, upsert=False)
    if count == settings.find_one({"name": "motion_sensor_timer"})['value']:
        outputs.update({'name': 'right_light'}, {"$set": {'state': 0}}, upsert=False)
    for output in outputs.find():
        if output['state'] == 0:
            GPIO.output(output['pin'], GPIO.HIGH)
        else:
            GPIO.output(output['pin'], GPIO.LOW)
    if count < settings.find_one({"name": "motion_sensor_timer"})['value']+1:
        count += 1
    h, t = dht.read_retry(dht.DHT22, inputs.find({'name': 'temperature'})['pin'])
    inputs.update({'name': 'temperature'}, {"$set": {'metadata': t}}, upsert=False)
    inputs.update({'name': 'humidity'}, {"$set": {'metadata': h}}, upsert=False)
    sleep(1)
