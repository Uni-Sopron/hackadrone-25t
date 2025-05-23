from uuid import uuid4

from .utils import Coordinate, log
from .package import Package
from .entity import Entity

DRONE_PRICE__HUF = 0
INITIAL_BALANCE__HUF = 10_000
FAILURE_PENALTY__PERCENT = 120
DRONE_RESCUE_COST__HUF = 10_000
RELOCATION_COST__HUF = 5_000


class Company(Entity):
    _balance_HUF : int
    _name : str
    _base_location : Coordinate 
    _secret : str

    def __init__(self, name:str, base_location:Coordinate):
        super().__init__()
        self._base_location = base_location
        self._name = name
        self._balance_HUF = INITIAL_BALANCE__HUF
        self._secret = str(uuid4())
    
    def location(self) -> Coordinate:
        return self._base_location
    
    def try_to_pay_for_new_drone(self) -> None:
        self._balance_HUF -= DRONE_PRICE__HUF
    
    def earn_for_successful_delivery(self, package:Package) -> None:
        self._balance_HUF += package.revenue_HUF

    def pay_for_failed_delivery(self, package:Package) -> None:
        self._balance_HUF -= package.revenue_HUF * FAILURE_PENALTY__PERCENT // 100
    
    def try_to_pay_for_drone_rescue(self) -> None:
        if self._balance_HUF < DRONE_RESCUE_COST__HUF: raise ValueError(f"Cannot rescue drone: not enough money. Balance: {self._balance_HUF}, cost: {DRONE_RESCUE_COST__HUF}.")
        self._balance_HUF -= DRONE_RESCUE_COST__HUF
    
    def pay_tariff(self, amount_HUF:int, reason:str):
        charge:int = min(self._balance_HUF, amount_HUF)
        if charge > 0:
            self._balance_HUF -= charge
            log(f"COMPANY | TARIFF | {self._name} charged {charge} HUF for: {reason}")

    
    def try_to_relocate(self, new_location:Coordinate) -> None:
        if self._balance_HUF < RELOCATION_COST__HUF: raise ValueError(f"Cannot relocate: not enough money. Balance: {self._balance_HUF}, cost: {RELOCATION_COST__HUF}.")
        self._balance_HUF -= RELOCATION_COST__HUF
        self._base_location = new_location

    def _can_access_private(self, **kargs) -> bool:
        return "company_id" in kargs and kargs["company_id"] == self._name
    
    def _public_status(self) -> dict:
        return {
            "company_name" : self._name,
            "base_location" : self._base_location
        }
    
    def _private_status(self) -> dict:
        return {
            "money_HUF" : self._balance_HUF
        }
