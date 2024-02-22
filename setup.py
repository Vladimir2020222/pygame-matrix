from typing import Type

from config import MASK_EVENTS_FREQUENCY_MULTIPLIER, ENABLE_MOVEMENT_EVENTS, MOVEMENT_EVENTS_FREQUENCY_MULTIPLIER, \
    ENABLE_VISUAL_EVENTS, VISUAL_EVENTS_FREQUENCY_MULTIPLIER, ENABLE_MASK_EVENTS
from events import Event
from events.masks import SkullMaskEvent, MaskEvent
from events.movement import AccelerationEvent, ScreenScrollEvent, ApproximationEvent, MovementEvent
from events.visual import BlinkingEvent, VisualEvent


def load_events() -> list[Type[Event]]:
    events = []
    for event in (ApproximationEvent, SkullMaskEvent, AccelerationEvent, ScreenScrollEvent, BlinkingEvent):
        if issubclass(event, MaskEvent) and ENABLE_MASK_EVENTS:
            events.extend((event,) * MASK_EVENTS_FREQUENCY_MULTIPLIER)
        elif issubclass(event, MovementEvent) and ENABLE_MOVEMENT_EVENTS:
            events.extend((event,) * MOVEMENT_EVENTS_FREQUENCY_MULTIPLIER)
        elif issubclass(event, VisualEvent) and ENABLE_VISUAL_EVENTS:
            events.extend((event,) * VISUAL_EVENTS_FREQUENCY_MULTIPLIER)
    return events
