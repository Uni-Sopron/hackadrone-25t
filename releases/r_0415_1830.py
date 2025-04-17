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
    Coordinate(47.5335849, 16.6476689),
    Coordinate(47.5648821, 16.7705489),
    Coordinate(47.4848336, 16.7428457),
    Coordinate(47.4244592, 16.8421340),
    Coordinate(47.4412848, 16.9086858),
    Coordinate(47.4861614, 16.8997100),
    Coordinate(47.5870458, 16.4682568),
    Coordinate(47.5132862, 16.5710507)
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
    for _ in range(7):
        requests.post(
            "https://hackadrone.gazd.info/admin/add_drone", 
            json= { "company_id": team}, 
            headers=headers    
        )

