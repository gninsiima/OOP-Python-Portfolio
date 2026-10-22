# src/fish_model.py
import numpy as np
import matplotlib.pyplot as plt

def generate_fibonacci(n=15):
    """Task 1: Generates n Fibonacci numbers as a baseline stock model."""
    fib = [1, 1]
    for i in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib

class FishStock():
    """Task 2: Discrete logistic growth model with proportional harvesting."""
    def __init__(self, r=0, K=10000.0, N0=4000.0):
        self.r = r  #Intrisic growth rate
        self.K = K  #Carrying capacity (tonnes)
        self.N0 = N0 #Initial stock (tonnes)

    def simulate(self, weeks=52, harvest_rate=0.1):
        """Simulates fish stock and harvests over a given number of weeks."""
        stock = np.zeros(weeks + 1)
        harvests = np.zeros(weeks)
        stock[0] = self.N0
        
        for t in range(weeks):
            # Harvest in tonnes for the current week based on current stock
            h_tonnes = harvest_rate * stock[t]
            harvests[t] = h_tonnes
            
            # Discrete logistic growth equation
            growth = self.r * stock[t] * (1.0 - stock[t] / self.K)
            next_stock = stock[t] + growth - h_tonnes
            
            # Stock cannot drop below zero
            stock[t+1] = max(0.0, next_stock)
            
        return stock, harvests

class PriceModel:
    """Task 3: Seeded random walk price model with bounds."""
    def __init__(self, initial_price=12000.0, min_price=9000.0, max_price=16000.0, seed=42):
        self.initial_price = initial_price
        self.min_price = min_price
        self.max_price = max_price
        self.seed = seed

    def generate_paths(self, weeks=52, num_paths=1000):
        """Generates multiple weekly price paths using a random walk with reflecting bounds."""
        np.random.seed(self.seed)
        prices = np.zeros((weeks, num_paths))
        current_prices = np.full(num_paths, self.initial_price)
        
        for t in range(weeks):
            shocks = np.random.normal(0, 300, num_paths)
            current_prices += shocks
            current_prices = np.clip(current_prices, self.min_price, self.max_price)
            prices[t] = current_prices
            
        return prices

class RiskAssessor:
    """Task 4 & 5: Statistical analysis, variance critique, CV risk classification, and VaR."""
    @staticmethod
    def compute_statistics(annual_revenues):
        mean_rev = np.mean(annual_revenues)
        median_rev = np.median(annual_revenues)
        var_rev = np.var(annual_revenues, ddof=1)
        std_rev = np.std(annual_revenues, ddof=1)
        cv = std_rev / mean_rev if mean_rev != 0 else 0.0
        
        return {
            "mean": mean_rev,
            "median": median_rev,
            "variance": var_rev,
            "std_dev": std_rev,
            "cv": cv
        }

    @staticmethod
    def classify_risk(cv):
        """Classifies risk based on the unitless Coefficient of Variation (CV)."""
        if cv < 0.10:
            return "Low Risk (Stable Revenue)"
        elif cv < 0.25:
            return "Moderate Risk (Manageable Volatility)"
        else:
            return "High Risk (Severe Revenue Instability)"

    @staticmethod
    def calculate_var(annual_revenues, percentile=5):
        """Calculates Value-at-Risk at a given percentile (e.g., 5%)."""
        return np.percentile(annual_revenues, percentile)



if __name__ == "__main__":
    print("--- Task 1: Fibonacci Stock Baseline ---")
    fib_stock = generate_fibonacci(15)
    print(f"Fibonacci Stock (15 weeks): {fib_stock}")
    print("\nBiological Critique:")
    print("Unbounded Fibonacci growth is biologically unrealistic because fish populations")
    print("in Lake Victoria face environmental carrying capacity limits (K), resource")
    print("competition, predation, and density-dependent mortality. Real ecosystems never")
    print("exhibit permanent exponential acceleration without bounds.")
    print("\n--- Task 2: FishStock Simulation (52 Weeks, h=0.1)---")
    model =FishStock(r=0.4, K=10000.0, N0=4000.0)
    stock_traj, harvest_traj = model.simulate(weeks=52, harvest_rate=0.1)
    print(f"Initial Stock: {stock_traj[0]:.2f} tonnes")
    print(f"Week 1 Stock: {stock_traj[1]:.2f} tonnes, Harvest: {harvest_traj[0]:.2f} tonnes")
    print(f"Final Stock (Week 52): {stock_traj[-1]:.2f} tonnes")
    print("\n--- Task 3: PriceModel Simulation ---")
    price_model = PriceModel(seed=42)
    price_paths = price_model.generate_paths(weeks=52, num_paths=1000)
    print(f"Price paths shape (Weeks, Paths): {price_paths.shape}")
    print(f"Initial Price across all paths: {price_paths[0, 0]:,.2f} UGX/kg")
    print(f"Week 1 mean price across paths: {np.mean(price_paths[0]):,.2f} UGX/kg")
    print(f"Week 52 mean price across paths: {np.mean(price_paths[-1]):,.2f} UGX/kg")
    print("\n--- Task 4 & 5: RiskAssessor & Statistics (h=0.1) ---")
    # Weekly revenue = harvest (tonnes) * 1000 (kg/tonne) * price paths (UGX/kg)
    weekly_revenue = (harvest_traj[:, np.newaxis] * 1000.0) * price_paths
    annual_revenue = np.sum(weekly_revenue, axis=0) # 1000 annual totals

    stats = RiskAssessor.compute_statistics(annual_revenue)
    risk_class = RiskAssessor.classify_risk(stats["cv"])
    var_5 = RiskAssessor.calculate_var(annual_revenue, 5)

    print(f"Mean Annual Revenue: {stats['mean']:,.2f} UGX")
    print(f"Median Annual Revenue: {stats['median']:,.2f} UGX")
    print(f"Variance: {stats['variance']:,.2f} UGX^2")
    print(f"Standard Deviation: {stats['std_dev']:,.2f} UGX")
    print(f"Coefficient of Variation (CV): {stats['cv']:.4f}")
    print(f"Risk Classification: {risk_class}")
    print(f"5% Value-at-Risk (VaR): {var_5:,.2f} UGX")

    print("\nVariance Critique:")
    print("A raw variance threshold like 50,000 is meaningless because variance is expressed in squared units (UGX^2).")
    print("With annual revenues in the billions of UGX, squared variance is astronomically large, making any absolute threshold scale-dependent.")
    print("The Coefficient of Variation (CV) is unitless and provides a valid scale-invariant measure of relative risk.")
