"""
task6_project.py
Generates long-term population projections to 2030 for UBOS districts.
"""

import pandas as pd
import numpy as np
from src.data_loader import load_all_districts
from src.forecasters import ExponentialForecaster

def run_task6():
    districts = load_all_districts()
    
    # Use ExponentialForecaster (CAGR) as our robust long-term model
    model = ExponentialForecaster()
    
    horizon = 6  # 2025 to 2030
    future_years = np.arange(2025, 2030 + 1)
    
    projections = []
    
    for name, dist in districts.items():
        # Fit on full historical data (2015-2024)
        model.fit(dist.years, dist.data)
        preds = model.predict(horizon)
        
        for yr, pop in zip(future_years, preds):
            projections.append({
                "District": name,
                "Year": yr,
                "Projected Pop (Thousands)": pop
            })
            
        # Also include the final historical year (2024) for reference
        projections.append({
            "District": name,
            "Year": 2024,
            "Projected Pop (Thousands)": dist.data[-1]
        })
            
    df_proj = pd.DataFrame(projections)
    
    # Pivot table for clean district-by-year view
    pivot_df = df_proj.pivot(index="District", columns="Year", values="Projected Pop (Thousands)")
    # Reorder columns chronologically
    pivot_df = pivot_df[[2024, 2025, 2026, 2027, 2028, 2029, 2030]]
    
    print("=" * 85)
    print("LONG-TERM POPULATION PROJECTIONS TO 2030 (in thousands)")
    print("=" * 85)
    print(pivot_df.to_string(formatters={col: "{:.1f}".format for col in pivot_df.columns}))
    print("=" * 85)

if __name__ == "__main__":
    run_task6()