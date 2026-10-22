# src/fish_extension.py
import numpy as np
import matplotlib.pyplot as plt
from fish_model import FishStock, PriceModel

class ClosedSeasonStock(FishStock):
    """Extension: Extends FishStock to support multi-year simulations with closed seasons."""
    def simulate_multiyear(self, years=5, harvest_rate=0.2, closed_season_duration=8):
        """Simulates stock over multiple years with an annual closed season."""
        weeks_total = years * 52
        stock = np.zeros(weeks_total + 1)
        harvests = np.zeros(weeks_total)
        stock[0] = self.N0
        
        # Define closed weeks: the last N weeks of every 52-week year
        closed_weeks = set()
        for y in range(years):
            year_start = y * 52
            for w in range(52 - closed_season_duration, 52):
                closed_weeks.add(year_start + w)
                
        for t in range(weeks_total):
            h = 0.0 if t in closed_weeks else harvest_rate
            h_tonnes = h * stock[t]
            harvests[t] = h_tonnes
            
            growth = self.r * stock[t] * (1.0 - stock[t] / self.K)
            next_stock = stock[t] + growth - h_tonnes
            stock[t+1] = max(0.0, next_stock)
            
        return stock, harvests


if __name__ == "__main__":
    print("=" * 60)
    print("EXTENSION: CLOSED SEASON ANALYSIS (5 YEARS / 260 WEEKS)")
    print("=" * 60)

    model = ClosedSeasonStock(r=0.4, K=10000.0, N0=4000.0)
    price_model = PriceModel(seed=42)
    
    test_h = 0.20
    weeks_260 = 260
    
    # Generate multi-year price paths (260 weeks)
    price_paths_260 = price_model.generate_paths(weeks=weeks_260, num_paths=1000)
    
    # 1. Standard continuous harvesting (h = 0.20 for 260 weeks)
    stock_normal, harvest_normal = model.simulate(weeks=weeks_260, harvest_rate=test_h)
    rev_normal = np.sum((harvest_normal[:, np.newaxis] * 1000.0) * price_paths_260, axis=0)
    
    # 2. Closed season harvesting (8 weeks off per year for 5 years)
    stock_closed, harvest_closed = model.simulate_multiyear(years=5, harvest_rate=test_h, closed_season_duration=8)
    rev_closed = np.sum((harvest_closed[:, np.newaxis] * 1000.0) * price_paths_260, axis=0)
    
    print(f"\nHarvest Rate: {test_h:.2f} over 5 Years (260 Weeks)")
    print(f"  [Standard] Final Stock: {stock_normal[-1]:.2f} tonnes | Mean Revenue: {np.mean(rev_normal):,.2f} UGX")
    print(f"  [Closed]   Final Stock: {stock_closed[-1]:.2f} tonnes | Mean Revenue: {np.mean(rev_closed):,.2f} UGX")

    # Plot 5-year stock trajectory comparison
    plt.figure(figsize=(10, 5))
    time_axis = np.arange(weeks_260 + 1)
    plt.plot(time_axis, stock_normal, label="Continuous Harvesting (h=0.20)", color="red", linewidth=2)
    plt.plot(time_axis, stock_closed, label="Closed Season (8 wks/yr off)", color="green", linewidth=2)
    plt.title("5-Year Lake Victoria Stock Comparison: Continuous vs. Closed Season")
    plt.xlabel("Weeks")
    plt.ylabel("Stock (Tonnes)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()