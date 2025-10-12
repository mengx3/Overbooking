import random
from typing import List, Tuple
from src.flight import Flight

class ScenarioGenerator:
    
    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)

    def generate_scenario(self, scenario_id: int, num_flights: int) -> List[Flight]:
        """Generate a single scenario with multiple flights"""
        flights = []
        
        for i in range(num_flights):
            capacity = random.randint(100, 300)
            
            overbook_rate = random.uniform(1.0, 1.15)
            
            flight = Flight(
                flight_id=f"S{scenario_id:03d}_F{i:03d}",
                capacity=capacity,
                overbook_rate=overbook_rate
            )
            
            flight.generate_passengers()
            flights.append(flight)
        
        return flights
