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

    def create_cost_distribution_plot(self, data: pd.DataFrame):
        plt.figure(figsize=(10, 6))
        
        for policy in data['policy'].unique():
            policy_data = data[data['policy'] == policy]['total_cost']
            plt.hist(policy_data, alpha=0.6, label=policy, bins=20)
        
        plt.xlabel('Total Cost ($)', fontsize=12)
        plt.ylabel('Frequency', fontsize=12)
        plt.title('Distribution of Compensation Costs', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'cost_distribution.png'), dpi=100)
        plt.close()

    def create_scenario_trends_plot(self, data: pd.DataFrame):
        plt.figure(figsize=(12, 6))
        
        for policy in data['policy'].unique():
            policy_data = data[data['policy'] == policy].sort_values('scenario_id')
            plt.plot(policy_data['scenario_id'], policy_data['total_cost'], 
                    label=policy, alpha=0.7, linewidth=1.5)
        
        plt.xlabel('Scenario ID', fontsize=12)
        plt.ylabel('Total Cost ($)', fontsize=12)
        plt.title('Cost Trends Across Scenarios', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(self.plots_dir, 'scenario_trends.png'), dpi=100)
        plt.close()
        
        print(f"  ✓ Plots saved to {self.plots_dir}")
    
    def generate_all_outputs(self, data: Dict[str, pd.DataFrame]):
        print("\nGenerating outputs...")
        
        self.save_csv_files(data)
        
        self.create_bumping_comparison_plot(data['summary'])
        self.create_cost_distribution_plot(data['summary'])
        self.create_scenario_trends_plot(data['summary'])
        
        print(f"\n All outputs saved to {self.output_dir}/")
        print("\n To view interactive dashboard:")
        print("  1. Open dashboard.html in your browser")
        print("  2. Load the CSV files from output/csv/")
        print("     - scenario_summary.csv")
        print("     - flight_details.csv")
