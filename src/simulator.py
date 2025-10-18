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
