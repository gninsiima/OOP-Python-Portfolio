my_project_root/
│
├── venv/                              # Python virtual environment
├── district_population_forecasts.png  # Standard visualization chart
├── district_population_forecasts_bootstrap.png  # Enhanced chart with 95% intervals
├── README.md                          # Project documentation
│
└── src/                               # Source package folder
    ├── data_loader.py                 # District data loader & dictionary initialization
    ├── district.py                    # DistrictPopulation class (Stats, YoY, CAGR)
    ├── forecasters.py                 # Abstract Forecaster base class & model subclasses
    ├── task2_stats.py                 # Statistical benchmarks (NumPy vs statistics module)
    ├── task3_growth.py                # Year-on-Year growth rates and CAGR analysis
    ├── task5_validate.py              # Train/Test model validation (MAE, RMSE, MAPE)
    ├── task6_project.py               # Long-term exponential population projections to 2030
    ├── task7_visualize.py             # Generates  historical population data and 2030 exponential projections 
    └── task8_planning.py              # Educational resource planning (Classroom requirements)
    └── extention.py              # Generates historical data, 2030 exponential forecasts, and 95% bootstrap prediction intervals.