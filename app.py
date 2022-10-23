import time
import wiringpi
import dictdiffer
import requests
import copy
import json
import os

PIN_BASE = 65
BASE_URL = 'http://localhost:9000/'
AUTH_TOKEN = os.environ['AUTH_TOKEN'] 
HEADERS = {
    "Authorization": "Token " + AUTH_TOKEN,
    "Content-Type": "application/json",
}
PIN_MAPPING = {
    "0x20":{
        "PA0":PIN_BASE,
        "PA1":PIN_BASE + 1,
        "PA2":PIN_BASE + 2,
        "PA3":PIN_BASE + 3,
        "PA4":PIN_BASE + 4,
        "PA5":PIN_BASE + 5,
        "PA6":PIN_BASE + 6,
        "PA7":PIN_BASE + 7,
        "PB0":PIN_BASE + 8,
        "PB1":PIN_BASE + 9,
        "PB2":PIN_BASE + 10,
        "PB3":PIN_BASE + 11,
        "PB4":PIN_BASE + 12,
        "PB5":PIN_BASE + 13,
        "PB6":PIN_BASE + 14,
        "PB7":PIN_BASE + 15
    }
}

def set_pin_mode(i2c_adress, pin_name, pin_mapping):
    try:
        pin = pin_mapping[i2c_adress][pin_name]
        wiringpi.pinMode(pin, 0)
        wiringpi.pullUpDnControl(pin, 2)
        return pin
    except:
        return

def update_occupied_state(id,state):
    URL = BASE_URL + 'places/' + str(id)
    request_body = {
        "occupied": state
    }
    data=json.dumps(request_body)
    requests.request("PATCH",URL,headers=HEADERS,data=data)

response = requests.request("GET",BASE_URL + 'places/',headers=HEADERS)
response_json = response.json()

wiringpi.wiringPiSetup()

for adress in PIN_MAPPING:
    wiringpi.mcp23017Setup(PIN_BASE,int(adress, 0))

previous_state = {}
current_state = {}

for place in response_json:
    pin = set_pin_mode(place['i2c_adress'],place['pin_name'],PIN_MAPPING)

    previous_state[place['id']] = {
        "pin": pin,
        "state": False
    }
    current_state[place['id']] = {
        "pin": pin,
        "state": False
    }

print("Awaiting input..")

while True:
    time.sleep(0.1)
    previous_state = copy.deepcopy(current_state)

    for gpio in current_state:
        current_state[gpio]['state'] = not wiringpi.digitalRead(current_state[gpio]['pin'])

    if previous_state != current_state:
        for diff in list(dictdiffer.diff(previous_state, current_state)):
            id = str(diff[1][0])
            state = str(diff[2][1])
            update_occupied_state(id,state)

