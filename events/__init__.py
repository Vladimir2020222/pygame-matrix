import random
from cmath import sqrt
from time import perf_counter
from typing import Sequence, Type, Collection

import pygame

from base import SymbolChanger, GetAccelerationCoefficientMixin
from config import WIDTH, HEIGHT, DENSITY
from enums import DirectionEnum
from global_ import GLOBAL_VARIABLES
from symbol import Symbol
from masks import Mask, SkullMask


class Event(SymbolChanger):
    duration: float
    incompatible_events: Type['Event'] = []

    def __init__(self, symbols: Sequence[Symbol] | pygame.sprite.Group):
        self.symbols = symbols
        self.started_at = None

    @property
    def time_passed(self):
        return perf_counter() - self.started_at

    def update(self):
        if self.duration < self.time_passed:
            self.stop()

    def start(self):
        self.started_at = perf_counter()
        self.is_active = True

    def stop(self):
        self.is_active = False

    @classmethod
    def is_compatible_with(cls, other_events: Collection[Type['Event']]) -> bool:
        for incompatible_event in cls.incompatible_events:
            if incompatible_event in other_events:
                return False
        for another_event in other_events:
            if another_event == cls:
                return False
        return True

