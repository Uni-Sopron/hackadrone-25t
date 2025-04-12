from .utils import *
from dataclasses import dataclass


DEFAULT_CHARGING_SPEED__W = 20

@dataclass
class ChargingStation:
    id: str
    location: Coordinate
    max_charging_speed_W: float|None
    # TODO maybe later max charging speed / capacity   
    # TODO maybe later open hours logic

    def charging_speed_W(self) -> float:
        if self.max_charging_speed_W is None: return DEFAULT_CHARGING_SPEED__W
        else: return self.charging_speed_W 
