import argparse
from src.simulator import OverbookingSimulator
from src.visualizer import Visualizer
from src.policies import RandomPolicy, FIFOPolicy
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description='Airline Overbooking Scenario Simulator')
    parser.add_argument('--num-scenarios', type=int, default=50, 
                       help='Number of scenarios to simulate')
    parser.add_argument('--num-flights', type=int, default=20, 
                       help='Number of flights per scenario')
    parser.add_argument('--policy', choices=['random', 'fifo', 'both'], 
                       default='both', help='Bumping policy to use')
    parser.add_argument('--seed', type=int, default=42, 
                       help='Random seed for reproducibility')
    parser.add_argument('--output-dir', type=str, default='output', 
                       help='Directory for output files')
    
    args = parser.parse_args()

    print("=" * 50)
    print("AIRLINE OVERBOOKING SCENARIO SIMULATOR")
    print("=" * 50)
    print("Scenarios: {}".format(args.num_scenarios))
    print("Flights per scenario: {}".format(args.num_flights))
    print("Policy: {}".format(args.policy))
    print("Random seed: {}".format(args.seed))
    print("=" * 50)
    
    # Initialize simulator
    simulator = OverbookingSimulator(
        num_scenarios=args.num_scenarios,
        num_flights_per_scenario=args.num_flights,
        seed=args.seed
    )
    
    # Run simulations
    print("\nRunning simulations...")
    
    try:
        # Compare both policies
        results = simulator.compare_policies()
        
        print("✓ Completed {} scenarios".format(args.num_scenarios))
        print("✓ Simulated {} total flights".format(args.num_scenarios * args.num_flights))
        
        # Generate outputs
        visualizer = Visualizer(output_dir=args.output_dir)
        visualizer.generate_all_outputs(results)
        
        # Print summary statistics
        print("\n" + "=" * 50)
        print("SIMULATION RESULTS SUMMARY")
        print("=" * 50)
        
        summary = results['summary']

        for policy in ['RandomPolicy', 'FIFOPolicy']:
            policy_data = summary[summary['policy'] == policy]
            print("\n{}:".format(policy))
            print("  Average passengers bumped: {:.2f}".format(policy_data['total_bumped'].mean()))
            print("  Average total cost: ${:.2f}".format(policy_data['total_cost'].mean()))
            print("  Average bumping rate: {:.3%}".format(policy_data['bumping_rate'].mean()))
        
        print("\n" + "=" * 50)
        print("OUTPUT FILES GENERATED:")
        print("=" * 50)
        print("CSV files: {}/csv/".format(args.output_dir))
        print("Plots: {}/plots/".format(args.output_dir))
        print("HTML Dashboard: {}/html/dashboard.html".format(args.output_dir))
        print("\nOpen the HTML dashboard in your browser to view interactive results!")
        
    except Exception as e:
        print("\n Error during simulation: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
