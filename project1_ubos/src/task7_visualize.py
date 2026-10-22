"""
task7_visualize.py
Plots historical population data and 2030 exponential projections for all 5 UBOS districts using Matplotlib.
"""

import matplotlib.pyplot as plt
import numpy as np
from src.data_loader import load_all_districts
from src.forecasters import ExponentialForecaster

def run_task7():
    districts = load_all_districts()
    model = ExponentialForecaster()
    
    horizon = 6  # 2025 to 2030
    future_years = np.arange(2025, 2030 + 1)
    
    # Create a figure with a 3x2 grid of subplots (we will use 5 of them)
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(14, 12))
    axes = axes.flatten()  # Flatten to easily loop over them
    
    for i, (name, dist) in enumerate(districts.items()):
        ax = axes[i]
        
        # Fit model on historical data
        model.fit(dist.years, dist.data)
        preds = model.predict(horizon)
        
        # Combine historical and future years/values for continuous plotting
        full_years = np.concatenate([dist.years, future_years])
        full_preds = np.concatenate([[dist.data[-1]], preds])  # bridge the gap from last historical point
        
        # Plot historical data
        ax.plot(dist.years, dist.data, marker='o', color='royalblue', linewidth=2, label='Historical (2015-2024)')
        
        # Plot forecast data (starting from last historical point)
        forecast_years = np.concatenate([[dist.years[-1]], future_years])
        forecast_values = np.concatenate([[dist.data[-1]], preds])
        ax.plot(forecast_years, forecast_values, marker='s', linestyle='--', color='darkorange', linewidth=2, label='Exponential Forecast (2025-2030)')
        
        # Styling each subplot
        ax.set_title(f"{name} District Population Forecast", fontsize=12, fontweight='bold')
        ax.set_xlabel("Year", fontsize=10)
        ax.set_ylabel("Population (Thousands)", fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left', fontsize=9)

    # Hide the 6th unused subplot slot if it exists
    if len(districts) < len(axes):
        fig.delaxes(axes[-1])
        
    plt.tight_layout()
    
    # Save figure to file and show
    output_path = "district_population_forecasts.png"
    plt.savefig(output_path, dpi=300)
    print(f"✅ Plot successfully generated and saved to '{output_path}'!")
    
    plt.show()

if __name__ == "__main__":
    run_task7()