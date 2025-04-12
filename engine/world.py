from company import Company
from drone import Drone
from package import Package
from utils import Coordinate, log, log_try, log_outcome
from datetime import datetime,timedelta
from typing import Any

class World:
    __entity_types = {Drone, Company, Package} # TODO Charging stations
    _entities: dict[type,dict[str,Any]]
    _last_event: datetime

    @staticmethod
    def now():
        return datetime.now().replace(microsecond=0)
        
    def __init__(self):
        self._entities = { type : {} for type in self.__entity_types }
        self._last_event = World.now()
    

    def _try_to_get_entity(self, entity:type, id:str) -> Any: 
        if id not in self._entities[entity]: raise ValueError(f"No {entity.__name__} with id {id}")
        return self._entities[entity][id]
    
    def status(self,company_name:str, entities:set[type]) -> dict[type,list[dict]]:
        self._apply_time_delay()
        try:
            company = self._try_to_get_entity(Company, company_name)
        except ValueError as e:
            return {"ERROR" : e.args[0]}
        return {
            entity.__name__ : [
                item.status(company)
                for item in self._entities[entity].values()
            ]
            for entity in entities # TODO does not work for anything besides Drone yet
        }

    def try_to_register_company(self, name:str, location:Coordinate) -> None:
        log_try(f" WORLD | REGISTER | trying to register {name} at {location}")
        if name in self._entities[Company]: 
            log_outcome(False, "Name already used.")
            raise ValueError(f"Company with name {name} already exists.")
        self._entities[Company][name] = Company(name, location)
        log_outcome(True)

    def action(self, action:dict) -> None:
        self._apply_time_delay()
        self._apply_action(action)
    
    def _apply_time_delay(self) -> None:
        time_delay:timedelta = World.now() - self._last_event
        log(f" WORLD | DELAY | {time_delay.total_seconds()} s") 
        if time_delay.total_seconds() > 0:
            self._last_event += time_delay
            for drone in self._entities[Drone].values():
                drone.apply_time_pass(int(time_delay.total_seconds()))
    
    def _try_to_get_coordinates(self, action:dict) -> Coordinate:
        try: [lat,lon] = action["coordinates"]
        except KeyError: raise ValueError("Missing coordinates.")
        except ValueError: raise ValueError(f"Incorrect coordinate format: {action['coordinates']}")
        return Coordinate(lat,lon)

    def _apply_action(self, action:dict) -> None:
        assert "company_id" in action
        log_try(f" WORLD | ACTION | trying {action}")
        try: 
            company:Company = self._try_to_get_entity(Company, action["company_id"])
            match(action):
                case {"action_type":"company", "company_id" : c_id, "action" : a}:
                    match(a):
                        case "new_drone": 
                            company.try_to_pay_for_new_drone()
                            new_drone:Drone = Drone(company)
                            self._entities[Drone][new_drone.id()] = new_drone
                        case "relocate":  company.try_to_relocate(self._try_to_get_coordinates(action))
                case {"action_type":"drone", "company_id": c_id, "drone_id" : d_id, "action" : a}:
                    drone:Drone = self._try_to_get_entity(Drone, d_id)
                    if not drone.is_owned_by(company): raise ValueError(f"Drone {d_id} is not owned by company {c_id}.")
                    match(a):
                        case "rest": drone.try_to_rest()
                        case "rescue": drone.try_to_start_rescue()
                        case "move": drone.try_to_set_destination(self._try_to_get_coordinates(action))
                        case "pickup_package" | "drop_package":
                            try: p_id:str = action["package_id"]
                            except KeyError: raise ValueError("Missing package id.")
                            package:Package = self._try_to_get_entity(Package, p_id)
                            if a == "pickup_package": drone.try_to_pickup_package(package)
                            elif a == "drop_package": drone.try_to_drop_off_package(package)
        except ValueError as e:
            log_outcome(False, e.args[0])
            raise e
        log_outcome(True)


    

