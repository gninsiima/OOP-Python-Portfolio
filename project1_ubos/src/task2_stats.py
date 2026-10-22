import statistics
import numpy as np
from src.data_loader import load_all_districts

def run_task2():
    districts = load_all_districts()
    
    print(f"{'District':<10} | {'Std (np ddof=1)':<15} | {'Var (np ddof=1)':<15} | {'Var (stats)':<15}")
    print("-" * 63)
    
    for name, dist in districts.items():
        pop_list = dist.data.tolist()
        
        # NumPy stats (sample variance/std with ddof=1)
        np_var = np.var(dist.data, ddof=1)
        np_std = np.std(dist.data, ddof=1)
        
        # Python statistics module stats
        stats_var = statistics.variance(pop_list)
        
        print(f"{name:<10} | {np_std:<15.4f} | {np_var:<15.4f} | {stats_var:<15.4f}")

if __name__ == "__main__":
    run_task2()