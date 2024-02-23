import random

import pygame.display

# you can use esc to enable full screen mode

DEBUG = True
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
AVAILABLE_SYMBOLS = ('1', '0')
FONT_NAME = 'arial'
DEFAULT_COLOR = 0, 235, 0
USE_ANTIALIAS = False
FPS = 30  # from 0 to infinity
DENSITY = [16]  # from 0 to infinity
TRAILS_LENGTH = 4
MIN_SYMBOL_OPACITY = 0.1  # from 0 fo 1 (the more value is the fewer lags are)

SYMBOLS_SPEED = 17  # from 0 to infinity
SYMBOLS_SPEED_ADDITION = 2   # from 0 to infinity
SPEED_RANDOMIZATION = 2   # from 0 to infinity
# symbol speed is calculated using this formula:
# self.size * SYMBOLS_SPEED / 15 + SYMBOLS_SPEED_ADDITION + random.randint(0, SPEED_RANDOMIZATION)
# by increasing symbol speed you can decrease lags, but also decrease density


ENABLE_SYMBOLS_RANDOMIZATION = True
SYMBOLS_RANDOMIZATION_SPEED = 0.3  # from 0 to 1

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


def get_random_symbol_size():
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

