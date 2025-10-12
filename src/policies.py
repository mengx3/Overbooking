from typing import List
from abc import ABC, abstractmethod
import random
from src.passenger import Passenger

class BumpingPolicy(ABC):
    
    @abstractmethod
    def select_passengers_to_bump(self, passengers: List[Passenger], num_to_bump: int) -> List[Passenger]:
        pass

class RandomPolicy(BumpingPolicy):

    def select_passengers_to_bump(self, passengers: List[Passenger], num_to_bump: int) -> List[Passenger]:
        if num_to_bump <= 0:
            return []
        return random.sample(passengers, min(num_to_bump, len(passengers)))

class FIFOPolicy(BumpingPolicy):
    
    def select_passengers_to_bump(self, passengers: List[Passenger], num_to_bump: int) -> List[Passenger]:
        if num_to_bump <= 0:
            return []
        sorted_passengers = sorted(
            passengers, 
            key=lambda p: p.checkin_time if p.checkin_time else datetime.now(),
            reverse=True
        )
        return sorted_passengers[:min(num_to_bump, len(passengers))]
