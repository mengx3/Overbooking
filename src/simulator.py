from typing import Dict, List, Any
import pandas as pd
from src.scenario_generator import ScenarioGenerator
from src.policies import BumpingPolicy, RandomPolicy, FIFOPolicy
from src.flight import Flight

class OverbookingSimulator:
    """Main simulator for running overbooking scenarios"""   
    def __init__(self, num_scenarios: int, num_flights_per_scenario: int, seed: int = 42):
        self.num_scenarios = num_scenarios
        self.num_flights_per_scenario = num_flights_per_scenario
        self.generator = ScenarioGenerator(seed)
        self.results = []

    def run_scenario(self, scenario_id: int, policy: BumpingPolicy) -> Dict[str, Any]:
        """Run a single scenario with given policy"""
        flights = self.generator.generate_scenario(scenario_id, self.num_flights_per_scenario)
        
        scenario_stats = {
            'scenario_id': scenario_id,
            'policy': policy.__class__.__name__,
            'total_passengers_booked': 0,
            'total_passengers_showed': 0,
            'total_passengers_bumped': 0,
            'total_cost': 0,
            'flights_with_bumping': 0,
            'flight_details': []
        }
        
        for flight in flights:
            flight.simulate_show_ups()

            num_to_bump = flight.get_overbooked_count()
            
            if num_to_bump > 0:
                bumped = policy.select_passengers_to_bump(
                    flight.showed_up_passengers, 
                    num_to_bump
                )
                flight.bumped_passengers = bumped
                for passenger in bumped:
                    passenger.was_bumped = True
                scenario_stats['flights_with_bumping'] += 1
            
            scenario_stats['total_passengers_booked'] += len(flight.passengers)
            scenario_stats['total_passengers_showed'] += len(flight.showed_up_passengers)
            scenario_stats['total_passengers_bumped'] += len(flight.bumped_passengers)
            scenario_stats['total_cost'] += flight.calculate_total_cost()

            scenario_stats['flight_details'].append({
                'flight_id': flight.flight_id,
                'capacity': flight.capacity,
                'booked': len(flight.passengers),
                'showed_up': len(flight.showed_up_passengers),
                'bumped': len(flight.bumped_passengers),
                'cost': flight.calculate_total_cost()
            })
        
        return scenario_stats
    
