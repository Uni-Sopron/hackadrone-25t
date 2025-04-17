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
    Coordinate(47.3260315, 16.6478123),
    Coordinate(47.2053730, 16.6731840),
    Coordinate(47.1636374, 16.8676667),
    Coordinate(46.7706843, 17.2423323),
    Coordinate(46.5799974, 17.4078843),
    Coordinate(46.7885654, 17.3770372)
]

for station in new_stations:
    requests.post(
        "https://hackadrone.gazd.info/admin/add_station", 
        json= {
            "location": station, 
            "max_charging_speed_W": 100 + 10*randint(0,5)
        }, headers=headers    
    )


for team in ["Hubertus", "FoxDrone", "Karesz", "RoadRunnerExpress"]:
    for _ in range(2):
        requests.post(
            "https://hackadrone.gazd.info/admin/add_drone", 
            json= { "company_id": team}, 
            headers=headers    
        )

