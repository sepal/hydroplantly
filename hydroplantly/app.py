from datetime import datetime
import json
import logging
from typing import List
from hydroplantly.plant.watering import Watering
from hydroplantly.time_interval import TimeInterval
from plant import Plant



class App:
    __plants: List[Plant]
    __waterplan: List[Watering]
    __active_time: TimeInterval

    def __init__(self, settings_file: str) -> None:
        with open(settings_file) as file:
            settings = json.load(file)
            for plant_settings in settings['plants']:
                plant = Plant(**plant_settings)
                watering = Watering(plant)
                self.__plants.append(plant)
                self.__waterplan.append(watering)
            active_settings = settings['general']['active_time']
            self.__active_time = TimeInterval.from_time(active_settings['from'], active_settings['to'])



    def update(self) -> None:
        if not self.active:
            logging.info("Sleeping")
            return 

        logging.info("Watering update")
        for watering in self.__waterplan:
            watering.update()

    @property
    def active(self):
        return self.__active_time.isInDatetime(datetime.now())

def main():
    app = App("settings.json")

if __name__ == "__main__":
    main()