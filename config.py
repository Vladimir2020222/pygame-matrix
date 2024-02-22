import random

import pygame.display

# you can use esc to enable full screen mode

DEBUG = False
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
AVAILABLE_SYMBOLS = ('1', '0')
FONT_NAME = 'arial'
DEFAULT_COLOR = 0, 235, 0
USE_ANTIALIAS = False
FPS = 3000  # from 0 to infinity
DENSITY = [15]  # from 0 to infinity
TRAILS_LENGTH = 4
MIN_SYMBOL_OPACITY = 0.1  # from 0 fo 1 (the more value is the fewer lags are)

SYMBOLS_SPEED = 8  # from 0 to infinity
SYMBOLS_SPEED_ADDITION = 5   # from 0 to infinity
SPEED_RANDOMIZATION = 4   # from 0 to infinity
# symbol speed is calculated using this formula:
# self.size * SYMBOLS_SPEED / 15 + SYMBOLS_SPEED_ADDITION + random.randint(0, SPEED_RANDOMIZATION)
# by increasing symbol speed you can decrease lags, but also decrease density


ENABLE_SYMBOLS_RANDOMIZATION = True
SYMBOLS_RANDOMIZATION_SPEED = 0.3  # from 0 to 1

ENABLE_BLINKING = True
BLINKING_FREQUENCY = 0.2  # from 0 to 1
BLINKING_STOP_PROBABILITY = 0.33  # from 1 to infinity
BLINKING_0_OPACITY_PROBABILITY = 0.4  # from 0 to 1
BLINKING_SYMBOL_MAX_OPACITY = 0.3

ENABLE_EVENTS = True
ENABLE_VISUAL_EVENTS = True
VISUAL_EVENTS_FREQUENCY_MULTIPLIER = 2  # from 1 to infinity
ENABLE_MASK_EVENTS = True  # !!! MAY CAUSE LOTS OF LAGS !!!
MASK_EVENTS_FREQUENCY_MULTIPLIER = 1
ENABLE_MOVEMENT_EVENTS = True  # !!!!!! MAY CAUSE LAGS !!!!!
MOVEMENT_EVENTS_FREQUENCY_MULTIPLIER = 1
SCREEN_SCROLL_STOP_SYMBOLS_PROBABILITY = 0.3
EVENTS_FREQUENCY = 0.03  # from 0 to 1


def get_random_symbol_size():
    random_int = random.random()
    if random_int < 0.8:
        return random.randint(5, 8)
    elif random_int < 0.9:
        return random.randint(8, 20)
    elif random_int < 0.99:
        return random.randint(15, 35)
    return random.randint(30, 50)
