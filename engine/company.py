from drone import *
from utils import *
from package import *

DRONE_PRICE__HUF = 40000
INITIAL_BALANCE__HUF = 1000000
FAILURE_PENALTY__PERCENT = 120 
DRONE_RESCUE_COST__HUF = 10000
RELOCATION_COST__HUF = 5000
 
class Company:
    _balance_HUF : int
    _drones :  dict[int,Drone]
    _name : str
    _base_location :Coordinate 

    def __init__(self, name:str, base_location:Coordinate):
        self._base_location = base_location
        self._name = name
        self._balance_HUF = INITIAL_BALANCE__HUF
        self._drones = {}
    
    def get_drone(self, drone_id:int) -> Drone:
        if drone_id not in self._drones: raise ValueError(f"Drone {drone_id} is not in the fleet.")
        return self._drones[drone_id]

    def try_to_buy_drone(self) -> Drone:
        if self._balance_HUF < DRONE_PRICE__HUF : raise ValueError("Cannot buy drone: not enough money.")
        drone = Drone(self,self._base_location)
        self._drones[drone._id] = drone
        return drone
    
    def earn_for_successful_delivery(self, package:Package) -> None:
        self._balance_HUF += package.revenue_HUF

    def pay_for_failed_delivery(self, package:Package) -> None:
        self._balance_HUF -= package.revenue_HUF * FAILURE_PENALTY__PERCENT // 100
    
    def try_to_pay_for_drone_rescue(self) -> None:
        if self._balance_HUF < DRONE_PRICE__HUF: raise ValueError("Cannot rescue drone: not enough money.")
        self._balance_HUF -= DRONE_PRICE__HUF
    
    def try_to_relocate(self, new_position:Coordinate) -> None:
        if self._balance_HUF < RELOCATION_COST__HUF: raise ValueError("Cannot relocate: not enough money.")
    

    




        



