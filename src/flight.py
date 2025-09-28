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
        
    def generate_passengers(self):
        """Generate random passengers for this flight"""
        fare_classes = ['economy', 'business', 'first']
        fare_weights = [0.7, 0.2, 0.1]
        
        for i in range(self.total_bookings):
            passenger = Passenger(
                passenger_id=f"{self.flight_id}_P{i:03d}",
                fare_class=random.choices(fare_classes, fare_weights)[0],
                booking_time=datetime.now(),
                checkin_time=None,
                show_up_probability=random.uniform(0.85, 0.95)
            )
            self.passengers.append(passenger)
    
    
    def simulate_show_ups(self):
        """Simulate which passengers show up"""
        self.showed_up_passengers = []
        for passenger in self.passengers:
            if passenger.simulate_show_up():
                self.showed_up_passengers.append(passenger)
    
    def get_overbooked_count(self) -> int:
        """Calculate how many passengers need to be bumped"""
        return max(0, len(self.showed_up_passengers) - self.capacity)
    
    def calculate_total_cost(self) -> float:
        """Calculate total compensation cost for bumped passengers"""
        return sum(p.get_compensation_cost() for p in self.bumped_passengers)
