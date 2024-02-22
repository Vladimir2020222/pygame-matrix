import random
from typing import Type, Collection

from config import WIDTH, HEIGHT
from events import Event
from events.movement import ApproximationEvent
from global_ import GLOBAL_VARIABLES
from masks import Mask, SkullMask


class MaskEvent(Event):
    enable_blinking = False
    mask_class: Type[Mask]
    default_color: tuple[int, int, int] = None

    def __init__(self, symbols, *, x=0, y=0, scale=1, default_color=None):
        x = x or random.randint(int(WIDTH // 4), int(WIDTH // 1.5))
        y = y or random.randint(int(HEIGHT // 4), int(HEIGHT // 1.5))
        kwargs = {'x': x, 'y': y, 'scale': scale}
        if default_color := default_color or self.default_color:
            kwargs['default_color'] = default_color
        self.mask = self.mask_class(**kwargs)
        self.mask_visible = True
        super().__init__(symbols)

    def show_mask(self):
        self.mask_visible = True
        GLOBAL_VARIABLES['masks'].append(self.mask)

    def hide_mask(self):
        self.mask_visible = False
        try:
            GLOBAL_VARIABLES['masks'].remove(self.mask)
        except ValueError:
            pass
        else:
            for symbol in self.symbols:
                self.mask.cancel(symbol)

    def start(self):
        super().start()
        self.show_mask()

    def update(self):
        random_value = random.random()
        if (
                self.enable_blinking and
                self.is_active and
                random_value < 0.1 or (not self.is_active) and random_value < 0.4
        ):
            if self.mask_visible:
                self.hide_mask()
            else:
                self.show_mask()
        super().update()

    def stop(self):
        self.hide_mask()
        super().stop()


class SkullMaskEvent(MaskEvent):
    duration = 3
    mask_class = SkullMask
    incompatible_events = [ApproximationEvent]

    def __init__(self, symbols, **kwargs):
        if 'scale' not in kwargs:
            kwargs['scale'] = random.randint(17, 17) / 10
        super().__init__(symbols, **kwargs)
