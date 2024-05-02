#
# DistanceSensor
#
from machine import Pin
from time import sleep_us

class DistanceSensor:
    """Class to get distance to features in front """
    def __init__(self, trigger_pin_num, echo_pin_num)-> None:
        """_summary_

        Args:
            trigger_pin_num (int): pin number for trigger
            echo_pin_num (int): pin number for echo
        """
        
        self._trigger_pin = Pin(trigger_pin_num, Pin.OUT)
        self._echo_pin = Pin(echo_pin_num, Pin.IN)
