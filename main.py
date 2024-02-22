# region imports
import pygame
pygame.init()
import random
from typing import Sequence, Type


from events.movement import AccelerationEvent, ScreenScrollEvent, ApproximationEvent

from fps_printer import FpsCounter
from setup import load_events
from events import Event
from global_ import GLOBAL_VARIABLES
from config import WIDTH, HEIGHT, FPS, DENSITY, AVAILABLE_SYMBOLS, DEBUG, get_random_symbol_size, ENABLE_EVENTS, \
    EVENTS_FREQUENCY
from symbol import Symbol


# endregion

if __name__ == '__main__':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

fps_counter = FpsCounter()

symbols: Sequence[Symbol] | pygame.sprite.Group = pygame.sprite.Group()
events: list[Event] = []


possible_events: list[Type[Event]] = load_events()


def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        GLOBAL_VARIABLES['tick'] += 1
        if DEBUG:
            fps_counter.update()
            fps_counter.print()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(pygame.display.is_fullscreen())
                    pygame.display.toggle_fullscreen()

        screen.fill((0, 0, 0))

        # region updating and creating symbols

        for symbol in symbols:
            if GLOBAL_VARIABLES['tick'] % 5 == 0 and symbol.should_be_removed():
                symbols.remove(symbol)
                if not symbol.is_part_of_trail:
                    for trail_symbol in symbol.trail:
                        symbols.remove(trail_symbol)
            symbol.update()
            symbol.draw(screen)

        for _ in range(DENSITY[0]):
            new_symbol = Symbol(
                random.choice(AVAILABLE_SYMBOLS),
                x=random.randint(0, WIDTH),
                y=0,
                size=get_random_symbol_size()
            )

            symbols.add(new_symbol)
            symbols.add(*new_symbol.get_trail())

        # endregion

        # region events
        if ENABLE_EVENTS:
            if random.random() < EVENTS_FREQUENCY:
                for _ in range(5):
                    event_class: Type[Event] = random.choice(possible_events)
                    event = event_class(symbols)

                    new_event_is_compatible = event.is_compatible_with(events)
                    other_events_is_compatible = all(
                        e.is_compatible_with((event, )) for e in events
                    )
                    if new_event_is_compatible and other_events_is_compatible:
                        event.start()
                        events.append(event)
                    break

            for event in events:
                event.update()
                if not event.is_active:
                    events.remove(event)

        # endregion

        # region masks

        for mask in GLOBAL_VARIABLES['masks']:
            for symbol in symbols:
                if mask.overlaps(symbol):
                    mask.apply(symbol)
                else:
                    mask.cancel(symbol)

        # endregion

        pygame.display.update()


if __name__ == '__main__':
    main()
