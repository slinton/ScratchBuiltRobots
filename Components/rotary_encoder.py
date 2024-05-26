#
# RotaryEncoder
# Version 0.1
#
from machine import Pin
from time import sleep
import uasyncio as asyncio

class RotaryEncoder:
    def __init__(self, sw, dt, clk)-> None:
        self.button = Pin(sw, Pin.IN, Pin.PULL_UP)
        self.direction = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.clock = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.previous = 1
        self.button_down = False
        
    def print_values(self)-> None:
        print(f'{self.clock.value()} {self.direction.value()} {self.button.value()}')
        
    async def update(self)-> None:
        current = self.clock.value()
        direct = self.direction.value()
        if current != self.previous:
            if current == 0:
                if direct == 0:
                    print('LEFT')
                else:
                    print('RIGHT')
            self.previous = current
            
        button_value = self.button.value()
        if button_value == 0 and not self.button_down:
            print('Button down')
            self.button_down = True
        elif button_value == 1 and self.button_down:
            print('Button up')
            self.button_down = False
            
    async def run_loop(self)-> None:
        while True:
            await self.update()
            #await asyncio.sleep_ms(100)
    
    def start(self)-> None:
        asyncio.run(self.run_loop())


if __name__ == '__main__':
    encoder = RotaryEncoder(sw=13, dt=14, clk=15)
    encoder.start()
    
        
             
