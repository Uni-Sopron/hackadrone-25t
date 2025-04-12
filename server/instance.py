from engine.world import World
from engine.utils import Coordinate

world = World()

world.try_to_register_company("Foo", Coordinate(1.2, 3.4))

world.action({
    "action_type" : "company",
    "company_id" : "Foo",
    "action" : "new_drone"
})
