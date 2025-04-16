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
    Coordinate(46.6834256, 17.6822392),
    Coordinate(46.7785356, 17.6593306),
    Coordinate(46.7103348, 17.2430825),
    Coordinate(46.7785224, 17.6595107)
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
    for _ in range(0):
        requests.post(
            "https://hackadrone.gazd.info/admin/add_drone", 
            json= { "company_id": team}, 
            headers=headers    
        )

