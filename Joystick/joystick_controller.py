#
# JoystickController
#
from machine import Pin, ADC
from time import sleep
from ble_server import BLEServer

class JoystickController(BLEServer):
    """Class for joystick controller. The controller has two joysticks, each with x, y 
    and button. It is up to the client to interpret the data. The data is sent as a string.
    """
    
    def __init__(self, 
                 left_pin_nums, 
                 right_pin_nums,
                 debug:bool=False
                 )->None:
        """Initialize JoystickController
        Args:
            left_pin_nums: Tuple with pin numbers for left joystick. The tuple should contain
                           three integers, where the first two are the ADC pins for x and y
                           and the third is the button pin.
            right_pin_nums: Tuple with pin numbers for right joystick. The tuple should contain
                            three integers, where the first two are the ADC pins for x and y
                            and the third is the button pin.
            debug: If True, print debug information
        """
        BLEServer.__init__(self, 
                           name="JoystickController",
                           send_interval_ms=100)
        
        self.left_pins = { "x": ADC(left_pin_nums[0]),
                           "y": ADC(left_pin_nums[1]),
                           "button": Pin(left_pin_nums[2], Pin.IN, Pin.PULL_UP)}
        
        self.right_pins = { "x": ADC(right_pin_nums[0]),
                            "y": ADC(right_pin_nums[1]),
                            "button": Pin(right_pin_nums[2], Pin.IN, Pin.PULL_UP)}
        
    def create_message(self)->str:
        """Create message with joystick data
        """
        lx = self.convert(self.left_pins["x"].read_u16())
        ly = self.convert(self.left_pins["y"].read_u16())
        lb = self.left_pins["button"].value()
        rx = self.convert(self.right_pins["x"].read_u16())
        ry = self.convert(self.right_pins["y"].read_u16())
        rb = self.right_pins["button"].value()
        message = f'{lx},{ly},{lb},{rx},{ry},{rb}'
        if self.debug:
            print(message)
        return message
    

if __name__ == "__main__":
    joystickController = JoystickController((16, 17, 18), (28, 27, 26), debug=True)
    while True:
        message = joystickController.create_message()
        print(message)
        sleep(0.1)
