from company import *
from drone import *
from datetime import datetime,timedelta

class World:
    _companies: dict[str,Company]
    _drones: list[Drone]
    _last_event: datetime


    def action(self, action:dict) -> None:
        time_delay:timedelta = datetime.now() - self._last_event 
        self._last_event += time_delay
        for drone in self.drones:
            drone.apply_time_pass(timedelta.seconds)
        
    def _get_company(self, company_id:int) -> Company:
        if company_id not in self._companies: raise ValueError(f"No company with id {company_id}")
        return self._companies[company_id]

    def _apply_action(self, action:dict) -> None:
        match(action):
            case {"action_type":"company", "company_id" : c_id, "action" : a}:
                company:Company = self._get_company(c_id)
                match(a):
                    case "new_drone": company.buy_drone()
            case {"action_type":"drone", "company_id": c_id, "drone_id" : d_id, "action" : a}:
                company:Company = self._get_company(c_id)
                drone:Drone = company.get_drone(d_id)
                match(a):
                    case "move": 
                        pass
                    case "rescue":
                        pass
                    case "rest":
                        pass
                    case "pickup_package":
                        pass
                    case "drop_package":
                        pass


    

