import random

import pygame.display

from global_ import GLOBAL_VARIABLES

# you can use esc to enable full screen mode

DEBUG = False
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]

AVAILABLE_SYMBOLS = ('1', '0')

FONT_NAME = 'unifont-15.1.04.ttf'
DEFAULT_COLOR = 0, 235, 0
ENABLE_COLOR_CHANGING = False  # this setting is not necessary for project, it is needed for default implementation of
#                               get_color function below
UPDATE_SYMBOL_COLOR = False  # update symbol color every tick using function get_color
USE_ANTIALIAS = False
FPS = 30  # from 0 to infinity
DENSITY = [15]  # from 0 to infinity
TRAILS_LENGTH = 4
MIN_SYMBOL_OPACITY = 0.1  # from 0 fo 1 (the more value is the fewer lags are)
DISTANCE_BETWEEN_SYMBOLS_IN_TAIL = 1  # from 0 to infinity; this number is multiplied to symbol height
DISTRIBUTE_SYMBOLS_BY_ROWS = False

SYMBOLS_SPEED = 12  # from 0 to infinity
SYMBOLS_SPEED_ADDITION = 3   # from 0 to infinity
SPEED_RANDOMIZATION = 4   # from 0 to infinity
# symbol speed is calculated using this formula:
# self.size * SYMBOLS_SPEED / 15 + SYMBOLS_SPEED_ADDITION + random.randint(0, SPEED_RANDOMIZATION)
# by increasing symbol speed you can decrease lags, but also decrease density


ENABLE_SYMBOLS_RANDOMIZATION = True
SYMBOLS_RANDOMIZATION_SPEED = 0.1  # from 0 to 1

ENABLE_BLINKING = True
BLINKING_FREQUENCY = 0.2  # from 0 to 1
BLINKING_STOP_PROBABILITY = 0.33  # from 1 to infinity
BLINKING_0_OPACITY_PROBABILITY = 0.5  # from 0 to 1
BLINKING_SYMBOL_MAX_OPACITY = 0.3


ENABLE_EVENTS = True
EVENTS_START_DELAY = 2  # time from start to enabling events in seconds

ENABLE_VISUAL_EVENTS = True
VISUAL_EVENTS_FREQUENCY_MULTIPLIER = 3  # from 1 to infinity

ENABLE_MASK_EVENTS = True  # !!! MAY CAUSE LOTS OF LAGS !!!
MASK_EVENTS_FREQUENCY_MULTIPLIER = 1  # from 1 to infinity

ENABLE_MOVEMENT_EVENTS = True  # !!!!!! MAY CAUSE LAGS !!!!!
MOVEMENT_EVENTS_FREQUENCY_MULTIPLIER = 2  # from 1 to infinity

SCREEN_SCROLL_STOP_SYMBOLS_PROBABILITY = 0.4
EVENTS_FREQUENCY = 0.03  # from 0 to 1


def get_random_symbol_size() -> float:
    random_value = random.random()

    if random_value < 0.5:
        return random.randint(2, 8)
    if random_value < 0.8:
        return random.randint(8, 15)
    if random_value < 0.92:
        return random.randint(13, 25)
    if random_value < 0.98:
        return random.randint(20, 45)
    if random_value < 0.992:
        return random.randint(40, 70)
    return random.randint(50, random.randint(70, random.randint(100, 500)))


def get_new_symbol_x(symbol_size: float) -> float:
    if DISTRIBUTE_SYMBOLS_BY_ROWS:
        size = symbol_size * 1.2
        cols = WIDTH // size
        return random.randint(0, round(cols - 1)) * size
    return random.randint(0, WIDTH)


_R, _G, _B = DEFAULT_COLOR
_COLOR_AIM = (0, 255, 255)
_tick = 2
_COLOR_CHANGING_SPEED = 2


def _increase_color_lightness(color: tuple[int, int, int]) -> tuple[int, int, int]:
    multiplier = 255 / max(color)
    return (
        round(color[0] * multiplier),
        round(color[1] * multiplier),
        round(color[2] * multiplier)
    )


def get_color() -> tuple[int, int, int]:
    if ENABLE_COLOR_CHANGING:
        global _R, _G, _B, _COLOR_AIM, _tick
        if GLOBAL_VARIABLES['tick'] == _tick:
            for _ in range(_COLOR_CHANGING_SPEED):
                if _R != _COLOR_AIM[0]:
                    _R += 1 if _R < _COLOR_AIM[0] else -1
                if _G != _COLOR_AIM[1]:
                    _G += 1 if _G < _COLOR_AIM[1] else -1
                if _B != _COLOR_AIM[2]:
                    _B += 1 if _B < _COLOR_AIM[2] else -1
            _tick += 1
        if (_R, _G, _B) == _COLOR_AIM:
            _COLOR_AIM = _increase_color_lightness((
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ))
        return _R, _G, _B
    return DEFAULT_COLOR
