from engine.package import generate_random_package, send_package_to_api
from engine.utils import Coordinate
from random import sample, randint
import requests

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Api-Key": "5d8733d2-cc9b-48b2-9011-46ce3b1585b1"
}

GT = Coordinate(47.6800402, 16.5787537) # GT
NC = Coordinate(47.6072494, 16.7054558) # Nagycenk - Szechenyi kastely
HK = Coordinate(47.6455318, 16.6039671) # Harka
FE = Coordinate(47.6203015, 16.8718423) # Fertod - Eszterhazy kastely

requests.post(
    "https://hackadrone.gazd.info/admin/add_station", 
    json= {
        "location": FE, 
        "max_charging_speed_W": 130
    }, headers=headers    
)


for team in ["Hubertus", "FoxDrone", "Karesz", "RoadRunnerExpress"]:
    requests.post(
        "https://hackadrone.gazd.info/admin/add_drone", 
        json= { "company_id": team}, 
        headers=headers    
    )


stations = [GT,NC, HK, FE]

for station in stations:
    for _ in range(randint(2,4)):
        send_package_to_api(generate_random_package(
            station, 4000, 4000, 1, 2, 1000, 1200, 3600, 5400
        ))

for station in stations:
    for _ in range(randint(2,4)):
        send_package_to_api(generate_random_package(
            station, 7000, 7000, 2, 3, 3000, 3500, 5400, 7200
        ))

for _ in range(randint(4,6)):
    [origin,destination] = sample(stations, k=2)
    p = generate_random_package(
        origin, 1000, 1000, 0, 0.1, 5000, 6000, 7500, 9000
    )
    p.destination = Coordinate(p.destination[0] + destination[0] - origin[0], p.destination[1] + destination[1] - origin[1])
    send_package_to_api(p)
