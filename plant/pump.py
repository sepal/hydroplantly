import imp
from grow.pump import Pump

from plant.model import PumpSettings, WateringSettings
import time

class PumpControl:
    __pump: Pump
    __settings: PumpSettings

    def __init__(self, channel: int, settings: PumpSettings) -> None:
        self.__settings = settings
        self.__pump = Pump(channel)
        self.__setSp

    def water(self):
        for i in range(self.__settings.pump_repeat):
            self.__pump.dose(self.__settings.pump_speed, 
                self.__settings.pump_time
            )
            time.sleep(self.__settings.pump_delay)
