from .utils import Coordinate
from .entity import Entity

DEFAULT_CHARGING_SPEED__W = 120


class ChargingStation(Entity):
    ENTITY_ID_PREFIX = "S"

    def __init__(self, location: Coordinate, max_charging_speed_W: float|None = None):
        super().__init__()
        self.location = location
        self.max_charging_speed_W = max_charging_speed_W
        # TODO maybe later max charging speed / capacity   
        # TODO maybe later open hours logic

    def charging_speed_W(self) -> float:
        if self.max_charging_speed_W is None:
            return DEFAULT_CHARGING_SPEED__W
        else:
            return self.max_charging_speed_W

    def _public_status(self) -> dict:
        return {
            "id" : self._id,
            "location" : self.location,
            "max_charging_speed_W": self.max_charging_speed_W
        }