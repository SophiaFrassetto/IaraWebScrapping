# build-in imports
from dataclasses import dataclass


@dataclass
class Country:
    name: str
    capital: str
    population: int
    area: float
