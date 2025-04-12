from time import sleep
from pprint import pprint

from .world import World
from .drone import Drone
from .utils import Coordinate


test = World()
test.try_to_register_company("Foo", Coordinate(1.2, 3.4))
sleep(1)
test.try_to_register_company("Bar", Coordinate(11.21, 13.41))
sleep(2)
for _ in range(1):
    sleep(0.7)
    try: 
        test.action({
            "action_type" : "company",
            "company_id" : "Foo",
            "action" : "new_drone"
        })
    except Exception as e:
        print(e)
test.action({
    "action_type" : "drone",
    "company_id" : "Foo",
    "drone_id" : "D0001",
    "action" : "move",
    "coordinates" : [100,100]
})

for _ in range(10):
    pprint(test.status("Foo", {Drone}))
    #print(test.status("Bar", {Drone}))
    sleep(2)
