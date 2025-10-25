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

    def save_csv_files(self, data: Dict[str, pd.DataFrame]):
        data['summary'].to_csv(os.path.join(self.csv_dir, 'scenario_summary.csv'), index=False)
        data['flights'].to_csv(os.path.join(self.csv_dir, 'flight_details.csv'), index=False)
        
        comparison = data['summary'].groupby('policy').agg({
            'total_bumped': ['mean', 'std'],
            'total_cost': ['mean', 'std'],
            'bumping_rate': ['mean', 'std']
        }).round(2)
        comparison.to_csv(os.path.join(self.csv_dir, 'comparison_results.csv'))
        
        print(f"  ✓ CSV files saved to {self.csv_dir}")
    
    def create_bumping_comparison_plot(self, data: pd.DataFrame):
        plt.figure(figsize=(10, 6))
        
        avg_bumping = data.groupby('policy')['total_bumped'].mean()
        std_bumping = data.groupby('policy')['total_bumped'].std()
        
        ax = avg_bumping.plot(kind='bar', yerr=std_bumping, capsize=5, 
                              color=['#2E86AB', '#A23B72'])
        ax.set_xlabel('Bumping Policy', fontsize=12)
        ax.set_ylabel('Average Passengers Bumped', fontsize=12)
        ax.set_title('Comparison of Bumping Policies', fontsize=14, fontweight='bold')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'bumping_comparison.png'), dpi=100)
        plt.close()
