from engine.package import generate_random_package, send_package_to_api
from engine.utils import Coordinate
from random import sample, randint
import requests

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Api-Key": "5d8733d2-cc9b-48b2-9011-46ce3b1585b1"
}

new_stations = [
    Coordinate(47.5222976, 17.1670069),
    Coordinate(47.5220969, 17.3367343),
    Coordinate(47.7320954, 17.4826824),
    Coordinate(47.5487532, 17.5064925),
    Coordinate(47.3328947, 17.4641096),
    Coordinate(47.1698703, 17.3938651),
    Coordinate(46.9848056, 17.6956530),
    Coordinate(46.9139212, 17.8896240)
]

for station in new_stations:
    requests.post(
        "https://hackadrone.gazd.info/admin/add_station", 
        json= {
            "location": station, 
            "max_charging_speed_W": 400 + 30*randint(0,5)
        }, headers=headers    
    )


for team in ["Hubertus", "FoxDrone", "Karesz", "RoadRunnerExpress"]:
    for _ in range(3):
        requests.post(
            "https://hackadrone.gazd.info/admin/add_drone", 
            json= { "company_id": team}, 
            headers=headers    
        )

