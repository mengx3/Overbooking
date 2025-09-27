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
