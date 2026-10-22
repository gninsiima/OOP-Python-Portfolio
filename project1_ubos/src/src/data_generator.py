import numpy as np
import pandas as pd
import os

def generate_30_day_demand_csv(filename="data/microgrid_demand_30days.csv"):
    """
    Generates 30 days of simulated energy demand (D1 and D2) with a weekly pattern
    and random noise, using a seeded random generator for reproducibility.
    """
    np.random.seed(42) # Seeded for reproducibility
    
    days = np.arange(1, 31)
    
    # Base daily loads with a 7-day weekly cycle (e.g., lower demand on weekends)
    # D1: Daytime load, D2: Critical equipment load
    weekly_pattern_d1 = 120 + 20 * np.sin(2 * np.pi * days / 7)
    weekly_pattern_d2 = 90 + 10 * np.cos(2 * np.pi * days / 7)
    
    # Add Gaussian noise
    noise_d1 = np.random.normal(0, 8, size=30)
    noise_d2 = np.random.normal(0, 5, size=30)
    
    d1_loads = np.maximum(50, weekly_pattern_d1 + noise_d1) # Ensure positive values
    d2_loads = np.maximum(40, weekly_pattern_d2 + noise_d2)
    
    df = pd.DataFrame({
        "Day": days,
        "D1_Daytime_Load_kWh": d1_loads,
        "D2_Critical_Load_kWh": d2_loads
    })
    
    # Ensure data folder exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"Successfully generated 30-day demand dataset at: {filename}")
    return df

if __name__ == "__main__":
    generate_30_day_demand_csv()