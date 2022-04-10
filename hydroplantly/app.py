import json
from plant import Plant

class App:
    __plants = [Plant]

    def __init__(self, settings_file: str) -> None:
        with open(settings_file) as file:
            settings = json.load(file)
            for plant_settings in settings['plants']:
                plant = Plant(**plant_settings)
                self.__plants.append(plant)

        print(self.__plants)


def main():
    app = App("settings.json")

if __name__ == "__main__":
    main()