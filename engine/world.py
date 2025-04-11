from company import Company
from drone import Drone
from package import Package
from utils import Coordinate
from datetime import datetime,timedelta

class World:
    _companies: dict[str,Company]
    _drones: list[Drone]
    _packages: dict[str,Package]
    _last_event: datetime

    def action(self, action:dict) -> None:
        self._apply_time_delay()
        self._apply_action(action)
    
    def _apply_time_delay(self) -> None:
        time_delay:timedelta = datetime.now() - self._last_event 
        self._last_event += time_delay
        for drone in self._drones:
            drone.apply_time_pass(int(time_delay.total_seconds()))
        
    def _try_to_get_company(self, company_id:str) -> Company:
        if company_id not in self._companies: raise ValueError(f"No company with id {company_id}")
        return self._companies[company_id]
    
    def _try_to_get_coordinates(self, action:dict) -> Coordinate:
        try: [lat,lon] = action["coordinates"]
        except KeyError: raise ValueError("Missing coordinates.")
        except ValueError: raise ValueError(f"Incorrenct coordinate format: {action['coordinates']}")
        return Coordinate(lat,lon)

    def _apply_action(self, action:dict) -> None:
        assert "company_id" in action
        company:Company = self._try_to_get_company(action["company_id"])
        match(action):
            case {"action_type":"company", "company_id" : c_id, "action" : a}:
                match(a):
                    case "new_drone": self._drones.append(company.try_to_buy_drone())
                    case "relocate":  company.try_to_relocate(self._try_to_get_coordinates(action))
            case {"action_type":"drone", "company_id": c_id, "drone_id" : d_id, "action" : a}:
                drone:Drone = company.get_drone(d_id)
                match(a):
                    case "rest": drone.try_to_rest()
                    case "rescue": drone.try_to_start_rescue()
                    case "move": drone.try_to_set_destination(self._try_to_get_coordinates(action))
                    case "pickup_package" | "drop_package":
                        try: p_id:str = action["package_id"]
                        except KeyError: raise ValueError("Missing package id.")
                        try: package:Package = self._packages[p_id]
                        except KeyError: raise ValueError(f"Package with id {p_id} does not exist.")
                        if a == "pickup_package": drone.try_to_pickup_package(package)
                        elif a == "drop_package": drone.try_to_drop_off_package(package)


    

