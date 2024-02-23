from typing import TypedDict


class GlobalVariables(TypedDict):
    tick: int
    masks: list['Mask']


GLOBAL_VARIABLES: GlobalVariables = GlobalVariables(tick=0, masks=[])
