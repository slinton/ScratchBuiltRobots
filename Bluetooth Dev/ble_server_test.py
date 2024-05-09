#
# BLE Server Test
#
import uasyncio as asyncio
from ble_server import BLEServer
from machine import Pin
from time import sleep
import random

button = Pin(0, Pin.IN, Pin.PULL_UP)

def button_pressed():
    message = 'on' if random.randint(0,1) == 1 else 'off'
    # message = 'off' if button.value() == 1 else 'on'
    print(f'Send message {message}')
    return message


while True:
    server = BLEServer(
            name='BLE Test',
            create_message_func=button_pressed,
            send_interval_ms=1000)
    server.start()
