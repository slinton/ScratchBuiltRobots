#
# DistanceSensor
#
from machine import Pin
from time import sleep_us, ticks_us

class DistanceSensor:
    """Class to get distance to features in front """
    
    def __init__(self, trigger, echo)-> None:
        """_summary_

        Args:
            trigger (int): pin number for trigger
            echo (int): pin number for echo
        """
        
        self._trigger_pin = Pin(trigger, Pin.OUT)
        self._echo_pin = Pin(echo, Pin.IN)
        
    def get_distance_cm(self)-> float:
        """Get distance in cm

        Returns:
            float: distance in cm
        """

        # Trigger the ultrasonic pulse
        self._trigger_pin.value(0)
        sleep_us(2)
        self._trigger_pin.value(1)
        sleep_us(10)
        self._trigger_pin.value(0)
        
        # Start timing the signal from the echo pin
        while self._echo_pin.value() == 0:
            pass
        t1 = ticks_us()
        
        # Finish timing the signal from the echo pin
        while self._echo_pin.value() == 1:
            pass
        t2 = ticks_us()
        
        # Echo pin signal duration indicates time of flight
        return (t2 - t1) * 0.034 / 2
