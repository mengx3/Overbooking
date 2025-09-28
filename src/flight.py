"""Flight class with booking management"""
from typing import List, Dict
from datetime import datetime
import random
from src.passenger import Passenger

class Flight:
    """Represents a single flight with overbooking"""
    
    def __init__(self, flight_id: str, capacity: int, overbook_rate: float):
        self.flight_id = flight_id
        self.capacity = capacity
        self.overbook_rate = overbook_rate
        self.total_bookings = int(capacity * overbook_rate)
        self.passengers: List[Passenger] = []
        self.showed_up_passengers: List[Passenger] = []
        self.bumped_passengers: List[Passenger] = []
