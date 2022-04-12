from typing import List
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium as UserFont
from plant.watering import Watering
from helpers import DISPLAY_WIDTH, \
    DISPLAY_HEIGHT, \
    icon_left_chev_right, \
    icon_clock, \
    icon_saturation, \
    icon_saturation_avg, \
    bg_tab_left, \
    bg_tab_mid, \
    bg_tab_right, \
    COLOR_BG_ACTIVE, \
    COLOR_BG_INACTIVE, \
    COLOR_TEXT_ACTIVE, \
    COLOR_TEXT_INACTIVE, \
    COLOR_WHITE


class View:

    def __init__(self, image: Image.Image) -> None:
        self.__image = image
        self.__draw = ImageDraw.ImageDraw(image)
        self.font = ImageFont.truetype(UserFont, 14)
        self.font_small = ImageFont.truetype(UserFont, 10)

    def button_a(self):
        return False

    def button_b(self):
        return False

    def button_x(self):
        return False

    def button_y(self):
        return False

    def update(self):
        pass

    def render(self):
        pass

    def clear(self):
        self.__draw.rectangle((0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT), (0, 0, 0))

    def icon(self, icon, position):
        self.__image.paste(icon, position)

    def masked_icon(self, icon, position, color):
        col = Image.new("RGBA", icon.size, color=color)
        self.__image.paste(col, position, mask=icon)

    @property
    def draw(self):
        return self.__draw


class PlantOverview(View):

    __current_tab = 1
    __waterplan = []

    def __init__(self, image: Image.Image, waterplan: List[Watering]) -> None:
        super().__init__(image)
        self.__waterplan = waterplan

    def draw_tabs(self, active_tab):
        self.masked_icon(
            bg_tab_left, (49, 0), COLOR_BG_ACTIVE if active_tab == 1 else COLOR_BG_INACTIVE)
        self.masked_icon(
            bg_tab_mid, (70, 0), COLOR_BG_ACTIVE if active_tab == 2 else COLOR_BG_INACTIVE)
        self.masked_icon(bg_tab_right, (91, 0),
                         COLOR_BG_ACTIVE if active_tab == 3 else COLOR_BG_INACTIVE)

        self.draw.text((57, 1), "1", COLOR_TEXT_ACTIVE if active_tab ==
                       1 else COLOR_TEXT_INACTIVE, self.font_small)
        self.draw.text((78, 1), "2", COLOR_TEXT_ACTIVE if active_tab ==
                       2 else COLOR_TEXT_INACTIVE, self.font_small)
        self.draw.text((99, 1), "3", COLOR_TEXT_ACTIVE if active_tab ==
                       3 else COLOR_TEXT_INACTIVE, self.font_small)

    def render(self):
        watering = self.__waterplan[0]
        sensor = watering.moistureSensor
        next_water = watering.nextWater.strftime('%H:%M')

        self.clear()
        self.icon(icon_left_chev_right, (0, 2))
        self.draw_tabs(self.__current_tab)

        self.draw.text((65, 16), "Basil", COLOR_WHITE, self.font)

        self.icon(icon_clock, (32, 40))

        self.draw.text((22, 60), next_water, COLOR_WHITE, self.font)

        self.icon(icon_saturation, (75, 40))
        self.draw.text((66, 60), "{:1.2f}".format(
            sensor.saturation), COLOR_WHITE, self.font)

        self.icon(icon_saturation_avg, (113, 40))
        self.draw.text((103, 60), "{:1.2f}".format(
            sensor.avgSaturation), COLOR_WHITE, self.font)

    def button_a(self):
        self.__current_tab += 1

        if self.__current_tab > 3:
            self.__current_tab = 1
