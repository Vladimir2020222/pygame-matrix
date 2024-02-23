import random
from cmath import sqrt
from typing import Sequence, Collection, Type

import pygame

from base import GetAccelerationCoefficientMixin
from config import DENSITY, HEIGHT, WIDTH, SCREEN_SCROLL_STOP_SYMBOLS_PROBABILITY
from enums import DirectionEnum
from events import Event
from symbol import Symbol


class MovementEvent(Event):
    pass


class AccelerationEvent(MovementEvent, GetAccelerationCoefficientMixin):
    duration = 3
    acceleration_time = 1.5
    speed = 5
    symbol_state_keys = ['speed']

    def __init__(self, symbols):
        self.density = DENSITY[0]
        super().__init__(symbols)

    def start(self):
        super().start()
        self.density = DENSITY[0]
        for symbol in self.symbols:
            self.save_symbol_state(symbol)

    def stop(self):
        super().stop()
        DENSITY[0] = self.density
        for symbol in self.symbols:
            self.restore_symbol_state(symbol)

    def update(self):
        super().update()
        acceleration = self.speed * self.get_acceleration_coefficient()
        acceleration = max(acceleration, 1)
        DENSITY[0] = round(self.density * acceleration)
        key = self.get_key('speed')
        for symbol in self.symbols:
            try:
                symbol.speed = symbol.foreign_data[key] * acceleration
            except KeyError:
                self.save_symbol_state(symbol)
                symbol.speed = symbol.speed * acceleration


class ScreenScrollEvent(MovementEvent, GetAccelerationCoefficientMixin):
    duration = 4
    acceleration_time = 1.5
    speed = 1.35
    symbol_state_keys = ['speed']
    incompatible_events = []

    def __init__(
            self,
            symbols: Sequence[Symbol] | pygame.sprite.Group,
            direction: DirectionEnum = None,
            stop_symbols: bool = None
    ):
        if stop_symbols is None:
            stop_symbols = random.random() < SCREEN_SCROLL_STOP_SYMBOLS_PROBABILITY
        self.stop_symbols = stop_symbols
        if direction is None:
            directions = (DirectionEnum.left, DirectionEnum.right)
            if stop_symbols:
                directions += (DirectionEnum.bottom, )
            direction = random.choice(directions)
        self.direction = direction
        self.density = None
        super().__init__(symbols)

    def get_speed(self) -> float:
        return self.speed * self.get_acceleration_coefficient()

    def start(self):
        super().start()
        if self.stop_symbols:
            for symbol in self.symbols:
                self.save_symbol_state(symbol)
                symbol.speed = 0
            self.density = DENSITY[0]
            DENSITY[0] = 0

    def update(self):
        super().update()
        for symbol in self.symbols:
            try:
                speed = symbol.foreign_data[self.get_key('speed')] * self.get_speed()
            except KeyError:
                speed = symbol.speed * self.get_speed()
            match self.direction:
                case DirectionEnum.top:
                    symbol.rect.y += speed
                    if symbol.rect.y >= HEIGHT:
                        symbol.rect.y = 0
                case DirectionEnum.bottom:
                    symbol.rect.y -= speed
                    if symbol.rect.y <= 0:
                        symbol.rect.y = HEIGHT - 1
                case DirectionEnum.left:
                    symbol.rect.x -= speed
                    if symbol.rect.x <= 0:
                        symbol.rect.x = WIDTH
                case DirectionEnum.right:
                    symbol.rect.x += speed
                    if symbol.rect.x >= WIDTH:
                        symbol.rect.x = 0

    def stop(self):
        super().stop()
        if self.stop_symbols:
            for symbol in self.symbols:
                self.restore_symbol_state(symbol)
            DENSITY[0] = self.density

    def is_compatible_with(self, other_events: Collection['Event']) -> bool:
        return super().is_compatible_with(other_events) and not (
            AccelerationEvent in [x.__class__ for x in other_events] and self.stop_symbols
        )


class ApproximationEvent(MovementEvent, GetAccelerationCoefficientMixin):
    duration = 1.2
    acceleration_time = 0.4
    approximation_speed = 0.04
    incompatible_events = [AccelerationEvent, ScreenScrollEvent]

    def __init__(self, *args, to: tuple[int, int] = None, **kwargs):
        if to is None:
            to = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.to = to
        self.density = DENSITY[0]
        super().__init__(*args, **kwargs)

    def start(self):
        super().start()
        self.density = DENSITY[0]
        DENSITY[0] = 0
        for symbol in self.symbols:
            symbol.speed = 0

    def update(self):
        super().update()
        acceleration_coefficient = self.get_acceleration_coefficient()
        coefficient = self.approximation_speed * acceleration_coefficient
        size_multiplier = 1 + coefficient
        for symbol in self.symbols:
            rect = symbol.rect
            symbol.set_size(symbol._size * size_multiplier, reset_speed=False)

            move_coefficient = coefficient * min(6, (symbol.size / 14) ** 1.5)

            # approximation #
            x_distance = self.to[0] - rect.x
            y_distance = self.to[1] - rect.y
            distance = max(sqrt(x_distance ** 2 + y_distance ** 2).real, 0.001)
            # x value #
            if symbol.is_part_of_trail:
                rect.x = symbol.trail_head.rect.x
            else:
                cos = x_distance / distance
                x_change = x_distance * cos * move_coefficient + 0.3  # it works awful without this stupid magic value

                if rect.x > self.to[0]:
                    rect.x += x_change
                else:
                    rect.x -= x_change

            # y value #
            sin = y_distance / distance

            y_change = y_distance * sin * move_coefficient + 0.3  # same
            if rect.y > self.to[1]:
                rect.y += y_change
            else:
                rect.y -= y_change

    def stop(self):
        super().stop()
        for symbol in self.symbols:
            symbol._speed = None
        DENSITY[0] = self.density
