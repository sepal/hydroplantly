from PIL import Image

DISPLAY_WIDTH = 160
DISPLAY_HEIGHT = 80

COLOR_WHITE = (255, 255, 255)
COLOR_BLUE = (31, 137, 251)
COLOR_GREEN = (90, 218, 45)
COLOR_YELLOW = (254, 219, 82)
COLOR_RED = (247, 0, 63)
COLOR_BLACK = (0, 0, 0)

COLOR_BG_ACTIVE = (240, 240, 240)
COLOR_TEXT_ACTIVE = (51, 51, 51)

COLOR_BG_INACTIVE = (153, 153, 153)
COLOR_TEXT_INACTIVE = (204, 204, 204)

# Icons
icon_left_chev_right = Image.open('assets/left-chev-right.png')
icon_clock = Image.open("assets/clock.png")
icon_saturation_avg = Image.open("assets/saturation-avg.png")
icon_saturation = Image.open("assets/saturation.png")

# Tabs
bg_tab_left = Image.open('assets/tab-left.png')
bg_tab_mid = Image.open('assets/tab-mid.png')
bg_tab_right = Image.open('assets/tab-right.png')
