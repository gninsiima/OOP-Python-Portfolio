import numpy as np
import matplotlib.pyplot as plt
from microgrid import MicroGrid

class HybridMicroGrid(MicroGrid):
    """
    Extension: Adds a diesel generator (z) and a 3rd constraint,
    expanding the system to 3x3. Also tests linear dependence and Monte Carlo sensitivity.
    """
    def __init__(self):
        super().__init__()
        # 3x3 Coefficient matrix including diesel generator (z)
        # Rows: [3x + 2y + z], [4x + y + 2z], [x + 3y + 4z]
        self.A_hybrid = np.array([
            [3, 2, 1],
            [4, 1, 2],
            [1, 3, 4]
        ], dtype=float)
        
        # Check determinant for the 3x3 system
        det_3x3 = np.linalg.det(self_A := self.A_hybrid)
        cond_3x3 = np.linalg.cond(self.A_hybrid)
        
        print("--- HybridMicroGrid (3x3) System Validation ---")
        print(f"3x3 Determinant: {det_3x3:.4f}")
        print(f"3x3 Condition Number: {cond_3x3:.4f}")

    def solve_hybrid_day(self, d1: float, d2: float, d3: float) -> np.ndarray:
        """Solves the 3x3 system for Solar (x), Battery (y), and Diesel (z)."""
        b = np.array([d1, d2, d3], dtype=float)
        return np.linalg.solve(self.A_hybrid, b)

    def demonstrate_linear_dependence(self):
        """Shows what happens if the 3rd constraint is linearly dependent."""
        print("\n--- Demonstrating Linear Dependence ---")
        # Let's make row 3 an exact linear combination of row 1 and row 2
        A_dependent = np.array([
            [3, 2, 1],
            [4, 1, 2],
            [7, 3, 3]  # Row 3 = Row 1 + Row 2
        ], dtype=float)
        
        det = np.linalg.det(A_dependent)
        print(f"Dependent Matrix Determinant: {det:.4f}")
        try:
            np.linalg.solve(A_dependent, np.array([100, 80, 180], dtype=float))
        except np.LinAlgError as e:
            print(f"Caught expected LinAlgError: Matrix is singular! ({e})")

    def monte_carlo_sensitivity(self, base_d1=100.0, base_d2=80.0, draws=1000):
        """
        Runs Monte Carlo simulation perturbing D1 and D2 by +/- 5%.
        Relates output variance to the condition number.
        """
        print(f"\n--- Monte Carlo Sensitivity Analysis ({draws} draws, +/- 5% perturbation) ---")
        
        # Perturb D1 and D2 uniformly by +/- 5%
        np.random.seed(42)
        d1_perturbed = np.random.uniform(base_d1 * 0.95, base_d1 * 1.05, draws)
        d2_perturbed = np.random.uniform(base_d2 * 0.95, base_d2 * 1.05, draws)
        
        # Solve for all draws using our base 2x2 system
        # A X = B -> X = A^-1 B
        B_matrix = np.vstack([d1_perturbed, d2_perturbed])
        solutions = np.linalg.solve(self.A, B_matrix) # Shape: (2, 1000)
        
        x_solar = solutions[0, :]
        y_battery = solutions[1, :]
        
        print(f"Solar (x) output spread -> Mean: {np.mean(x_solar):.2f}, Std Dev: {np.std(x_solar):.2f}")
        print(f"Battery (y) output spread -> Mean: {np.mean(y_battery):.2f}, Std Dev: {np.std(y_battery):.2f}")
        print(f"Condition Number Reminder: {self.cond_num:.2f} (Limits error amplification)")

        # Optional: Plot distribution
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes[0].hist(x_solar, bins=30, color='#f39c12', edgecolor='black', alpha=0.7)
        axes[0].set_title('Solar (x) Sensitivity Distribution (+/- 5% Demand)')
        axes[0].set_xlabel('Solar Generation (kWh)')
        axes[0].set_ylabel('Frequency')

        axes[1].hist(y_battery, bins=30, color='#3498db', edgecolor='black', alpha=0.7)
        axes[1].set_title('Battery (y) Sensitivity Distribution (+/- 5% Demand)')
        axes[1].set_xlabel('Battery Usage (kWh)')
        axes[1].set_ylabel('Frequency')

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    hybrid = HybridMicroGrid()
    
    # Test 3x3 solve
    x, y, z = hybrid.solve_hybrid_day(120, 90, 110)
    print(f"Hybrid Dispatch Test -> Solar: {x:.2f}, Battery: {y:.2f}, Diesel: {z:.2f}")
    
    # Demonstrate linear dependence
    hybrid.demonstrate_linear_dependence()
    
    # Run Monte Carlo sensitivity analysis
    hybrid.monte_carlo_sensitivity()