import os
from datetime import datetime
from http import HTTPStatus

from flask import request
from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from flask_openapi3.types import ResponseDict
from pydantic import BaseModel, Field

from .instance import world
from engine.charging_station import DEFAULT_CHARGING_SPEED__W
from engine.package import Package, generate_random_package
from engine.utils import Coordinate

ADMIN_APIDOC_VISIBLE = bool(int(os.getenv("ADMIN_APIDOC_VISIBLE", "0")))
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")
if not ADMIN_API_KEY:
    raise ValueError("ADMIN_API_KEY environment variable is not set.")

admin_tag = Tag(name="Admin Operations", description="Admin functionalities.")
admin = APIBlueprint(
    "api",
    __name__,
    url_prefix="/admin",
    abp_tags=[admin_tag],
    doc_ui=ADMIN_APIDOC_VISIBLE,
    abp_security=[{"Api-Key": []}],
)


class ResponseModel(BaseModel):
    message: str


class CompanyBody(BaseModel):
    company_name: str = Field(..., min_length=1)
    base_location: Coordinate = Field(..., description="Latitude, longitude")

class DonationBody(BaseModel):
    company_name: str = Field(..., min_length=1)
    amount_huf: int

class DroneBody(BaseModel):
    company_id: str = Field(..., min_length=1)


class PackageBody(BaseModel):
    origin: Coordinate
    destination: Coordinate
    weight_kg: float
    revenue_HUF: int
    latest_delivery_datetime: datetime = datetime(2025, 4, 18, 0, 0, 0)


class GenPackageBody(BaseModel):
    center: Coordinate
    max_distance_origin_m: float = Field(20000)
    max_distance_destination_m: float = Field(20000)
    min_weight_kg: float = Field(1)
    max_weight_kg: float = Field(5)
    min_revenue_huf: int = Field(500)
    max_revenue_huf: int = Field(5000)
    min_delay_s: int = Field(1800)
    max_delay_s: int = Field(7200)


class StationBody(BaseModel):
    location: Coordinate
    max_charging_speed_W: float = Field(
        DEFAULT_CHARGING_SPEED__W, ge=0, description="Charging speed in W"
    )


responses: ResponseDict = {
    HTTPStatus.OK: ResponseModel,
    HTTPStatus.BAD_REQUEST: ResponseModel,
    HTTPStatus.UNAUTHORIZED: ResponseModel,
    HTTPStatus.FORBIDDEN: ResponseModel,
}


@admin.get("/status", responses=responses)
def status():
    """Get admin status"""
    try:
        state = world.admin_status()
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return state, HTTPStatus.OK


@admin.post("/add_company", responses=responses)
def add_company(body: CompanyBody):
    """Add a new company"""
    if request.headers.get("Api-Key", "") != ADMIN_API_KEY:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    try:
        api_key = world.try_to_register_company(body.company_name, body.base_location)
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": f"Company added, {api_key=}"}


@admin.post("/add_drone", responses=responses)
def add_drone(body: DroneBody):
    """Add a new drone"""
    if request.headers.get("Api-Key", "") != ADMIN_API_KEY:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    try:
        world.action(
            {
                "action_type": "company",
                "action": "new_drone",
                "company_id": body.company_id,
            }
        )
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": "Drone added"}


@admin.post("/add_package", responses=responses)
def add_package(body: PackageBody):
    """Add a new package"""
    if request.headers.get("Api-Key", "") != ADMIN_API_KEY:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    if body.origin == body.destination:
        return {
            "message": "Origin and destination cannot be the same"
        }, HTTPStatus.BAD_REQUEST
    package = Package(
        origin=body.origin,
        destination=body.destination,
        weight_kg=body.weight_kg,
        revenue_HUF=body.revenue_HUF,
        latest_delivery_datetime=body.latest_delivery_datetime,
    )
    try:
        world.try_to_advertise_package(package)
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": f"Package {package._id} added"}



@admin.post("/gen_packages", responses=responses)
def gen_packages(body: GenPackageBody):
    """Generate packages based on the provided parameters."""
    if request.headers.get("Api-Key", "") != ADMIN_API_KEY:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    try:
        package = generate_random_package(
            center=body.center,
            max_distance_origin_m=body.max_distance_origin_m,
            max_distance_destination_m=body.max_distance_destination_m,
            min_weight_kg=body.min_weight_kg,
            max_weight_kg=body.max_weight_kg,
            min_revenue_huf=body.min_revenue_huf,
            max_revenue_huf=body.max_revenue_huf,
            min_delay_s=body.min_delay_s,
            max_delay_s=body.max_delay_s
        )
        world.try_to_advertise_package(package)
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": f"Package {package._id} generated and added"}


@admin.post("/add_station", responses=responses)
def add_station(body: StationBody):
    """Add a new charging station"""
    if request.headers.get("Api-Key", "") != ADMIN_API_KEY:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    try:
        world.try_to_add_charging_station(body.location, body.max_charging_speed_W)
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": "Station added"}


@admin.post("/set_scoreboard_visibility/<int:visible>", responses=responses)
def set_scoreboard_visibility(visible: int):
    """Set scoreboard visibility"""
    if request.headers.get("Api-Key", "") != ADMIN_API_KEY:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    # TODO
    return {"message": "Scoreboard visibility set"}


@admin.post("/donate", responses=responses)
def donate(body: DonationBody):
    """Donate money to a company"""
    if request.headers.get("Api-Key", "") != ADMIN_API_KEY:
        return {"error": "Invalid API key"}, HTTPStatus.UNAUTHORIZED
    try:
        world.donate(body.company_name, body.amount_huf)
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": "Money donated."}
