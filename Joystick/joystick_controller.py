#
# JoystickController
#
from machine import Pin, I2C
from ads1x15 import ADS1115
from ble_server import BLEServer
from time import sleep

class JoystickController(BLEServer):
    def __init__(self, i2c, left: int, right: int, led: int=None, debug: bool = False)-> None:
        BLEServer.__init__(self, 
                           name="JoystickController",
                           send_interval_ms=1000)
        self.left_button = Pin(left, Pin.IN, Pin.PULL_UP)
        self.right_button = Pin(right, Pin.IN, Pin.PULL_UP)
        self.led = None if led == None else Pin(led, Pin.OUT)
        self.adc = ADS1115(i2c, address=72, gain=1)
        self.rate = 4
        self.debug = debug
        
    def create_message(self)-> str:
        ch0 = hex(self.adc.read(self.rate, 0))[2:]
        ch1 = hex(self.adc.read(self.rate, 1))[2:]
        ch2 = hex(self.adc.read(self.rate, 2))[2:]
        ch3 = hex(self.adc.read(self.rate, 3))[2:]
        left_value = 1 - self.left_button.value()
        right_value = 1 - self.right_button.value()
        button_code = left_value + 2 * right_value
        message = f'{ch0},{ch1},{ch2},{ch3},{button_code}'
        return message
    
    def show_connected(self, connected: bool)-> None:
        if self.led == None:
            return
        if connected:
            self.led.value(1)
        else:
            self.led.value(0)


if __name__ == '__main__':
    i2c = I2C(1, scl=27, sda=26, freq=200_000)
    joystickController = JoystickController(i2c=i2c, left=18, right=28, led=1, debug=True)
    joystickController.start()
    

