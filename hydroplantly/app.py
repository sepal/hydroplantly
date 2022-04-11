import json
import logging
from hydroplantly.plant.moisture import MoistureSensor
from hydroplantly.plant.watering import Watering
from plant import Plant

class App:
    __plants = [Plant]
    __waterplan = [Watering]

    def __init__(self, settings_file: str) -> None:
        with open(settings_file) as file:
            settings = json.load(file)
            for plant_settings in settings['plants']:
                plant = Plant(**plant_settings)
                watering = Watering(plant)
                self.__plants.append(plant)
                self.__waterplan.append(watering)

    def update(self) -> None:
        for watering in self.__waterplan:
            watering.update()

def main():
    app = App("settings.json")

if __name__ == "__main__":
    main()