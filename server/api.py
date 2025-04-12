from http import HTTPStatus

from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.types import ResponseDict
from pydantic import BaseModel, Field

from .instance import world
from engine.drone import Drone

api = APIBlueprint("public api", __name__, url_prefix="/api")


@api.get("/state")
def state():
    """Get world state"""
    return world.status("Foo", { Drone })


class DroneBody(BaseModel):
    """Drone operation request body"""

    company_id: int = Field(..., ge=0)
    drone_id: int = Field(..., ge=0)


class MoveBody(DroneBody):
    """Move request body"""

    latitude: float = Field(..., ge=47, le=48)
    longitude: float = Field(..., ge=16, le=17)


class PackageBody(DroneBody):
    """Package operation request body"""

    package_id: int = Field(..., ge=0)


class StationBody(DroneBody):
    """Station operation request body"""

    station_id: int = Field(..., ge=0)


responses: ResponseDict = {
    HTTPStatus.OK: None,
    HTTPStatus.BAD_REQUEST: None,
    HTTPStatus.NOT_FOUND: None,
    HTTPStatus.UNAUTHORIZED: None,
    HTTPStatus.FORBIDDEN: None,
}


@api.post("/move")
def move(body: MoveBody):
    """Move the drone to a location"""
    # TODO
    return {}


@api.post("/pickup", responses=responses)
def pickup(body: PackageBody):
    """Pick up a package"""
    # TODO
    return ""


@api.post("/drop", responses=responses)
def drop(body: PackageBody):
    """Drop off a package"""
    # TODO
    return ""


@api.post("/charge", responses=responses)
def charge(body: StationBody):
    """Charge the drone"""
    # TODO
    return ""


@api.post("/rescue", responses=responses)
def rescue(body: DroneBody):
    """Rescue the drone"""
    # TODO
    return ""
