import timeit
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from microgrid import MicroGrid

class MicroGridDispatch(MicroGrid):
    """
    Extends MicroGrid to handle 30-day batch solving, vectorisation, 
    timing, feasibility checks, statistics, cost analysis, and plotting.
    """
    def __init__(self, csv_path="data/microgrid_demand_30days.csv"):
        super().__init__()
        self.df = pd.read_csv(csv_path)

    def solve_vectorized(self):
        """Solves all 30 days in a single vectorized call."""
        B = np.vstack([
            self.df['D1_Daytime_Load_kWh'].values,
            self.df['D2_Critical_Load_kWh'].values
        ])
        X = np.linalg.solve(self.A, B)
        return X.T  # Shape: (30, 2) -> Column 0: Solar (x), Column 1: Battery (y)

    def analyze_usage_and_costs(self, solutions):
        """Calculates usage statistics and daily/monthly costs (Tasks 5 & 6)."""
        solar = solutions[:, 0]
        battery = solutions[:, 1]

        # Task 5: Statistics & Volatility
        stats = {
            "Solar Mean": np.mean(solar),
            "Solar Var": np.var(solar),
            "Solar Std": np.std(solar),
            "Battery Mean": np.mean(battery),
            "Battery Var": np.var(battery),
            "Battery Std": np.std(battery),
        }
        
        # Coefficient of variation (Std / Mean) to compare relative volatility
        solar_cv = stats["Solar Std"] / stats["Solar Mean"]
        battery_cv = stats["Battery Std"] / stats["Battery Mean"]

        print("\n--- Task 5: Usage Statistics & Volatility ---")
        print(f"Solar (x)   -> Mean: {stats['Solar Mean']:.2f} kWh | Std: {stats['Solar Std']:.2f} kWh | CV: {solar_cv:.4f}")
        print(f"Battery (y) -> Mean: {stats['Battery Mean']:.2f} kWh | Std: {stats['Battery Std']:.2f} kWh | CV: {battery_cv:.4f}")
        
        more_volatile = "Solar" if solar_cv > battery_cv else "Battery"
        print(f"Conclusion: {more_volatile} usage is more volatile relative to its mean.")

        # Task 6: Cost Model (Solar: UGX 150/kWh, Battery: UGX 450/kWh)
        solar_cost_per_kwh = 150
        battery_cost_per_kwh = 450

        daily_costs = (solar * solar_cost_per_kwh) + (battery * battery_cost_per_kwh)
        total_monthly_cost = np.sum(daily_costs)

        print("\n--- Task 6: Energy Cost Analysis (UGX) ---")
        print(f"Average Daily Cost:   UGX {np.mean(daily_costs):,.2f}")
        print(f"Total 30-Day Cost:    UGX {total_monthly_cost:,.2f}")

        return daily_costs

    def plot_dispatch_and_costs(self, solutions, daily_costs):
        """Task 7: Stacked bar chart of solar vs battery with secondary cost axis."""
        days = self.df['Day']
        solar = solutions[:, 0]
        battery = solutions[:, 1]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Primary Axis: Stacked bar chart for energy sources
        ax1.bar(days, solar, label='Solar (x)', color='#f39c12', alpha=0.85)
        ax1.bar(days, battery, bottom=solar, label='Battery (y)', color='#3498db', alpha=0.85)
        
        ax1.set_xlabel('Day of Month', fontsize=12)
        ax1.set_ylabel('Energy Usage (kWh)', fontsize=12)
        ax1.set_title('30-Day Micro-Grid Dispatch Plan & Daily Costs (Kasese, Uganda)', fontsize=14, fontweight='bold')
        ax1.legend(loc='upper left')
        ax1.grid(axis='y', linestyle='--', alpha=0.5)

        # Secondary Axis: Line plot for daily energy cost
        ax2 = ax1.twinx()
        ax2.plot(days, daily_costs, color='#e74c3c', marker='o', linewidth=2, label='Daily Cost (UGX)')
        ax2.set_ylabel('Daily Cost (UGX)', fontsize=12, color='#e74c3c')
        ax2.tick_params(axis='y', labelcolor='#e74c3c')
        ax2.legend(loc='upper right')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    planner = MicroGridDispatch()
    
    # Solve 30 days
    solutions = planner.solve_vectorized()
    
    # Run statistics and cost analysis
    daily_costs = planner.analyze_usage_and_costs(solutions)
    
    # Generate visualization
    planner.plot_dispatch_and_costs(solutions, daily_costs)