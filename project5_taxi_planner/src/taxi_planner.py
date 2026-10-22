import numpy as np
import scipy.linalg
import statistics
import matplotlib.pyplot as plt

# ==========================================
# DATA SETUP
# ==========================================
ROUTES_DATA = {
    "Ntinda": {"passengers": np.array([35, 40, 42, 50, 55, 60, 48, 52, 47, 45]), "fare": 2000},
    "Entebbe": {"passengers": np.array([60, 58, 65, 70, 72, 80, 75, 68, 66, 64]), "fare": 5000},
    "Mukono": {"passengers": np.array([45, 47, 50, 49, 55, 62, 58, 53, 51, 50]), "fare": 3000},
}

# ==========================================
# TASK 1: Route Class
# ==========================================
class Route:
    def __init__(self, name, passengers, fare):
        self.name = name
        self.passengers = np.array(passengers, dtype=float)
        self.fare = float(fare)

    def daily_revenue(self):
        """Returns daily revenue array (passengers * fare)."""
        return self.passengers * self.fare

    def total_revenue(self):
        """Returns total revenue over the recorded period."""
        return np.sum(self.daily_revenue())

    def descriptive_stats(self):
        """Computes mean, variance, and standard deviation using statistics module and numpy."""
        pass_list = self.passengers.tolist()
        return {
            "mean": statistics.mean(pass_list),
            "variance": statistics.variance(pass_list),
            "stdev": statistics.stdev(pass_list),
            "np_mean": np.mean(self.passengers),
            "np_std": np.std(self.passengers, ddof=1)
        }

# ==========================================
# TASK 2: Supply-Demand Equilibrium (Ntinda)
# ==========================================
def solve_equilibrium():
    # Qd = 120 - 0.02P  =>  0.02P + Qd = 120
    # Qs = 10 + 0.03P   => -0.03P + Qs = 10
    # Matrix form AX = B where X = [P, Q]^T
    # [ 0.02  1 ] [ P ] = [ 120 ]
    # [-0.03  1 ] [ Q ] = [  10 ]
    
    A = np.array([[0.02, 1.0], 
                  [-0.03, 1.0]])
    B = np.array([120.0, 10.0])
    
    P_eq, Q_eq = scipy.linalg.solve(A, B)
    current_fare = 2000
    
    print("--- Task 2: Supply-Demand Equilibrium (Ntinda) ---")
    print(f"Equilibrium Price (P*): UGX {P_eq:.2f}")
    print(f"Equilibrium Quantity (Q*): {Q_eq:.2f} passengers/trip-hour")
    print(f"Current Fare: UGX {current_fare}")
    
    if current_fare < P_eq:
        print("Interpretation: The current UGX 2,000 fare is BELOW equilibrium.")
        print("Result: Excess demand (passenger queues/shortage of seats), creating upward pressure on fares.\n")
    else:
        print("Interpretation: The current fare is ABOVE or AT equilibrium.\n")

# ==========================================
# TASK 3: Forecaster Base Class & Subclasses
# ==========================================
class Forecaster:
    def forecast(self, history):
        raise NotImplementedError("Subclasses must implement forecast method.")

class MovingAverageForecaster(Forecaster):
    def __init__(self, window=3):
        self.window = window

    def forecast(self, history):
        if len(history) < self.window:
            return np.mean(history)
        return np.mean(history[-self.window:])

class SimpleExponentialSmoothing(Forecaster):
    def __init__(self, alpha=0.5):
        self.alpha = alpha

    def forecast(self, history):
        s = history[0]
        for t in range(1, len(history)):
            s = self.alpha * history[t] + (1 - self.alpha) * s
        return s

class LinearTrendForecaster(Forecaster):
    def forecast(self, history):
        n = len(history)
        if n < 2:
            return history[-1]
        x = np.arange(n)
        slope, intercept = np.polyfit(x, history, 1)
        return slope * n + intercept

