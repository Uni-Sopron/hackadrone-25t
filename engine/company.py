from utils import Coordinate
from package import Package

DRONE_PRICE__HUF = 40000
INITIAL_BALANCE__HUF = 100000
FAILURE_PENALTY__PERCENT = 120 
DRONE_RESCUE_COST__HUF = 10000
RELOCATION_COST__HUF = 5000
 
class Company:
    _balance_HUF : int
    _name : str
    _base_location : Coordinate 

    def __init__(self, name:str, base_location:Coordinate):
        self._base_location = base_location
        self._name = name
        self._balance_HUF = INITIAL_BALANCE__HUF
    
    def location(self) -> Coordinate:
        return self._base_location
    
    def try_to_pay_for_new_drone(self) -> None:
        if self._balance_HUF < DRONE_PRICE__HUF : raise ValueError("Cannot buy drone: not enough money.")
        self._balance_HUF -= DRONE_PRICE__HUF
    
    def earn_for_successful_delivery(self, package:Package) -> None:
        self._balance_HUF += package.revenue_HUF

    def pay_for_failed_delivery(self, package:Package) -> None:
        self._balance_HUF -= package.revenue_HUF * FAILURE_PENALTY__PERCENT // 100
    
    def try_to_pay_for_drone_rescue(self) -> None:
        if self._balance_HUF < DRONE_PRICE__HUF: raise ValueError("Cannot rescue drone: not enough money.")
        self._balance_HUF -= DRONE_PRICE__HUF
    
    def try_to_relocate(self, new_location:Coordinate) -> None:
        if self._balance_HUF < RELOCATION_COST__HUF: raise ValueError("Cannot relocate: not enough money.")
        self._balance_HUF -= RELOCATION_COST__HUF
        self._base_location = new_location
    

    




        



