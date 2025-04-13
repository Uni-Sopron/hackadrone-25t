from datetime import datetime, timedelta
import os
import pickle

from .company import Company
from .drone import Drone
from .package import Package
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

    def status(self, company_name: str, entities: set[type]) -> dict[str, list[dict]]:
        self._apply_time_delay()
        return {
            entity.__name__: [
                item.get_status(company_id=company_name)
                for item in self._entities[entity].values()
            ]
            for entity in entities
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
            raise ValueError(f"Charging station with name {name} does not exist.")
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
        log(f" WORLD | DELAY | {time_delay.total_seconds()} s")
        if time_delay.total_seconds() > 0:
            self._last_event += time_delay
            for drone in self._entities[Drone].values():
                drone.apply_time_pass(int(time_delay.total_seconds()))
            for id in list(self._entities[Package]):
                package: Package = self._entities[Package][id]
                if (
                    package.status in {Package.Status.FAILED, Package.Status.DELIVERED}
                    or package.status == Package.Status.AVAILABLE
                    and package.latest_delivery_datetime < World.now()
                ):
                    del self._entities[Package][id]
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
            company: Company = self._try_to_get_entity(Company, action["company_id"])
            match action:
                case {"action_type": "company", "company_id": c_id, "action": a}:
                    match a:
                        case "new_drone":
                            company.try_to_pay_for_new_drone()
                            new_drone: Drone = Drone(company)
                            self._entities[Drone][new_drone.id()] = new_drone
                        case "relocate":
                            company.try_to_relocate(
                                self._try_to_get_coordinates(action)
                            )
                case {
                    "action_type": "drone",
                    "company_id": c_id,
                    "drone_id": d_id,
                    "action": a,
                }:
                    drone: Drone = self._try_to_get_entity(Drone, d_id)
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
                            package: Package = self._try_to_get_entity(Package, p_id)
                            if a == "pickup_package":
                                drone.try_to_pickup_package(package)
                            elif a == "drop_package":
                                drone.try_to_drop_off_package(package)
                        case "charge":
                            try:
                                ch_id: str = action["charging_station_id"]
                            except KeyError:
                                raise ValueError("Missing charging station id.")
                            drone.try_to_land_to_charger(
                                self._try_to_get_entity(ChargingStation, ch_id)
                            )
        except ValueError as e:
            log_outcome(False, e.args[0])
            raise e
        log_outcome(True)
