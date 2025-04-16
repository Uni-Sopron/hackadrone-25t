from http import HTTPStatus

from flask import request
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.types import ResponseDict
from pydantic import BaseModel, Field

from .instance import world
from engine.tariffs import API_REQUEST_COST_HUF
from engine.world import Company, Drone, Package, ChargingStation

api = APIBlueprint("public api", __name__, url_prefix="/api")


class StateRequest(BaseModel):
    company_id: str = Field(..., min_length=1)


class DroneRequest(BaseModel):
    company_id: str = Field(..., min_length=1)
    drone_id: str = Field(..., min_length=1)


class MoveRequest(DroneRequest):
    latitude: float
    longitude: float


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

security = [{"Api-Key": []}]


def authenticate(company_id: str, api_key: str):
    """Authenticate the company"""
    try:
        found_company = world._try_to_get_entity(Company, company_id)
        assert isinstance(found_company, Company)
        found_company.pay_tariff(API_REQUEST_COST_HUF, "API request")
    except ValueError:
        return {"error": "Company not found"}, HTTPStatus.NOT_FOUND
    assert isinstance(found_company, Company)
    if api_key != found_company._secret:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    return HTTPStatus.OK


# @api.get("/state")
# def public_state():
#     """Get world state (public)"""
#     return world.status("", {Drone, Company, Package, ChargingStation})


@api.get("/state/<string:company_id>", security=security)
def state(path: StateRequest):
    """Get world knowledge of a company"""
    auth_response = authenticate(path.company_id, request.headers.get("Api-Key", ""))
    if auth_response != HTTPStatus.OK:
        return auth_response
    return world.status(path.company_id, {Drone, Company, Package, ChargingStation})


@api.post("/move", security=security)
def move(body: MoveRequest):
    """Move the drone to a location"""
    auth_response = authenticate(body.company_id, request.headers.get("Api-Key", ""))
    if auth_response != HTTPStatus.OK:
        return auth_response
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


@api.post("/pickup", responses=responses, security=security)
def pickup(body: PackageRequest):
    """Pick up a package"""
    auth_response = authenticate(body.company_id, request.headers.get("Api-Key", ""))
    if auth_response != HTTPStatus.OK:
        return auth_response
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


@api.post("/drop", responses=responses, security=security)
def drop(body: PackageRequest):
    """Drop off a package"""
    auth_response = authenticate(body.company_id, request.headers.get("Api-Key", ""))
    if auth_response != HTTPStatus.OK:
        return auth_response
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


@api.post("/charge", responses=responses, security=security)
def charge(body: StationRequest):
    """Charge the drone"""
    auth_response = authenticate(body.company_id, request.headers.get("Api-Key", ""))
    if auth_response != HTTPStatus.OK:
        return auth_response
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


@api.post("/rescue", responses=responses, security=security)
def rescue(body: DroneRequest):
    """Rescue the drone"""
    auth_response = authenticate(body.company_id, request.headers.get("Api-Key", ""))
    if auth_response != HTTPStatus.OK:
        return auth_response
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


@api.post("/rest", responses=responses, security=security)
def rest(body: DroneRequest):
    """Rest the drone"""
    auth_response = authenticate(body.company_id, request.headers.get("Api-Key", ""))
    if auth_response != HTTPStatus.OK:
        return auth_response
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
