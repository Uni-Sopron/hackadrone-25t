from enum import Enum
from datetime import datetime

from utils import *
from package import *
from charging_station import *

# TODO reasonable constants
BASE_BATTERY_CAPACITY__J = 1000 
BASE_WEIGHT__KG = 5 
BASE_SPEED__M_PER_S = 10
BASE_CHARGE_SPEED__W = 2000
BASE_LOAD_CAPACITY__KG = 3
BATTERY_DISCHARGE__W_PER_KG = 1
BATTERY_CAPACITY_DAMAGE__PERCENT = 1
BATTERY_SWAPPING_TIME__S = 7200
CLOSE_ENOUGH_DISTANCE__M = 1


class Drone:
    class State(Enum):
        IDLE = "idle"
        MOVING = "moving"
        CHARGING = "charging"
        DEAD = "dead"
        SWAPPING = "swapping" 

    _id: int
    _team_id: int
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
    def _generate_next_id(cls):
        cls.__next_id += 1
        return cls.__next_id
    
    @classmethod
    def drone_count(cls) -> int:
        return cls.__next_id

    
    def __init__(self, team_id:int, position:Coordinate):
        self._id = self._generate_next_id()
        self._team_id = team_id
        self._position = position
        self._target = None
        self._battery_J = BASE_BATTERY_CAPACITY__J
        self._battery_max_J = BASE_BATTERY_CAPACITY__J
        self._weight_kg = BASE_WEIGHT__KG
        self._speed_m_per_s = BASE_SPEED__M_PER_S
        self._state = Drone.State.IDLE
        self._packages = set()
        self._max_load_kg = BASE_LOAD_CAPACITY__KG
        self._swap_time_remaining_s:int|None = None
        #TODO company injection for money stuff
    
    def is_operational(self) -> bool:
        return self._state in {Drone.State.IDLE, Drone.State.MOVING, Drone.State.CHARGING}
    
    def close_enough(self, pos:Coordinate) -> bool:
        return distance_in_meters(self._position,pos) < CLOSE_ENOUGH_DISTANCE__M
    
    def apply_time_pass(self, seconds:int, conditions = None) -> None:
        match(self._state):
            case Drone.State.IDLE | Drone.State.DEAD : return
            case Drone.State.SWAPPING: 
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
                seconds_to_target:int = int(distance_in_meters(self._position, self._target) / self._speed_m_per_s)
                seconds_to_discharge:int = int(self._battery_J / (BATTERY_DISCHARGE__W_PER_KG * self._total_weight_kg()))
                seconds_to_apply:int = min(seconds, seconds_to_target, seconds_to_discharge)
                self._battery_max_J -= seconds_to_apply * (BATTERY_DISCHARGE__W_PER_KG * self._total_weight_kg())
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

    def pickup_package(self, package:Package) -> bool:
        if not self.is_operational(): return False
        if self._position != package.origin: return False
        if package.status != Package.Status.AVAILABLE: return False
        if package.weight_kg + self._current_load_kg() > self._max_load_kg: return False
        package.status = Package.Status.TAKEN
        self._packages.add(package)
        return True
        #TODO contract start logic
    
    def drop_off_package(self, package:Package) -> bool:
        if not self.is_operational(): return False
        if package not in self._packages: return False
        self._packages.remove(package)
        if datetime.now() < package.latest_delivery_datetime and self._position != package.destination:
            package.status = Package.Status.DELIVERED
            # TODO completion logic
        else:
            package.status = Package.Status.FAILED
            # TODO failed delivery logic
        return True
    
    def set_destination(self, position:Coordinate) -> bool:
        if not self.is_operational(): return False
        self._target = position
        self._state = Drone.State.MOVING
        return True
    
    def land_to_charger(self, charger:ChargingStation) -> bool:
        if not self.is_operational(): return False
        if self._position != charger.location: return False
        self._state = Drone.State.CHARGING
        return True

    def start_swap_waiting(self) -> None:
        self._state = Drone.State.SWAPPING
        self._target = None
        self._swap_time_remaining_s = BATTERY_SWAPPING_TIME__S
        # TODO swap cost logic
        


        







            
    

    