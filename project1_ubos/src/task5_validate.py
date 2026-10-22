"""
task5_validate.py
Validates forecasting models on 2015-2021 train data and evaluates on 2022-2024 test data.
Computes MAE, RMSE, and MAPE.
"""

import numpy as np
import pandas as pd
from src.data_loader import load_all_districts
from src.forecasters import LinearForecaster, ExponentialForecaster, FibonacciForecaster

def calculate_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict:
    """Compute MAE, RMSE, and MAPE."""
    mae = np.mean(np.abs(actual - predicted))
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}

def run_task5():
    districts = load_all_districts()
    models = {
        "Linear": LinearForecaster(),
        "Exponential": ExponentialForecaster(),
        "Fibonacci": FibonacciForecaster()
    }
    
    results = []

    for dist_name, dist in districts.items():
        # Split data: Train (2015-2021 -> indices 0 to 6), Test (2022-2024 -> indices 7 to 9)
        train_mask = dist.years <= 2021
        test_mask = dist.years > 2021
        
        train_years = dist.years[train_mask]
        train_values = dist.data[train_mask]
        actual_test_values = dist.data[test_mask]
        
        horizon = len(actual_test_values) # 3 years (2022, 2023, 2024)
        
        for model_name, model in models.items():
            # Fit on training data
            model.fit(train_years, train_values)
            # Predict test horizon
            pred_values = model.predict(horizon)
            
            # Calculate error metrics
            metrics = calculate_metrics(actual_test_values, pred_values)
            
            results.append({
                "District": dist_name,
                "Model": model_name,
                "MAE": metrics["MAE"],
                "RMSE": metrics["RMSE"],
                "MAPE (%)": metrics["MAPE"]
            })

    # Convert results to a clean DataFrame and print
    df_results = pd.DataFrame(results)
    
    print("=" * 70)
    print("MODEL VALIDATION RESULTS (Train: 2015-2021 | Test: 2022-2024)")
    print("=" * 70)
    print(df_results.to_string(index=False, formatters={
        "MAE": "{:.2f}".format,
        "RMSE": "{:.2f}".format,
        "MAPE (%)": "{:.2f}%".format
    }))
    print("=" * 70)

if __name__ == "__main__":
    run_task5()