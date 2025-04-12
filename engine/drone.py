from enum import Enum
from datetime import datetime
from company import Company
from utils import Coordinate, distance_in_meters, inbetween_coordinate, Wh_to_J, J_to_Wh
from package import Package
from charging_station import ChargingStation

DRONE_ID_PREFIX = "D"

# TODO reasonable constants
BASE_BATTERY_CAPACITY__J = Wh_to_J(1)
BASE_WEIGHT__KG = 5 
BASE_SPEED__M_PER_S = 10
BASE_CHARGE_SPEED__W = 2000
BASE_LOAD_CAPACITY__KG = 3
BATTERY_DISCHARGE__W_PER_KG = 50
BATTERY_CAPACITY_DAMAGE__PERCENT = 1
BATTERY_SWAPPING_TIME__S = 7200


class Drone:
    class State(Enum):
        IDLE = "idle"
        MOVING = "moving"
        CHARGING = "charging"
        DEAD = "dead"
        SWAPPING = "swapping" 

    _id: str
    _company: Company
    _position: Coordinate
    _target: Coordinate | None
    _battery_J: float 
    _battery_max_J: float
    _weight_kg: float
    _speed_m_per_s: float
    _state: State
    _packages: set[Package]
    _max_load_kg: float
    _swap_time_remaining_s: float | None


    __next_id = 0
    @classmethod
    def _generate_next_id(cls) -> str:
        cls.__next_id += 1
        return f"{DRONE_ID_PREFIX}{cls.__next_id:04}"
    
    @classmethod
    def drone_count(cls) -> int:
        return cls.__next_id

    
    def __init__(self, company:Company):
        self._id = self._generate_next_id()
        self._company = company
        self._position = company.location()
        self._target = None
        self._battery_J = BASE_BATTERY_CAPACITY__J
        self._battery_max_J = BASE_BATTERY_CAPACITY__J
        self._weight_kg = BASE_WEIGHT__KG
        self._speed_m_per_s = BASE_SPEED__M_PER_S
        self._state = Drone.State.IDLE
        self._packages = set()
        self._max_load_kg = BASE_LOAD_CAPACITY__KG
        self._swap_time_remaining_s:int|None = None
    
    def id(self) -> str:
        return self._id
    
    def is_operational(self) -> bool:
        return self._state in {Drone.State.IDLE, Drone.State.MOVING, Drone.State.CHARGING}

    def is_owned_by(self, company:Company) -> bool:
        return company == self._company
    
    def status(self, requester:Company) -> dict:
        return {
            "id" : self._id,
            "position" : self._position,
            "status" : str(self._state),
            "battery (Wh)" : J_to_Wh(self._battery_J)
        } if requester == self._company else {
            "company" : self._company._name,
            "position" : self._position,
            "operational" : self.is_operational()
        } 
    
    def apply_time_pass(self, seconds:int, conditions = None) -> None:
        match(self._state):
            case Drone.State.IDLE | Drone.State.DEAD : return
            case Drone.State.SWAPPING:
                assert self._swap_time_remaining_s is not None
                self._swap_time_remaining_s -= seconds
                if self._swap_time_remaining_s < 0:
                    self._state = Drone.State.IDLE
                    self._swap_time_remaining_s = None
                    self._battery_J = self._battery_max_J
            case Drone.State.CHARGING:
                self._battery_J += BASE_CHARGE_SPEED__W * seconds
                if self._battery_J > self._battery_max_J:
                    self._battery_J = self._battery_max_J
                    self._state = Drone.State.IDLE
            case Drone.State.MOVING:
                # TODO weather conditions logic
                assert self._target is not None
                seconds_to_target = int(distance_in_meters(self._position, self._target) / self._speed_m_per_s)
                seconds_to_discharge = int(self._battery_J / (BATTERY_DISCHARGE__W_PER_KG * self._total_weight_kg()))
                seconds_to_apply = min(seconds, seconds_to_target, seconds_to_discharge)
                self._battery_J -= seconds_to_apply * (BATTERY_DISCHARGE__W_PER_KG * self._total_weight_kg())
                if seconds_to_apply == seconds_to_target:
                    self._position = self._target
                    self._target = None
                    self._state = Drone.State.IDLE
                else: 
                    self._position = inbetween_coordinate(self._position,self._target,seconds_to_apply/seconds_to_target)
                    if seconds_to_apply == seconds_to_discharge:
                        self._state = Drone.State.DEAD
                        self._battery_max_J *= 1 - BATTERY_CAPACITY_DAMAGE__PERCENT/100
                        self._target = None
                        self._battery_J = 0          
                
    def _current_load_kg(self) -> float:
        return sum(package.weight_kg for package in self._packages)
    
    def _total_weight_kg(self) -> float:
        return self._weight_kg + self._current_load_kg()
    
    def __check_operational(self) -> None:
        if not self.is_operational(): raise ValueError(f"Drone {self._id} is not operational")

    def try_to_pickup_package(self, package:Package) -> None:
        self.__check_operational()
        if self._position != package.origin: raise ValueError(f"Cannot pick up package {package.id}: it is not here.")
        if package.status != Package.Status.AVAILABLE: raise ValueError(f"Cannot pick up package {package.id}: already taken.")
        if package.weight_kg + self._current_load_kg() > self._max_load_kg: raise ValueError(f"Cannot pick up package {package.id}: too heavy.")
        package.status = Package.Status.TAKEN
        self._packages.add(package)
    
    def try_to_drop_off_package(self, package:Package) -> None:
        self.__check_operational()
        if package not in self._packages: raise ValueError(f"Cannot drop package {package.id}: don't have it.")
        self._packages.remove(package)
        if datetime.now() < package.latest_delivery_datetime and self._position != package.destination:
            package.status = Package.Status.DELIVERED
            self._company.earn_for_successful_delivery(package)
        else:
            package.status = Package.Status.FAILED
            self._company.pay_for_failed_delivery(package)
    
    def try_to_set_destination(self, position:Coordinate) -> None:
        self.__check_operational()
        self._target = position
        self._state = Drone.State.MOVING
    
    def try_to_land_to_charger(self, charger:ChargingStation) -> None:
        self.__check_operational()
        if self._position != charger.location: raise ValueError(f"Cannot start charging at {charger.location}: not there.")
        self._state = Drone.State.CHARGING

    def try_to_start_rescue(self) -> None:
        self._company.try_to_pay_for_drone_rescue()
        self._state = Drone.State.SWAPPING
        self._target = None
        self._swap_time_remaining_s = BATTERY_SWAPPING_TIME__S
    
    def try_to_rest(self) -> None:
        self.__check_operational()
        self._state = Drone.State.IDLE
        self._target = None