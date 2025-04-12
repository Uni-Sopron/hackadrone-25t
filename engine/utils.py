from collections import namedtuple
from datetime import datetime

LATITUDE_SECOND_DISTANCE_M = 30.89
LONGITUDE_SECOND_DISTANCE_M = 20.79
LOGFILE = f"{datetime.now().isoformat()}.txt"


Coordinate = namedtuple('Coordinate', ['latitude', 'longitude'])

def distance_in_meters(pos1:Coordinate, pos2:Coordinate) -> float:
    return (
        (LATITUDE_SECOND_DISTANCE_M * (pos1.latitude - pos2.latitude)) ** 2 +
        (LONGITUDE_SECOND_DISTANCE_M * (pos1.longitude - pos2.longitude)) ** 2
    ) ** 0.5

def inbetween_coordinate(pos1:Coordinate, pos2:Coordinate, progress:float) -> Coordinate:
    return Coordinate(
        latitude = pos1.latitude * (1-progress) + pos2.latitude * progress,
        longitude = pos1.longitude * (1-progress) + pos2.longitude * progress
    )

def J_to_Wh(joules:float) -> float:
    return joules / 3600

def Wh_to_J(watthours:float) -> float:
    return watthours * 3600


def log(message:str):
    with open(LOGFILE, "a") as f:
        f.write(f"{datetime.now().isoformat()}: {message}\n")

def log_try(message:str):
    with open(LOGFILE, "a") as f:
        f.write(f"{datetime.now().isoformat()}: {message}... ")

def log_outcome(success:bool, message:str = ""):
    with open(LOGFILE, "a") as f:
        f.write(f" [{'SUCCESS' if success else 'FAILURE'}] {message}\n")

