from http import HTTPStatus

from flask_openapi3.blueprint import APIBlueprint
from flask_openapi3.models.tag import Tag
from flask_openapi3.types import ResponseDict
from pydantic import BaseModel, Field

from .instance import world
from engine.utils import Coordinate

ADMIN_APIDOC_VISIBLE = True

admin_tag = Tag(name="Admin Operations", description="Admin functionalities.")
admin = APIBlueprint(
    "api",
    __name__,
    url_prefix="/admin",
    abp_tags=[admin_tag],
    doc_ui=ADMIN_APIDOC_VISIBLE,
)


class ResponseModel(BaseModel):
    message: str


class CompanyBody(BaseModel):
    company_name: str = Field(..., min_length=1)
    base_location: Coordinate = Field(..., description="Latitude, longitude")


class DroneBody(BaseModel):
    company_id: str = Field(..., min_length=1)


responses: ResponseDict = {
    HTTPStatus.OK: ResponseModel,
    HTTPStatus.BAD_REQUEST: ResponseModel,
    HTTPStatus.UNAUTHORIZED: ResponseModel,
    HTTPStatus.FORBIDDEN: ResponseModel,
}


@admin.post("/add_company", responses=responses)
def add_company(body: CompanyBody):
    """Add a new company"""
    try:
        world.try_to_register_company(body.company_name, body.base_location)
    except ValueError as e:
        return {"message": str(e)}, HTTPStatus.BAD_REQUEST
    return {"message": "Company added"}  # TODO return secret key


@admin.post("/add_drone", responses=responses)
def add_drone(body: DroneBody):
    """Add a new drone"""
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


@admin.post("/add_package")
def add_package(body):
    """Add a new package"""
    # TODO
    return {"message": "Package added"}


@admin.post("/add_station")
def add_station():
    """Add a new charging station"""
    # TODO
    return {"message": "Station added"}


@admin.post("/set_scoreboard_visibility/<int:visible>")
def set_scoreboard_visibility(visible: int):
    """Set scoreboard visibility"""
    # TODO
    return {"message": "Scoreboard visibility set"}


@admin.post("/adjust_score")
def adjust_score():
    """Adjust score of a company"""
    # TODO
    return {"message": "Score adjusted"}
