import timeit
import numpy as np
import pandas as pd
from scipy.optimize import nnls
from microgrid import MicroGrid

class MicroGridDispatch(MicroGrid):
    """
    Extends MicroGrid to handle 30-day batch solving, vectorisation, 
    timing comparisons, and infeasible output handling (Task 3 & 4).
    """
    def __init__(self, csv_path="data/microgrid_demand_30days.csv"):
        super().__init__()
        self.df = pd.read_csv(csv_path)

    def solve_loop(self):
        """Solves all 30 days iteratively using a standard Python loop."""
        results = []
        for _, row in self.df.iterrows():
            sol = self.solve_day(row['D1_Daytime_Load_kWh'], row['D2_Critical_Load_kWh'])
            results.append(sol)
        return np.array(results)  # Shape: (30, 2)

    def solve_vectorized(self):
        """
        Solves all 30 days in a single vectorized call by stacking 
        demands into a 2x30 right-hand side matrix B.
        """
        # B matrix shape: (2, 30) where row 0 is D1, row 1 is D2
        B = np.vstack([
            self.df['D1_Daytime_Load_kWh'].values,
            self.df['D2_Critical_Load_kWh'].values
        ])
        
        # scipy.linalg.solve handles multi-column B seamlessly: A X = B -> X has shape (2, 30)
        X = np.linalg.solve(self.A, B)
        return X.T  # Transpose back to shape (30, 2) for easy inspection

    def handle_infeasible_outputs(self, solutions):
        """
        Flags negative (infeasible) outputs and handles them using 
        clipping or scipy.optimize.nnls if necessary.
        """
        infeasible_mask = (solutions < 0).any(axis=1)
        infeasible_count = infeasible_mask.sum()
        
        print(f"\n--- Feasibility Check ---")
        print(f"Total days evaluated: {len(solutions)}")
        print(f"Infeasible days detected (negative values): {infeasible_count}")
        
        if infeasible_count > 0:
            print("Flagged days:", np.where(infeasible_mask)[0] + 1)
            # Handling strategy: Clipping negative values to 0 (minimum physical usage)
            cleaned_solutions = np.clip(solutions, 0, None)
            print("Action taken: Clipped negative values to 0 kWh.")
            return cleaned_solutions
        
        return solutions

if __name__ == "__main__":
    planner = MicroGridDispatch()
    
    # Task 3: Time both approaches
    loop_time = timeit.timeit(lambda: planner.solve_loop(), number=100)
    vec_time = timeit.timeit(lambda: planner.solve_vectorized(), number=100)
    
    print("\n--- Task 3: Performance Timing (100 iterations) ---")
    print(f"Python Loop Time:     {loop_time:.6f} seconds")
    print(f"Vectorized Call Time: {vec_time:.6f} seconds")
    print(f"Speedup factor:       {loop_time / vec_time:.2f}x faster with vectorization")
    
    # Run vectorized solve for data processing
    raw_solutions = planner.solve_vectorized()
    
    # Task 4: Handle infeasible outputs
    final_solutions = planner.handle_infeasible_outputs(raw_solutions)