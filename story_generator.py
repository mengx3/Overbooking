import json
import random
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import argparse
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.simulator import OverbookingSimulator
from src.passenger import Passenger
from src.flight import Flight
from src.policies import RandomPolicy, FIFOPolicy
from src.visualizer import Visualizer

app = Flask(__name__)
CORS(app)

@dataclass
class ScenarioConfig:
    """Configuration for AI-enhanced scenario generation"""
    num_scenarios: int
    num_flights: int
    complexity: str
    aircraft_types: List[str]
    route_type: str
    season: str
    overbook_min: float
    overbook_max: float
    risk_tolerance: str
    compensation_strategy: str
    showup_profile: str
    fare_classes: List[str]
    ai_mode: str
    custom_rules: str
    seed: int

class AIScenarioGenerator:
    
    def __init__(self, config: ScenarioConfig):
        self.config = config
        if config.seed:
            random.seed(config.seed)
            np.random.seed(config.seed)
        self.aircraft_capacities = {
            'narrow': (100, 200),
            'wide': (200, 400),
            'regional': (50, 100)
        }
        
        self.showup_profiles = {
            'normal': (0.85, 0.95),
            'high': (0.90, 0.98),
            'variable': (0.75, 0.95),
            'business': (0.92, 0.99),
            'leisure': (0.80, 0.90)
        }
