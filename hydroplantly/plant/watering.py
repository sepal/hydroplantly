from datetime import datetime, timedelta
from xmlrpc.client import DateTime
from plant.model import Plant, WateringSettings
from plant.moisture import MoistureSensor
from plant.pump import PumpControl


class Watering:
    __settings: WateringSettings

    __pump: PumpControl
    __moisture_sensor: MoistureSensor
    __last_watered: DateTime


    def __init__(self, plant: Plant, settings: WateringSettings) -> None:
        self.__plant = plant
        self.__settings = settings

        self.__pump = PumpControl(WateringSettings.pump_channel)
        self.__moisture_sensor = MoistureSensor(settings.moisture_setting)
        self.__last_watered = datetime.now()

    def update(self) -> None:
        ts = datetime.now()
        if self.__moisture_sensor.active:
            self.__moisture_sensor.update()

        if self.__settings.auto_water \
            and ts - self.__last_watered > self.__settings.water_interval:
            self.__pump.water()
            self.__last_watered = ts

    @property
    def getLastWatered(self) -> DateTime:
        return self.__last_watered
