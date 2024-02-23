import random
from typing import Optional, Any

import pygame

from config import WIDTH, HEIGHT, USE_ANTIALIAS, SYMBOLS_SPEED, ENABLE_SYMBOLS_RANDOMIZATION, \
    AVAILABLE_SYMBOLS, ENABLE_BLINKING, SYMBOLS_RANDOMIZATION_SPEED, BLINKING_FREQUENCY, \
    BLINKING_0_OPACITY_PROBABILITY, SPEED_RANDOMIZATION, \
    BLINKING_SYMBOL_MAX_OPACITY, BLINKING_STOP_PROBABILITY, DEFAULT_COLOR, TRAILS_LENGTH, MIN_SYMBOL_OPACITY, \
    FONT_NAME, SYMBOLS_SPEED_ADDITION, get_color, DISTANCE_BETWEEN_SYMBOLS_IN_TAIL, UPDATE_SYMBOL_COLOR


def load_font(s):
    try:
        return pygame.font.Font(FONT_NAME, round(s))
    except FileNotFoundError:
        return pygame.font.SysFont(FONT_NAME, round(s))


class Symbol(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    trail: Optional[list['Symbol']] = None

    decrease_opacity = 1 / (TRAILS_LENGTH + 1)

    def __init__(
            self,
            symbol: str,
            *,
            x: int,
            y: int,
            opacity: float = 1,
            size: int = 10,
            color: tuple[int, int, int] = None,
            enable_symbol_randomization: bool = ENABLE_SYMBOLS_RANDOMIZATION,
            enable_blinking: bool = ENABLE_BLINKING,
            speed: Optional[int] = None,
            is_part_of_trail: bool = False,
            trail_head: 'Symbol' = None,
            update_color: bool = UPDATE_SYMBOL_COLOR
    ):
        super().__init__()
        assert is_part_of_trail == (not not trail_head)

        self.opacity_before_blinking = opacity
        self.enable_symbol_randomization = enable_symbol_randomization
        self.update_color = update_color
        self.speed = speed
        self._speed_randomization = None
        self.is_part_of_trail = is_part_of_trail
        if is_part_of_trail:
            self.trail_head = trail_head
        self.symbol = symbol
        self.opacity = opacity
        self.color = color or get_color()
        self.is_blinking = False

        self.foreign_data: dict[str, Any] = {}
        self.enable_blinking = enable_blinking

        self.__previous_rounded_size = round(size) - 10
        self.size = size          # this line make size setter to load font

        self.image = self.get_rendered_symbol()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

    def size(self) -> int:
        return self._size

    def set_size(self, value: int, *, reset_speed=True):
        self._size = value
        rounded_value = round(value)

        if rounded_value != self.__previous_rounded_size:
            if reset_speed:
                self._speed = None
            self.__previous_rounded_size = round(value)
            try:
                self._font = fonts_cache[rounded_value]
            except KeyError:
                self._font = load_font(rounded_value)
                fonts_cache[rounded_value] = self._font

    size = property(size, set_size)

    @property
    def speed(self):
        if self._speed is None:
            self._speed = self.size * SYMBOLS_SPEED / 15 + SYMBOLS_SPEED_ADDITION
            if not self.is_part_of_trail:
                speed_randomization = random.randint(0, SPEED_RANDOMIZATION)
                self._speed += speed_randomization
                self._speed_randomization = speed_randomization
            else:
                self._speed_randomization = self.trail_head._speed_randomization
                self._speed += self._speed_randomization
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.get_rendered_symbol(), (self.rect.x, self.rect.y))

    def should_be_removed(self) -> bool:
        return ((not -1000 < self.rect.y < HEIGHT + 10)
                or (not 10 < self.rect.x < WIDTH + 10)
                or (self.opacity <= MIN_SYMBOL_OPACITY and (not self.is_blinking and self.enable_blinking)))

    def update(self) -> None:
        self.rect.y += self._speed or self.speed

        if self.enable_symbol_randomization and random.random() < SYMBOLS_RANDOMIZATION_SPEED:
            if len(AVAILABLE_SYMBOLS) == 2:
                self.symbol = AVAILABLE_SYMBOLS[AVAILABLE_SYMBOLS.index(self.symbol) - 1]
            else:
                self.symbol = random.choice(AVAILABLE_SYMBOLS)

        if self.enable_blinking:
            if self.is_blinking:
                if random.random() < BLINKING_STOP_PROBABILITY:
                    self.opacity = self.opacity_before_blinking
                    self.is_blinking = False
            elif random.random() < BLINKING_FREQUENCY:
                self.is_blinking = True
                self.opacity_before_blinking = self.opacity
                if random.random() < BLINKING_0_OPACITY_PROBABILITY:
                    self.opacity = 0
                else:
                    self.opacity = round(random.random() * BLINKING_SYMBOL_MAX_OPACITY, 1)
        if self.update_color:
            self.color = get_color()

    def get_trail(self, attach=True) -> list['Symbol']:
        trail = []
        new_symbol = self._get_next_in_trail()

        while new_symbol:
            trail.append(new_symbol)
            new_symbol = new_symbol._get_next_in_trail()
        if attach:
            self.trail = trail
        return trail

    def _get_next_in_trail(self) -> Optional['Symbol']:
        if self.should_be_removed() or self.opacity - self.decrease_opacity <= MIN_SYMBOL_OPACITY:
            return

        rendered_symbol = self.get_rendered_symbol()
        symbol = Symbol(
            self.symbol,
            x=self.rect.x,
            y=self.rect.y - (rendered_symbol.get_height() * DISTANCE_BETWEEN_SYMBOLS_IN_TAIL),
            opacity=self.opacity - self.decrease_opacity,
            size=self.size,
            color=self.color,
            speed=self.speed,
            is_part_of_trail=True,
            trail_head=self
        )
        return symbol

    def get_rendered_symbol(self) -> pygame.Surface:
        alpha: int = round(255 * self.opacity, -1)
        cached = symbols_cache.get((self.symbol, self.size, self.color, alpha))
        if cached:
            self.image = cached
            return cached

        rendered_symbol = self._font.render(
            self.symbol,
            USE_ANTIALIAS,
            pygame.Color(*self.color)
        )
        rendered_symbol.set_alpha(alpha)
        symbols_cache[(self.symbol, self.size, self.color, alpha)] = rendered_symbol
        self.image = rendered_symbol
        return rendered_symbol

    def __repr__(self):
        r = (f'Symbol(\n'
                f'\tcoords={self.rect.x, self.rect.y},\n'
                f'\tsize={self.size},\n'
                f'\topacity={self.opacity},\n'
                f'\tspeed={self.speed}\n'
                f'\tis_part_of_trail={self.is_part_of_trail}\n')
        if self.is_part_of_trail:
            r += f'\thead_coords={self.trail_head.rect.x, self.trail_head.rect.y}'
        return r + ')'

    __str__ = __repr__


fonts_cache: dict[int, pygame.font.Font] = {}

symbols_cache: dict[
    tuple[str, int, tuple[int, int, int], int],
    pygame.Surface
] = {}
