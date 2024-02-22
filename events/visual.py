import random

from base import GetAccelerationCoefficientMixin
from events import Event


class VisualEvent(Event):
    pass


class BlinkingEvent(VisualEvent, GetAccelerationCoefficientMixin):
    duration = 2
    blinking_speed = 0.8
    acceleration_time = 0.8
    symbol_state_keys = ['opacity', 'enable_blinking']

    def __init__(self, symbols):
        super().__init__(symbols)

    def update(self):
        acceleration_coefficient = self.get_acceleration_coefficient() * self.blinking_speed
        key = self.get_key('opacity')
        for symbol in self.symbols:
            if key not in symbol.foreign_data.keys():
                self.save_symbol_state(symbol)
                symbol.enable_blinking = False
                symbol.opacity = 0
            else:
                if random.random() < acceleration_coefficient:
                    symbol.opacity = 0
                else:
                    symbol.opacity = symbol.foreign_data[key]
        super().update()

    def stop(self):
        super().stop()
        for symbol in self.symbols:
            self.restore_symbol_state(symbol)