if __name__ == "__main__":
    print("=" * 60)
    print("MINI-PROJECT 3: LAKE VICTORIA FISH STOCK & EXPORT RISK MODEL")
    print("=" * 60)

    # Task 1: Fibonacci Baseline
    fib_stock = generate_fibonacci(15)
    print(f"\n--- Task 1: Fibonacci Stock Baseline ---")
    print(f"Fib Stock: {fib_stock}")

    # Initialize models
    model = FishStock(r=0.4, K=10000.0, N0=4000.0)
    price_model = PriceModel(seed=42)
    price_paths = price_model.generate_paths(weeks=52, num_paths=1000)

    # Task 6: Scenario Analysis for h = 0.05, 0.10, 0.20, 0.30
    harvest_rates = [0.05, 0.10, 0.20, 0.30]
    scenarios = {}

    print(f"\n--- Task 6: Scenario Analysis (Harvest Rates) ---")
    for h in harvest_rates:
        stock, harvests = model.simulate(weeks=52, harvest_rate=h)
        # Weekly revenue = harvest (tonnes) * 1000 (kg/tonne) * price paths (UGX/kg)
        weekly_revenue = (harvests[:, np.newaxis] * 1000.0) * price_paths
        annual_revenue = np.sum(weekly_revenue, axis=0)
        
        stats = RiskAssessor.compute_statistics(annual_revenue)
        risk_class = RiskAssessor.classify_risk(stats["cv"])
        var_5 = RiskAssessor.calculate_var(annual_revenue, 5)
        
        scenarios[h] = {
            "stock": stock,
            "harvests": harvests,
            "annual_revenue": annual_revenue,
            "stats": stats,
            "risk_class": risk_class,
            "var_5": var_5
        }
        
        print(f"\nHarvest Rate h = {h:.2f}:")
        print(f"  Final Stock (Week 52): {stock[-1]:.2f} tonnes")
        print(f"  Mean Annual Revenue: {stats['mean']:,.2f} UGX")
        print(f"  Revenue CV: {stats['cv']:.4f} -> {risk_class}")
        print(f"  5% VaR: {var_5:,.2f} UGX")

    # MSY Comparison
    msy = (model.r * model.K) / 4.0
    print(f"\nTheoretical Maximum Sustainable Yield (MSY = rK/4): {msy:,.2f} tonnes/year")

    # Task 7: Visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot A: Stock trajectories
    weeks = np.arange(len(scenarios[0.05]["stock"]))
    for h, data in scenarios.items():
        axes[0].plot(weeks, data["stock"], label=f"h = {h:.2f}", linewidth=2)
    axes[0].set_title("Lake Victoria Fish Stock Trajectories (52 Weeks)")
    axes[0].set_xlabel("Weeks")
    axes[0].set_ylabel("Stock (Tonnes)")
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    # Plot B: Histogram of annual revenue for h = 0.10 with VaR
    rev_h10 = scenarios[0.10]["annual_revenue"]
    var_h10 = scenarios[0.10]["var_5"]
    axes[1].hist(rev_h10 / 1e9, bins=30, color="skyblue", edgecolor="black", alpha=0.7)
    axes[1].axvline(var_h10 / 1e9, color="red", linestyle="--", linewidth=2, label=f"5% VaR: {var_h10/1e9:.2f}B UGX")
    axes[1].set_title("Annual Revenue Distribution (h = 0.10)")
    axes[1].set_xlabel("Annual Revenue (Billion UGX)")
    axes[1].set_ylabel("Frequency")
    axes[1].grid(True, linestyle="--", alpha=0.6)
    axes[1].legend()

    plt.tight_layout()
    plt.show()
