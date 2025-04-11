from utils import *
from dataclasses import dataclass




@dataclass
class ChargingStation:
    location: Coordinate
    # TODO maybe later max charging speed / capacity   
    # TODO maybe later open hours logic