"""
extension.py
Plots historical data, 2030 exponential forecasts, and 95% bootstrap prediction intervals.
"""

import matplotlib.pyplot as plt
import numpy as np
from src.data_loader import load_all_districts
from src.forecasters import ExponentialForecaster

def bootstrap_prediction_intervals(model, years, values, horizon, n_bootstraps=1000):
    """Generates bootstrap prediction intervals by resampling residuals."""
    # 1. Fit baseline model to get in-sample predictions
    model.fit(years, values)
    slope_or_cagr = model.cagr
    current = values[0]
    fitted = [current]
    for _ in range(1, len(values)):
        current = current * (1 + slope_or_cagr)
        fitted.append(current)
    fitted = np.array(fitted)
    
    # 2. Calculate residuals
    residuals = values - fitted
    
    # 3. Deterministic future prediction
    future_preds = model.predict(horizon)
    
    # 4. Bootstrap simulations (at least 1,000 resamples)
    np.random.seed(42) # For reproducibility
    boot_simulations = np.zeros((n_bootstraps, horizon))
    
    for i in range(n_bootstraps):
        # Sample residuals with replacement
        resample_res = np.random.choice(residuals, size=horizon, replace=True)
        # Add cumulative residual noise to future deterministic projection
        boot_simulations[i, :] = future_preds + np.cumsum(resample_res)
        
    # 5. Calculate 95% confidence bounds (2.5th and 97.5th percentiles)
    lower_bound = np.percentile(boot_simulations, 2.5, axis=0)
    upper_bound = np.percentile(boot_simulations, 97.5, axis=0)
    
    return future_preds, lower_bound, upper_bound

def run_extension():
    districts = load_all_districts()
    model = ExponentialForecaster()
    
    horizon = 6  # 2025 to 2030
    future_years = np.arange(2025, 2030 + 1)
    
    # Create a figure with a 3x2 grid of subplots
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 12))
    axes = axes.flatten()
    
    for i, (name, dist) in enumerate(districts.items()):
        ax = axes[i]
        
        # Get forecasts and bootstrap intervals
        preds, lower, upper = bootstrap_prediction_intervals(model, dist.years, dist.data, horizon)
        
        # Bridge historical endpoint to future arrays for smooth plotting
        forecast_years = np.concatenate([[dist.years[-1]], future_years])
        forecast_values = np.concatenate([[dist.data[-1]], preds])
        lower_band = np.concatenate([[dist.data[-1]], lower])
        upper_band = np.concatenate([[dist.data[-1]], upper])
        
        # Plot historical data
        ax.plot(dist.years, dist.data, marker='o', color='royalblue', linewidth=2, label='Historical (2015-2024)')
        
        # Plot exponential forecast
        ax.plot(forecast_years, forecast_values, marker='s', linestyle='--', color='darkorange', linewidth=2, label='Exponential Forecast')
        
        # Shade 95% prediction interval band
        ax.fill_between(forecast_years, lower_band, upper_band, color='orange', alpha=0.25, label='95% Prediction Interval')
        
        # Styling each subplot
        ax.set_title(f"{name} District Population & 95% Intervals", fontsize=11, fontweight='bold')
        ax.set_xlabel("Year", fontsize=9)
        ax.set_ylabel("Population (Thousands)", fontsize=9)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left', fontsize=8)

    # Hide the 6th unused subplot slot
    if len(districts) < len(axes):
        fig.delaxes(axes[-1])
        
    plt.tight_layout()
    
    output_path = "district_population_forecasts_bootstrap.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Enhanced bootstrap plot successfully saved to '{output_path}'!")
    
    plt.show()

if __name__ == "__main__":
    run_extension()