#
# JoystickController
#
from machine import Pin, I2C
from ads1x15 import ADS1115
from ble_server import BLEServer
from time import sleep

class JoystickController(BLEServer):
    def __init__(self, i2c, left, right, debug)-> None:
        BLEServer.__init__(self, 
                           name="JoystickController",
                           send_interval_ms=1000)
        self.left_button = Pin(left, Pin.IN, Pin.PULL_UP)
        self.right_button = Pin(right, Pin.IN, Pin.PULL_UP)
        self.adc = ADS1115(i2c, address=72, gain=1)
        self.rate = 4
        self.debug = debug
        
    def create_message(self)-> str:
        ch0 = self.adc.read(self.rate, 0)
        ch1 = self.adc.read(self.rate, 1)
        ch2 = self.adc.read(self.rate, 2)
        ch3 = self.adc.read(self.rate, 3)
        left_value = 1 - self.left_button.value()
        right_value = 1 - self.right_button.value()
        message = f'{ch0}, {ch1}, {ch2}, {ch3}, {left_value}, {right_value}'
        return message


if __name__ == '__main__':
    i2c = I2C(1, scl=27, sda=26, freq=200_000)
    joystickController = JoystickController(i2c=i2c, left=18, right=28, debug=True)
    joystickController.start()
    
