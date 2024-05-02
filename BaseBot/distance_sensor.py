#
# DistanceSensor
#
from machine import Pin
from time import sleep_us, ticks_us

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
        
    def get_distance_cm(self)-> float:
        """Get distance in cm

        Returns:
            float: distance in cm
        """
        
        self._trigger_pin.value(0)
        sleep_us(2)
        self._trigger_pin.value(1)
        sleep_us(10)
        self._trigger_pin.value(0)
        
        # Capture time of start of pulse
        while self._echo_pin.value() == 0:
            pass
        t1 = ticks_us()
        
        # Capture time of end of pulse
        while self._echo_pin.value() == 1:
            pass
        t2 = ticks_us()
        
        # Pulse duration indicates time of flight
        return (t2 - t1) * 0.034 / 2
