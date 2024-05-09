#
# JoystickController
#
from machine import Pin, ADC
from ble_server import BLEServer

class JoystickController(BLEServer):
    """Class for joystick control
    """
    
    def __init__(self, 
                 left_pin_nums, 
                 right_pin_nums
                 ):
        """Constructor
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
        """Create message
        """
        lx = self.convert(self.left_pins["x"].read_u16())
        ly = self.convert(self.left_pins["y"].read_u16())
        lb = self.left_pins["button"].value()
        rx = self.convert(self.right_pins["x"].read_u16())
        ry = self.convert(self.right_pins["y"].read_u16())
        rb = self.right_pins["button"].value()
        return f'{lx},{ly},{lb},{rx},{ry},{rb}'
    
    def convert(self, value):
        """Convert value from 0-
        """
        # TODO: Implement this function
        in_min = 0
        in_max = 65_535
        out_max = 100
        out_min = -100
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        
    
    
if __name__ == "__main__":
    joystickController = JoystickController((32, 33, 34), (35, 36, 37))
    joystickController.start()
