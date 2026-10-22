# Mini-Project 2: Solar Micro-Grid Dispatch Planner
**Context:** Rural Health Center Dispatch Planning in Kasese, Uganda  
**Course/Project:** MSDS Object-Oriented Python & Linear Algebra  

---

## 📂 Project Structure
```text
│
├── data/
│   └── microgrid_demand_30days.csv  # Generated 30-day demand dataset
├── src/
│   ├── __init__.py
│   ├── microgrid.py                 # Base class: 2x2 system, determinant, condition number
│   ├── data_generator.py            # Synthetic data generation with reproducible seeds
│   ├── dispatch_planner.py          # Task 3-7: Batch solving, vectorization, cost model, stats
│   └── hybrid_microgrid.py          # Extension: 3x3 hybrid model, linear dependence, Monte Carlo
├── venv/                            # Python virtual environment
└── README.md
