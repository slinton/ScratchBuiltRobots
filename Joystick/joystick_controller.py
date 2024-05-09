#
# JoystickController
#
from machine import Pin, ADC
from time import sleep
from ble_server import BLEServer

class JoystickController(BLEServer):
    """Class for joystick controller. The controller as two joysticks, each with x, y 
    and button.
    """
    
    def __init__(self, 
                 left_pin_nums, 
                 right_pin_nums,
                 debug:bool=False
                 )->None:
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
    
    # TODO
    def convert(self, input:int)->int:
        """Convert value from 0-
        """
        # TODO: Implement this function
        input_min = 0
        input_max = 65_535
        output_min = -100
        output_max = 100
        output = (input - input_min) * (output_max - output_min) / (input_max - input_min) + output_min
        if self.debug:
            print(f'input: {input}, output: {output}')
        return output
    
    # TODO
    def zero(self)->None:
        """Zero joystick values
        """
        print('Zeroing joystick...', end='')
        lx0 = 0
        ly0 = 0
        rx0 = 0
        ry0 = 0
        
        for _ in range(10):
            lx0 += self.left_pins["x"].read_u16()
            ly0 += self.left_pins["y"].read_u16()
            rx0 += self.right_pins["x"].read_u16()
            ry0 += self.right_pins["y"].read_u16()
            sleep(0.1)
            
        lx0 //= 10
        ly0 //= 10
        rx0 //= 10
        ry0 //= 10
        print(f' Done: {lx0}, {ly0}, {rx0}, {ry0}')
            
            
    
if __name__ == "__main__":
    joystickController = JoystickController((32, 33, 34), (35, 36, 37))
    joystickController.start()
