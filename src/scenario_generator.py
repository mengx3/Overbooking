import random
from typing import List, Tuple
from src.flight import Flight

class ScenarioGenerator:
    
    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)
