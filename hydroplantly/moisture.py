from typing import Dict, List
from grow.moisture import Moisture

from model import MoistureSettings

NUM_SAMPLES = 10


class MoistureSensor:
    __sensor: Moisture
    __settings: MoistureSettings
    __avg_saturation: float
    __last_reading: float
    __saturation = [float]

    def __init__(self, settings: MoistureSettings) -> None:
        self.__settings = settings
        self.__sensor = Moisture(
            settings.channel, settings.wet_point, settings.dry_point)
        self.__saturation = [1.0 for _ in range(NUM_SAMPLES)]
        self.__last_reading = 0.0
        self.__avg_saturation = 0.0

    @property
    def active(self) -> bool:
        return self.__settings.active

    def update(self) -> None:
        self.__last_reading = self.__sensor.saturation
        self.__saturation.append(self.__last_reading)
        self.__saturation = self.__saturation[-NUM_SAMPLES:]
        self.__avg_saturation = sum(self.__saturation) / float(NUM_SAMPLES)

    @property
    def avgSaturation(self) -> float:
        return self.__avg_saturation

    @property
    def saturation(self) -> float:
        return self.__last_reading

    @property
    def channel(self) -> int:
        return self.__settings.channel
