import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict
import os

class Visualizer:
    
    def __init__(self, output_dir: str = 'output'):
        self.output_dir = output_dir
        self.plots_dir = os.path.join(output_dir, 'plots')
        self.csv_dir = os.path.join(output_dir, 'csv')
        
        for dir_path in [self.plots_dir, self.csv_dir]:
            os.makedirs(dir_path, exist_ok=True)
