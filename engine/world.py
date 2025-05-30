from datetime import datetime, timedelta
import os
from typing import cast
from random import choice, uniform, sample
import pickle

from .company import Company
from .drone import BATTERY_DISCHARGE__W_PER_KG, Drone
from .package import Package, generate_random_package
from .charging_station import ChargingStation
from .utils import Coordinate, log, log_try, log_outcome, TIMEFORMAT
from .entity import Entity

BACKUP_DIR = "instance"
BACKUP_COUNT = 5


class World:
    __entity_types = {Drone, Company, Package, ChargingStation}
    _entities: dict[type, dict[str, Entity]]
    _last_event: datetime

    @staticmethod
    def now():
        return datetime.now().replace(microsecond=0)

    def __init__(self):
        self._entities = {type: {} for type in self.__entity_types}
        self._last_event = World.now()
        os.makedirs(BACKUP_DIR, exist_ok=True)

    def _try_to_get_entity(self, entity: type, id: str) -> Entity:
        if id not in self._entities[entity]:
            raise ValueError(f"No {entity.__name__} with id {id}")
        return self._entities[entity][id]
    
    def donate(self, company_name: str, amount_HUF: int) -> None:
        company: Company = cast(Company, self._try_to_get_entity(Company, company_name))
        company._balance_HUF += amount_HUF
        log(f" WORLD | COMPANY | DONATE | Balance of {company_name} increased by {amount_HUF} HUF to {company._balance_HUF} HUF.")

    def status(self, company_name: str, entities: set[type]) -> dict[str, list[dict]]:
        self._apply_time_delay()
        self._maintain_minimum_package_count()
        log(f"WORLD | COMPANY | STATUS | Company {company_name} asked for status.")
        return {
            entity.__name__: [
                item.get_status(company_id=company_name)
                for item in self._entities[entity].values()
            ]
            for entity in entities
        }
    
    def admin_status(self):
        return {
            "teams": [
                { "teams_id": team_id, "name": team_id, "score": team._balance_HUF }
                for team_id, team in self._entities[Company].items() if isinstance(team,Company)
            ],
            "drones": [
                {
                "drone_id": drone_id,
                "team_id": drone._company._name,
                "operational" : drone.is_operational(),
                "state" : drone._state.value,
                "position": {
                    "latitude": drone._position[0],
                    "longitude": drone._position[1]
                },
                "source": {
                    "latitude": drone._position[0],
                    "longitude": drone._position[1]
                },
                "destination": {
                    "latitude": drone._target[0] if drone._state == Drone.State.MOVING else drone._position[0],
                    "longitude": drone._target[1] if drone._state == Drone.State.MOVING else drone._position[1]
                },
                "battery": drone._battery_J / drone._battery_max_J,
                "battery_remaining_s": drone._battery_J / (BATTERY_DISCHARGE__W_PER_KG * drone._total_weight_kg()),
                "swapping_time_remaining_s" : drone._swap_time_remaining_s if drone._swap_time_remaining_s is not None else None,
                "payload_capacity": drone._max_load_kg,
                "current_payload": drone._total_weight_kg(),
                "packages": [
                    {
                        "package_id": package._id,
                        "weight": package.weight_kg,
                        "destination": {
                            "latitude": package.destination[0],
                            "longitude": package.destination[1]
                        },
                        "deadline": package.latest_delivery_datetime.isoformat(),
                        "reward": package.revenue_HUF,
                        "contractor": package.contractor._name if isinstance(package.contractor, Company) else None,
                    }
                    for package in drone._packages if isinstance(package, Package)
                ]
                }
                for drone_id, drone in self._entities[Drone].items() if isinstance(drone,Drone)
            ],
            "packages": [
                {
                    "package_id": package_id,
                    "weight": package.weight_kg,
                    "position": {
                        "latitude": package.origin[0],
                        "longitude": package.origin[1]
                    },
                    "destination": {
                        "latitude": package.destination[0],
                        "longitude": package.destination[1]
                    },
                    "reward": package.revenue_HUF,
                    "deadline": package.latest_delivery_datetime.isoformat(),
                    "contractor": package.contractor._name if isinstance(package.contractor, Company) else None,
                }
                for package_id, package in self._entities[Package].items()
                if isinstance(package, Package) and package.status == Package.Status.AVAILABLE
            ],
            "chargingStations": [
                {
                "station_id": station_id,
                "position": {
                    "latitude": station.location[0],
                    "longitude": station.location[1]
                },
                "charging_speed": station.charging_speed_W()
                }
                for station_id, station in self._entities[ChargingStation].items()
                if isinstance(station,ChargingStation)
            ]
            }

    def try_to_register_company(self, name: str, location: Coordinate) -> str:
        log_try(f" WORLD | REGISTER | trying to register {name} at {location}")
        if name in self._entities[Company]:
            log_outcome(False, "Name already used.")
            raise ValueError(f"Company with name {name} already exists.")
        company = Company(name, location)
        self._entities[Company][name] = company
        log_outcome(True)
        return company._secret

    def try_to_add_charging_station(
        self, location: Coordinate, max_charging_speed_W: float | None = None
    ) -> None:
        log_try(
            f" WORLD | ADD CHARGING STATION | trying to add charging station at {location}"
        )
        station = ChargingStation(location, max_charging_speed_W)
        self._entities[ChargingStation][station._id] = station
        log_outcome(True)

    def try_to_close_down_charging_station(self, name: str) -> None:
        log_try(
            f" WORLD | CLOSE CHARGING STATION | trying to close charging station {name}"
        )
        if name not in self._entities[ChargingStation]:
            log_outcome(False, "Station does not exist.")
            raise ValueError(f"Charging station with id {name} does not exist.")
        del self._entities[ChargingStation][name]
        log_outcome(True)

    def try_to_advertise_package(self, package: Package) -> None:
        log_try(f" WORLD | ADD PACKAGE | trying to advertise package station {package}")
        if package._id in self._entities[Package]:
            log_outcome(False, "Package already advertised.")
            raise ValueError("Package already advertised.")
        if package.latest_delivery_datetime <= World.now():
            log_outcome(False, "Deadline already over.")
            raise ValueError("Deadline already over.")
        self._entities[Package][package._id] = package
        log_outcome(True)
    
    def _generate_random_package(self) -> Package:
        roll:float = uniform(0,10)
        station:Coordinate = cast(ChargingStation, choice(list(self._entities[ChargingStation].values()))).location
        if roll < 5: # small local package
            return generate_random_package(station, 4000, 4000, 1, 2, 2000, 2400, 3600, 5400)
        elif roll < 9: # large local package
            return generate_random_package(station, 7000, 7000, 2, 3, 3000, 3500, 5400, 7200)
        else: # package between charging stations
            [station, station2] = [cast(ChargingStation, s).location for s in sample(list(self._entities[ChargingStation].values()), k=2)]
            p = generate_random_package(station, 1000, 1000, 1, 4, 5000, 6000, 7500, 9000)
            p.destination = Coordinate(p.destination[0] + station2[0] - station[0], p.destination[1] + station2[1] - station[1])
            return p
    
    def _maintain_minimum_package_count(self):
        package_count:int = len(self._entities[Package])
        needed_packages:int =  3 * len(self._entities[Drone])
        if package_count <  needed_packages:
            for _ in range(int(needed_packages*1.2) - package_count):
                self.try_to_advertise_package(self._generate_random_package())

    def action(self, action: dict) -> None:
        self._apply_time_delay()
        self._apply_action(action)
        self.backup(True)

    def backup(self, force=False) -> None:
        backups = [f for f in os.scandir(BACKUP_DIR)]
        backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        if (
            force
            or len(backups) < BACKUP_COUNT
            or World.now() - datetime.fromtimestamp(backups[0].stat().st_mtime)
            < timedelta(minutes=10)
        ):
            with open(
                f"{BACKUP_DIR}/{World.now().strftime(TIMEFORMAT)}.pkl", "wb"
            ) as file:
                pickle.dump(self, file)
        if len(backups) + 1 > BACKUP_COUNT:
            for f in backups[BACKUP_COUNT:]:
                os.remove(f.path)

    def _apply_time_delay(self) -> None:
        time_delay: timedelta = World.now() - self._last_event
        if time_delay.total_seconds() > 0:
            log(f" WORLD | DELAY | {time_delay.total_seconds()} s")
            self._last_event += time_delay
            for drone in self._entities[Drone].values():
                cast(Drone, drone).apply_time_pass(int(time_delay.total_seconds()))
            for id in list(self._entities[Package]):
                package: Package = cast(Package,self._entities[Package][id])
                if (package.status in {Package.Status.FAILED, Package.Status.DELIVERED}): 
                    del self._entities[Package][id]
                elif (package.status == Package.Status.AVAILABLE and package.latest_delivery_datetime < World.now()):
                    if (package.contractor is not None): 
                        cast(Company, package.contractor).pay_for_failed_delivery(package)
                    del self._entities[Package][id]
                elif (package.status == Package.Status.AVAILABLE and package.latest_delivery_datetime < World.now() + timedelta(minutes = 45)):
                    if not hasattr(package, "increased_revenue"):
                        setattr(package, "increased_revenue", True)
                        package.revenue_HUF *= 3
                        package.latest_delivery_datetime += timedelta(minutes=20)
            self.backup()

    def _try_to_get_coordinates(self, action: dict) -> Coordinate:
        try:
            [lat, lon] = action["coordinates"]
        except KeyError:
            raise ValueError("Missing coordinates.")
        except ValueError:
            raise ValueError(f"Incorrect coordinate format: {action['coordinates']}")
        return Coordinate(lat, lon)

    def _apply_action(self, action: dict) -> None:
        assert "company_id" in action
        log_try(f" WORLD | ACTION | trying {action}")
        try: 
            company:Company = cast(Company,self._try_to_get_entity(Company, action["company_id"]))
            match action:
                case {"action_type": "company", "company_id": c_id, "action": a}:
                    match a:
                        case "new_drone":
                            company.try_to_pay_for_new_drone()
                            new_drone: Drone = Drone(company)
                            self._entities[Drone][new_drone.id()] = new_drone
                        case "relocate":
                            company.try_to_relocate(self._try_to_get_coordinates(action))
                case {"action_type":"drone", "company_id": c_id, "drone_id" : d_id, "action" : a}:
                    drone:Drone = cast(Drone,self._try_to_get_entity(Drone, d_id))
                    if not drone.is_owned_by(company):
                        raise ValueError(
                            f"Drone {d_id} is not owned by company {c_id}."
                        )
                    match a:
                        case "rest":
                            drone.try_to_rest()
                        case "rescue":
                            drone.try_to_start_rescue()
                        case "move":
                            drone.try_to_set_destination(
                                self._try_to_get_coordinates(action)
                            )
                        case "pickup_package" | "drop_package":
                            try:
                                p_id: str = action["package_id"]
                            except KeyError:
                                raise ValueError("Missing package id.")
                            package:Package = cast(Package,self._try_to_get_entity(Package, p_id))
                            if a == "pickup_package": drone.try_to_pickup_package(package)
                            elif a == "drop_package": drone.try_to_drop_off_package(package)
                        case "charge":
                            try:
                                ch_id: str = action["charging_station_id"]
                            except KeyError:
                                raise ValueError("Missing charging station id.")
                            drone.try_to_land_to_charger(cast(ChargingStation,self._try_to_get_entity(ChargingStation, ch_id)))
        except ValueError as e:
            log_outcome(False, e.args[0])
            raise e
        log_outcome(True)
    
    def migrate(self):
        for package in self._entities[Package].values():
            package = cast(Package, package)
            if not hasattr(package, 'contractor'):
                package.contractor = None
        if not hasattr(self, "_min_package_count"):
            self._min_package_count:int = 30
        if not hasattr(self, "_charge_speed_upgrade"):
            self._charge_speed_upgrade = [3]
            for station in self._entities[ChargingStation].values():
                station = cast(ChargingStation, station)
                if station.max_charging_speed_W is not None:
                    station.max_charging_speed_W *= 3
                else:
                    station.max_charging_speed_W = 300
