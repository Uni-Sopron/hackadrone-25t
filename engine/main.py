from world import World
from drone import Drone
from utils import Coordinate
from time import sleep




test = World()
test.try_to_register_company("Foo", Coordinate(1.2, 3.4))
sleep(1)
test.try_to_register_company("Bar", Coordinate(11.21, 13.41))
sleep(2)
for _ in range(3):
    sleep(0.7)
    try: 
        test.action({
            "action_type" : "company",
            "company_id" : "Foo",
            "action" : "new_drone"
        })
    except:
        pass
test.action({
    "action_type" : "drone",
    "company_id" : "Foo",
    "drone_id" : "D0001",
    "action" : "move",
    "coordinates" : [100,100]
})

for _ in range(10):
    print(test.status("Foo", {Drone}))
    #print(test.status("Bar", {Drone}))
    sleep(2)
