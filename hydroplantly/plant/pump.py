import logging
from grow.pump import Pump

from plant.model import PumpSettings, WateringSettings
import time

class PumpControl:
    __pump: Pump
    __settings: PumpSettings
    __channel: int

    def __init__(self, channel: int, settings: PumpSettings) -> None:
        self.__settings = settings
        self.__pump = Pump(channel)
        self.__channel = channel

    def water(self):
        for i in range(self.__settings.repeat):
            logging.info(f"Dose {i} on channel {self.channel}")
            self.__pump.dose(self.__settings.speed, 
                self.__settings.time
            )
            time.sleep(self.__settings.delay)

    @property
    def channel(self) -> int:
        return self.__channel
