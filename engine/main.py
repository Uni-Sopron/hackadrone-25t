from world import World
from utils import Coordinate
from time import sleep




test = World()
test.try_to_register_company("Foo", Coordinate(1.2, 3.4))
sleep(1)
test.try_to_register_company("Bar", Coordinate(11.21, 13.41))
sleep(2)
for _ in range(5):
    sleep(0.7)
    try: 
        test.action({
            "action_type" : "company",
            "company_id" : "Foo",
            "action" : "new_drone"
        })
    except:
        pass