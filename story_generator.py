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
