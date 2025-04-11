from drone import *
from utils import *
from package import *

DRONE_PRICE__HUF = 40000
INITIAL_BALANCE__HUF = 1000000
FAILURE_PENALTY__PERCENT = 120 
DRONE_RESCUE_COST__HUF = 10000

class Company:
    _balance_HUF : int
    _drones :  dict[int,Drone]
    _name : str
    _base_location :Coordinate # maybe not necessary


    def __init__(self, name:str, base_location:Coordinate):
        self._base_location = base_location
        self._name = name
        self._balance_HUF = INITIAL_BALANCE__HUF
        self._drones = {}

    def buy_drone(self) -> int|None:
        if self._balance_HUF < DRONE_PRICE__HUF : return None
        drone = Drone(self,self._base_location)
        self._drones[drone._id, drone]
        return drone._id
    
    def complete_package_delivery(self, package:Package) -> None:
        self._balance_HUF += package.revenue_HUF

    def fail_package_delivery(self, package:Package) -> None:
        self._balance_HUF -= package.revenue_HUF * FAILURE_PENALTY__PERCENT // 100
    
    def order_drone_rescue(self) -> bool:
        if self._balance_HUF < DRONE_PRICE__HUF: return False
        self._balance_HUF -= DRONE_PRICE__HUF
        return True
    
    def get_drone(self, drone_id:int) -> Drone|None :
        return self._drones.get(drone_id, None)
    

    




        



