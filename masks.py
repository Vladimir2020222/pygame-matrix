from typing import Sequence

import pygame

from base import SymbolChanger
from symbol import Symbol


class Mask(pygame.sprite.Sprite, SymbolChanger):
    rect: pygame.rect.Rect
    image: pygame.Surface
    mask: pygame.Mask
    symbol_state_keys: Sequence[str]

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


class SkullMask(Mask):
    symbol_state_keys = ('color', 'is_blinking', 'enable_blinking', 'size')

    def __init__(self, *, x, y, default_color=(170, 0, 0), scale=1, change_symbols_scale=True):
        self.increase_symbols_scale = change_symbols_scale
        super().__init__(image='skull.png', x=x, y=y, default_color=default_color, scale=scale)

    def apply(self, symbol: Symbol) -> None:
        if super().apply(symbol):
            if self.increase_symbols_scale:
                symbol.size *= 0.2