# ==========================================
# TASK 4: Walk-Forward Backtesting & Tuning
# ==========================================
def backtest_and_tune():
    print("--- Task 4: Backtesting (Days 4-10) & Alpha Tuning ---")
    alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for route_name, data in ROUTES_DATA.items():
        passengers = data["passengers"]
        
        # Grid search for best alpha on SES
        best_alpha = alphas[0]
        best_ses_mae = float('inf')
        
        for alpha in alphas:
            ses = SimpleExponentialSmoothing(alpha)
            errors = []
            for t in range(3, len(passengers)):
                train = passengers[:t]
                actual = passengers[t]
                pred = ses.forecast(train)
                errors.append(abs(actual - pred))
            mean_ae = np.mean(errors)
            if mean_ae < best_ses_mae:
                best_ses_mae = mean_ae
                best_alpha = alpha
        
        # Evaluate all models with walk-forward (days 4 to 10 correspond to indices 3 to 9)
        models = {
            "MA (w=3)": MovingAverageForecaster(3),
            f"SES (alpha={best_alpha})": SimpleExponentialSmoothing(best_alpha),
            "Linear Trend": LinearTrendForecaster()
        }
        
        print(f"\nRoute: {route_name} (Best SES Alpha: {best_alpha})")
        for m_name, model in models.items():
            errors = []
            for t in range(3, len(passengers)):
                train = passengers[:t]
                actual = passengers[t]
                pred = model.forecast(train)
                errors.append(abs(actual - pred))
            mae = np.mean(errors)
            print(f"  {m_name:<20} | MAE: {mae:.2f}")

# ==========================================
# TASK 5 & 6: Day 11 Forecasting & Fleet Planning
# ==========================================
def run_day11_forecast_and_fleet():
    print("\n--- Tasks 5 & 6: Day 11 Forecast & Fleet Planning ---")
    
    day11_results = {}
    
    for route_name, data in ROUTES_DATA.items():
        passengers = data["passengers"]
        fare = data["fare"]
        
        # Using Linear Trend or optimized SES as best model
        model = LinearTrendForecaster()
        forecast_passengers = model.forecast(passengers)
        forecast_revenue = forecast_passengers * fare
        
        # Fleet Planning: 8 trips/day, 14 passengers/vehicle, 15% buffer
        capacity_per_vehicle = 8 * 14
        raw_vehicles = forecast_passengers / capacity_per_vehicle
        buffered_vehicles = raw_vehicles * 1.15
        recommended_vehicles = int(np.ceil(buffered_vehicles))
        
        day11_results[route_name] = {
            "passengers": forecast_passengers,
            "revenue": forecast_revenue,
            "vehicles": recommended_vehicles
        }
        
        print(f"Route: {route_name}")
        print(f"  Forecast Passengers (Day 11): {forecast_passengers:.1f}")
        print(f"  Forecast Revenue (UGX):       {forecast_revenue:,.2f}")
        print(f"  Recommended Fleet Size:       {recommended_vehicles} vehicles (incl. 15% buffer)\n")

    return day11_results

# ==========================================
# EXTENSION: 60-Day Seasonal Simulation
# ==========================================
def run_extension():
    print("--- Extension: 60-Day Seasonal Simulation ---")
    np.random.seed(42)
    days = 60
    base_demand = 50
    
    # Generate weekly pattern: Fridays (day index % 7 == 4) are busier, Sundays (day index % 7 == 6) quieter
    demand = []
    for d in range(days):
        day_of_week = d % 7
        if day_of_week == 4: # Friday
            seasonal_bump = 15
        elif day_of_week == 6: # Sunday
            seasonal_bump = -15
        else:
            seasonal_bump = 0
        noise = np.random.normal(0, 3)
        demand.append(max(20, base_demand + seasonal_bump + noise))
    
    demand = np.array(demand)
    
    # Backtest Seasonal-Naïve (lag=7) vs Moving Average (w=3) from day 7 onwards
    ma_errors = []
    sn_errors = []
    
    for t in range(7, days):
        # Moving Average
        ma_pred = np.mean(demand[t-3:t])
        ma_errors.append(abs(demand[t] - ma_pred))
        
        # Seasonal Naïve (value from exactly 7 days ago)
        sn_pred = demand[t-7]
        sn_errors.append(abs(demand[t] - sn_pred))
        
    print(f"60-Day Simulation MAE - Moving Average (w=3): {np.mean(ma_errors):.2f}")
    print(f"60-Day Simulation MAE - Seasonal-Naïve (lag=7): {np.mean(sn_errors):.2f}")
    if np.mean(sn_errors) < np.mean(ma_errors):
        print("Conclusion: Seasonal-Naïve forecaster successfully beats the moving average under weekly seasonality!\n")

if __name__ == "__main__":
    solve_equilibrium()
    backtest_and_tune()
    run_day11_forecast_and_fleet()
    run_extension()