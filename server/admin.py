from flask import Blueprint

admin = Blueprint("api", __name__, url_prefix="/admin")


@admin.post("/add_company")
def add_company():
    # TODO
    return "Company added", 200


@admin.post("/add_drone")
def add_drone():
    # TODO
    return "Drone added", 200


@admin.post("/add_package")
def add_package():
    # TODO
    return "Package added", 200


@admin.post("/add_station")
def add_station():
    # TODO
    return "Station added", 200
