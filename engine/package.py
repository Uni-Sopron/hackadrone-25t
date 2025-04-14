from datetime import datetime
from enum import Enum

from .utils import Coordinate, TIMEFORMAT
from .entity import Entity


class Package(Entity):
    class Status(Enum):
        AVAILABLE = "available"
        TAKEN = "taken"
        DELIVERED = "delivered"
        FAILED = "failed"

    ENTITY_ID_PREFIX = "P"

    def __init__(
        self,
        origin: Coordinate,
        destination: Coordinate,
        weight_kg: float,
        revenue_HUF: int,
        latest_delivery_datetime: datetime,
    ) -> None:
        super().__init__()
        self.origin = origin
        self.destination = destination
        self.weight_kg = weight_kg
        self.revenue_HUF = revenue_HUF
        self.latest_delivery_datetime = latest_delivery_datetime
        self.status = Package.Status.AVAILABLE

    def _public_status(self) -> dict:
        return {
            "id": self._id,
            "status": self.status.value,
            "pick_up_location": self.origin,
            "drop_off_location": self.destination,
            "weight_kg": self.weight_kg,
            "revenue_HUF": self.revenue_HUF,
            "delivery_deadline": self.latest_delivery_datetime.isoformat(),
        }
