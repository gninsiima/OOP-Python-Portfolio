"""
task3_growth.py
Calculates Year-on-Year growth rates and CAGR for UBOS districts.
"""

from src.data_loader import load_all_districts

def run_task3():
    districts = load_all_districts()
    
    print("=" * 60)
    print("COMPOUND ANNUAL GROWTH RATE (CAGR) - 2015 to 2024")
    print("=" * 60)
    
    cagr_results = {}
    
    for name, dist in districts.items():
        cagr = dist.get_cagr()
        cagr_results[name] = cagr
        print(f"{name:<10}: {cagr:.2f}% per year")
        
    fastest_district = max(cagr_results, key=cagr_results.get)
    print("-" * 60)
    print(f"👉 Fastest growing district in relative terms: **{fastest_district}** ({cagr_results[fastest_district]:.2f}% CAGR)\n")

    print("=" * 60)
    print("YEAR-ON-YEAR (YoY) GROWTH RATES (%)")
    print("=" * 60)
    
    years_yoy = dist.years[1:] # 2016 to 2024
    for name, dist in districts.items():
        yoy = dist.get_yoy_growth_rates()
        yoy_str = ", ".join([f"{rate:.1f}%" for rate in yoy])
        print(f"{name:<10}: [{yoy_str}]")

if __name__ == "__main__":
    run_task3()