from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .utils import *
from .entity import Entity



@dataclass
class Package(Entity):
    class Status(Enum):
        AVAILABLE = "available"
        TAKEN = "taken"
        DELIVERED = "delivered"
        FAILED = "failed"

    id: str
    origin: Coordinate
    destination: Coordinate
    weight_kg: float
    revenue_HUF: int
    latest_delivery_datetime: datetime
    status:Status = Status.AVAILABLE

    def _public_status(self) -> dict:
        return {
            "id" : self.id,
            "status" : self.status.value,
            "pick-up location" : self.origin,
            "drop-off location" : self.destination,
            "weight (kg)" : self.weight_kg,
            "revenue (HUF)" : self.revenue_HUF,
            "delivery deadline" : self.latest_delivery_datetime.strftime(TIMEFORMAT)
        }