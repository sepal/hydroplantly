from datetime import datetime
import json
import logging
from threading import Timer
import time
import signal
import sys
from typing import List
from camera import Camera
from interface import Display
from views import PlantOverview
from watering import Watering
from time_interval import TimeInterval
from model import CameraSettings, Plant

global app_timer


class ProgramKilled(Exception):
    pass


def signal_handler(signum, frame):
    raise ProgramKilled


class App:
    __plants: List[Plant]
    __waterplan: List[Watering]
    __active_time: TimeInterval

    def __init__(self, settings_file: str) -> None:
        self.__waterplan = []
        self.__plants = []
        with open(settings_file) as file:
            settings = json.load(file)
                
            active_settings = settings['general']['active_time']
            self.__active_time = TimeInterval.from_time(
                active_settings['from'], active_settings['to'])

            for plant_settings in settings['plants']:
                plant = Plant(**plant_settings)
                watering = Watering(plant, self.__active_time)
                self.__plants.append(plant)
                self.__waterplan.append(watering)

            if "camera" in settings:
                camera_settings = CameraSettings(**settings['camera'])
            else:
                camera_settings = CameraSettings()
            self.__camera = Camera(camera_settings, self.__active_time)

        self.__display = Display()
        self.__display.setView(PlantOverview(self.__display.image, self.__waterplan))

    def update(self) -> None:
        logging.info("Watering update")
        for watering in self.__waterplan:
            watering.update()

        self.__display.update()

        self.__camera.update()

    @property
    def active(self):
        return self.__active_time.isInDatetime(datetime.now())


def app_updater(app: App) -> None:
    global app_timer
    logging.info(f"Running update")
    app.update()
    app_timer = Timer(10, app_updater, [app])
    app_timer.start()


def main():
    global app_timer
    logging.basicConfig(format='%(asctime)s %(levelname)-2s %(message)s',
                        level=logging.INFO,
                        handlers=[
                            logging.FileHandler("hydroplantly.log"),
                            logging.StreamHandler()
                        ])

    logging.info("Starting app")
    app = App("settings.json")
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    app_timer = Timer(1, app_updater, [app])
    app_timer.start()

    while True:
        try:
            time.sleep(10)
        except ProgramKilled:
            logging.warning("Program was stopped!")
            app_timer.cancel()
            sys.exit(0)


if __name__ == "__main__":
    main()
