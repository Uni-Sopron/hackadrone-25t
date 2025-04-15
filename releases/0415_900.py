from engine.package import Package, generate_random_package, send_package_to_api
from engine.utils import Coordinate
import requests

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Api-Key": "5d8733d2-cc9b-48b2-9011-46ce3b1585b1"
}

GT = Coordinate(47.6800402, 16.5787537)
NC = Coordinate(47.6072494, 16.7054558) # Nagycenk, Szechenyi Kastely

requests.post(
    "https://hackadrone.gazd.info/admin/add_station", 
    json= {
        "location": NC, 
        "max_charging_speed_W": 100
    }, headers=headers    
)

# Short, cheap jobs around GT
for _ in range(10):
    send_package_to_api(generate_random_package(
        GT, 5000, 5000, 1, 2, 1000, 1200, 3600, 5400
    ))

# Longer, more expensive jobs around GT
for _ in range(5):
    send_package_to_api(generate_random_package(
        GT, 10000, 10000, 2, 3, 3000, 3500, 5400, 7200
    ))

# Short cheap jobs around NC (with longer deadlines)
for _ in range(5):
    send_package_to_api(generate_random_package(
        NC, 5000, 5000, 1, 2, 1000, 1200, 5400, 7200
    ))

# Expensive jobs, where origin is close to GT, destination is close to NC
# Weight is minimal, otherwise impossible
for _ in range(7):
    p = generate_random_package(
        GT, 1500, 1500, 0, 0.1, 5000, 6000, 7500, 9000
    )
    p.destination[0] += NC[0]-GT[0]
    p.destination[1] += NC[1]-GT[1]
    send_package_to_api(p)

# Same, just backwards
for _ in range(3):
    p = generate_random_package(
        NC, 1500, 1500, 0, 0.1, 5000, 6000, 7500, 9000
    )
    p.destination[0] += GT[0]-NC[0]
    p.destination[1] += GT[1]-NC[1]
    send_package_to_api(p)

