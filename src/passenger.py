"""Passenger class and show-up simulation"""
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Passenger:
    """Represents a passenger with booking information"""
    passenger_id: str
    fare_class: str  # 'economy', 'business', 'first'
    booking_time: datetime
    checkin_time: Optional[datetime]
    show_up_probability: float
    did_show_up: bool = False
    was_bumped: bool = False

    def simulate_show_up(self) -> bool:
        """Simulate whether passenger shows up for flight"""
        self.did_show_up = random.random() < self.show_up_probability
        if self.did_show_up:
            # Assign check-in time (random time before departure)
            base_time = datetime.now()
            self.checkin_time = base_time - timedelta(hours=random.uniform(0.5, 24))
        return self.did_show_up
    
    def get_compensation_cost(self) -> float:
        """Calculate compensation cost if bumped"""
        base_costs = {
            'economy': 200,
            'business': 500,
            'first': 1000
        }
        return base_costs.get(self.fare_class, 200)
