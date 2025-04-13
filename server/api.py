from http import HTTPStatus

from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.types import ResponseDict
from pydantic import BaseModel, Field

from .instance import world
from engine.world import Company, Drone, Package, ChargingStation

api = APIBlueprint("public api", __name__, url_prefix="/api")


class DroneRequest(BaseModel):
    company_id: str = Field(..., min_length=1)
    drone_id: str = Field(..., min_length=1)


class MoveRequest(DroneRequest):
    latitude: float = Field(..., ge=47, le=48)
    longitude: float = Field(..., ge=16, le=17)


class PackageRequest(DroneRequest):
    package_id: str = Field(..., min_length=1)


class StationRequest(DroneRequest):
    station_id: str = Field(..., min_length=1, description="Charging station ID")


responses: ResponseDict = {
    HTTPStatus.OK: None,
    HTTPStatus.BAD_REQUEST: None,
    HTTPStatus.NOT_FOUND: None,
    HTTPStatus.UNAUTHORIZED: None,
    HTTPStatus.FORBIDDEN: None,
}


@api.get("/state")
def state():
    """Get world state"""
    # TODO authentication for private data
    return world.status("", {Drone, Company, Package, ChargingStation})


@api.post("/move")
def move(body: MoveRequest):
    """Move the drone to a location"""
    action = {
        "action_type": "drone",
        "company_id": body.company_id,
        "drone_id": body.drone_id,
        "action": "move",
        "coordinates": [body.latitude, body.longitude],
    }
    try:
        world.action(action)
        return {}
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@api.post("/pickup", responses=responses)
def pickup(body: PackageRequest):
    """Pick up a package"""
    action = {
        "action_type": "drone",
        "company_id": body.company_id,
        "drone_id": body.drone_id,
        "action": "pickup_package",
        "package_id": body.package_id,
    }
    try:
        world.action(action)
        return {}
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@api.post("/drop", responses=responses)
def drop(body: PackageRequest):
    """Drop off a package"""
    action = {
        "action_type": "drone",
        "company_id": body.company_id,
        "drone_id": body.drone_id,
        "action": "drop_package",
        "package_id": body.package_id,
    }
    try:
        world.action(action)
        return {}
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@api.post("/charge", responses=responses)
def charge(body: StationRequest):
    """Charge the drone"""
    action = {
        "action_type": "drone",
        "company_id": body.company_id,
        "drone_id": body.drone_id,
        "action": "charge",
        "charging_station_id": body.station_id,
    }
    try:
        world.action(action)
        return {}
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@api.post("/rescue", responses=responses)
def rescue(body: DroneRequest):
    """Rescue the drone"""
    action = {
        "action_type": "drone",
        "company_id": body.company_id,
        "drone_id": body.drone_id,
        "action": "rescue",
    }
    try:
        world.action(action)
        return {}
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST


@api.post("/rest", responses=responses)
def rest(body: DroneRequest):
    """Rest the drone"""
    action = {
        "action_type": "drone",
        "company_id": body.company_id,
        "drone_id": body.drone_id,
        "action": "rest",
    }
    try:
        world.action(action)
        return {}
    except Exception as e:
        return {"error": str(e)}, HTTPStatus.BAD_REQUEST
