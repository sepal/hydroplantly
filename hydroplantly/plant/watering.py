import logging
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


    def __init__(self, plant: Plant) -> None:
        self.__plant = plant

        self.__pump = PumpControl(WateringSettings.pump_channel)
        self.__moisture_sensor = MoistureSensor(self.__plant.watering_settings.moisture_setting)
        self.__last_watered = datetime.now()

    def update(self) -> None:
        ts = datetime.now()
        if self.__moisture_sensor.active:
            self.__moisture_sensor.update()
            logging.info(f"Updated moisture sensor {self.__moisture_sensor.channel}")
            logging.info(f"Saturation: {self.__moisture_sensor.saturation}")
            logging.info(f"Average saturation: {self.__moisture_sensor.avgSaturation}")

        if self.__settings.auto_water \
            and ts - self.__last_watered > self.__settings.water_interval:
            self.__pump.water()
            self.__last_watered = ts
            logging.info(f"Watered channel {self.__pump.channel}")

    @property
    def getLastWatered(self) -> DateTime:
        return self.__last_watered

    @property
    def moistureSensor(self) -> MoistureSensor:
        return self.__moisture_sensor
        
