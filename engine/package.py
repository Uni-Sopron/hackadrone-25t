from utils import *
from dataclasses import dataclass
from datetime import datetime
from enum import Enum




@dataclass
class Package:
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
