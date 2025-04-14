from datetime import datetime
from enum import Enum

from .utils import Coordinate, LATITUDE_SECOND_DISTANCE_M, LONGITUDE_SECOND_DISTANCE_M
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

from random import randrange, uniform, randint
from datetime import datetime, timedelta
def generate_random_package(
        center:Coordinate = Coordinate(47.6800454, 16.5795934),
        max_distance_origin_m:float = 20000,
        max_distance_destination_m:float = 20000,
        min_weight_kg:float = 1,
        max_weight_kg:float = 5,
        min_revenue_huf:int = 500,
        max_revenue_huf:int = 5000,
        min_delay_s:int = 1800,
        max_delay_s:int = 7200
) -> Package:
    return Package(
        Coordinate(
            center[0]+uniform(-1,1) * max_distance_origin_m / LATITUDE_SECOND_DISTANCE_M / 3600,
            center[1]+uniform(-1,1) * max_distance_origin_m / LONGITUDE_SECOND_DISTANCE_M / 3600
        ),
        Coordinate(
            center[0]+uniform(-1,1) * max_distance_destination_m / LATITUDE_SECOND_DISTANCE_M / 3600,
            center[1]+uniform(-1,1) * max_distance_destination_m / LONGITUDE_SECOND_DISTANCE_M / 3600
        ),
        uniform(min_weight_kg, max_weight_kg),
        randint(min_revenue_huf, max_revenue_huf),
        datetime.now().replace(microsecond=0) + timedelta(seconds=randint(min_delay_s, max_delay_s))
    )


if __name__ == "__main__":
    print(generate_random_package().get_status())
    print(generate_random_package().get_status())
    print(generate_random_package().get_status())