import logging
from datetime import datetime, timedelta
from time_interval import TimeInterval
from model import Plant, WateringSettings
from moisture import MoistureSensor
from pump import PumpControl


class Watering:
    __settings: WateringSettings

    __pump: PumpControl
    __moisture_sensor: MoistureSensor
    __last_watered: datetime
    __active_time: TimeInterval

    def __init__(self, plant: Plant, active_time: TimeInterval) -> None:
        self.__plant = plant
        self.__settings = plant.watering_settings

        self.__pump = PumpControl(
            self.__settings.pump_channel, self.__settings.pump_settings)
        self.__moisture_sensor = MoistureSensor(
            self.__plant.watering_settings.moisture_setting)
        self.__last_watered = datetime(1992, 1, 1)
        self.__active_time = active_time

    def update(self) -> None:
        ts = datetime.now()
        if self.__moisture_sensor.active:
            self.__moisture_sensor.update()
            logging.info(
                f"Updated moisture sensor {self.__moisture_sensor.channel}")
            logging.info(f"Saturation: {self.__moisture_sensor.saturation}")
            logging.info(
                f"Average saturation: {self.__moisture_sensor.avgSaturation}")

        if self.__settings.auto_water \
                and ts - self.__last_watered > self.__settings.water_interval \
                and self.__active_time.isInDatetime(ts):
            logging.info(f"Enabling pump on channel {self.__pump.channel}")
            self.__pump.water()
            self.__last_watered = ts

    @property
    def getLastWatered(self) -> datetime:
        return self.__last_watered

    @property
    def nextWater(self) -> datetime:
        next_watering = self.__last_watered + self.__settings.water_interval
        if not self.__active_time.isInDatetime(next_watering):
            next_watering = self.__active_time.dtStart

        return next_watering

    @property
    def moistureSensor(self) -> MoistureSensor:
        return self.__moisture_sensor

    @property
    def plantName(self) -> str:
        return self.__plant.name

    @property
    def channel(self) -> int:
        return self.__settings.pump_channel

    @property
    def autoWater(self) -> bool:
        return self.__settings.auto_water
