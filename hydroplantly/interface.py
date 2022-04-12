from PIL import Image
import ST7735
import RPi.GPIO as GPIO
from helpers import DISPLAY_WIDTH, DISPLAY_HEIGHT
from views import View


BUTTONS = [5, 6, 16, 24]
LABELS = ["A", "B", "X", "Y"]

class Display:

    def __init__(self) -> None:
        self.__display = ST7735.ST7735(
            port=0, cs=1, dc=9, backlight=12, rotation=270, spi_speed_hz=80000000)

        # Set up our canvas and prepare for drawing
        self.__image = Image.new("RGBA", (DISPLAY_WIDTH, DISPLAY_HEIGHT), color=(255, 255, 255))

        # Setup blank image for darkness
        self.__image_blank = Image.new("RGBA", (DISPLAY_WIDTH, DISPLAY_HEIGHT), color=(0, 0, 0))

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        for pin in BUTTONS:
            GPIO.add_event_detect(pin, GPIO.FALLING, self.handleButton, bouncetime=200)


    def setView(self, view: View):
        self.__view = view

    def update(self):
        if self.__view == None:
            return
        
        self.__view.render()
        self.__display.display(self.__image.convert("RGB"))

    def handleButton(self, pin):
        if self.__view == None:
            return
        index = BUTTONS.index(pin)
        label = LABELS[index]

        if label == "A":
            self.__view.button_a()

        self.update()





    @property
    def image(self):
        return self.__image 