from typing import Sequence

import pygame

from base import SymbolChanger
from symbol import Symbol


class Mask(pygame.sprite.Sprite, SymbolChanger):
    rect: pygame.rect.Rect
    image: pygame.Surface
    mask: pygame.Mask
    symbol_state_keys: Sequence[str]
    change_color_every_tick = False

    def __init__(self, *, image=None, x: int, y: int = 0, scale=1, default_color=(0, 0, 0)):
        assert image
        self.default_color = default_color
        self.image = pygame.transform.scale_by(pygame.image.load(image), scale).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width // 2
        self.rect.y = y - self.rect.height // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.keys = []
        super().__init__()

    def get_color(self) -> tuple[int, int, int]:
        return self.default_color

    def overlaps(self, symbol: Symbol) -> tuple[int, int] | None:
        x_offset = symbol.rect[0] - self.rect[0]
        y_offset = symbol.rect[1] - self.rect[1]

        mask = self.mask
        symbol_mask = symbol.mask

        return mask.overlap(symbol_mask, (x_offset, y_offset))

    def apply(self, symbol: Symbol) -> bool:
        if symbol.foreign_data.get(self.get_key('applied')):
            if self.change_color_every_tick:
                symbol.color = self.get_color()
            return False
        self.save_symbol_state(symbol)
        symbol.foreign_data[self.get_key('applied')] = True
        symbol.is_blinking = False
        symbol.enable_blinking = False
        symbol.color = self.get_color()
        return True

    def cancel(self, symbol) -> bool:
        if not symbol.foreign_data.get(self.get_key('applied')):
            return False
        self.restore_symbol_state(symbol)
        del symbol.foreign_data[self.get_key('applied')]
        return True

    def restore_symbol_state_key(self, symbol, key: str, ignore_key_error=True, clear_state=True) -> None:
        if key == 'size':
            try:
                foreign_key = self.get_key(key)
                symbol.set_size(symbol.foreign_data[foreign_key], reset_speed=False)
                if clear_state:
                    del symbol.foreign_data[foreign_key]
            except KeyError:
                if not ignore_key_error:
                    raise
        else:
            super().restore_symbol_state_key(symbol, key, ignore_key_error, clear_state)


class SkullMask(Mask):
    change_color_every_tick = True
    symbol_state_keys = ('color', 'is_blinking', 'enable_blinking', 'size', 'update_color')
    change_symbols_scale_factor = 0.5

    def __init__(self, *, x, y, default_color=(255, 0, 0), scale=1, change_symbols_scale=True):
        self.change_symbols_scale = change_symbols_scale
        super().__init__(image='skull.png', x=x, y=y, default_color=default_color, scale=scale)

    def apply(self, symbol: Symbol) -> None:
        if super().apply(symbol):
            symbol.update_color = False
            if self.change_symbols_scale:
                symbol.set_size(symbol.size * self.change_symbols_scale_factor, reset_speed=False)
