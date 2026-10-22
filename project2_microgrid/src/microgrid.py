import numpy as np
from scipy.linalg import solve

class MicroGrid:
    """
    A class to model and solve energy dispatch for a rural health centre micro-grid.
    System of equations:
    3x + 2y = D1 (Daytime load)
    4x + y  = D2 (Critical-equipment load)
    """
    def __init__(self):
        # Coefficient matrix A
        self.A = np.array([
            [3, 2],
            [4, 1]
        ], dtype=float)
        
        # Validate well-posedness upon initialization
        self._validate_system()

    def _validate_system(self):
        """Computes determinant and condition number to check system health."""
        self.det = np.linalg.det(self.A)
        self.cond_num = np.linalg.cond(self.A)
        
        print("--- MicroGrid System Validation ---")
        print(f"Determinant: {self.det:.4f} (Non-zero means unique solution exists)")
        print(f"Condition Number: {self.cond_num:.4f} (Measures sensitivity to small demand changes)")
        
        if np.isclose(self.det, 0):
            raise ValueError("System matrix is singular! No unique solution exists.")

    def solve_day(self, d1: float, d2: float) -> np.ndarray:
        """
        Solves for daily solar (x) and battery (y) usage given demands D1 and D2.
        """
        b = np.array([d1, d2], dtype=float)
        # Using scipy.linalg.solve for linear system
        solution = solve(self.A, b)
        return solution

# Quick test if run directly
if __name__ == "__main__":
    mg = MicroGrid()
    # Test with sample loads: D1 = 100 kWh, D2 = 80 kWh
    x, y = mg.solve_day(100, 80)
    print(f"\nTest Dispatch -> Solar (x): {x:.2f} kWh, Battery (y): {y:.2f} kWh")