# src/rainfall_model.py
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cosine
from scipy.signal import find_peaks

# --- TASK 1: Region Class ---
class Region:
    """Represents a geographic region and its monthly rainfall data (mm)."""
    def __init__(self, name, rainfall_array):
        self.name = name
        self.rainfall = np.array(rainfall_array, dtype=float)
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def annual_total(self):
        return np.sum(self.rainfall)

    def mean_monthly(self):
        return np.mean(self.rainfall)

    def wettest_month(self):
        idx = np.argmax(self.rainfall)
        return self.months[idx], self.rainfall[idx]

    def driest_month(self):
        idx = np.argmin(self.rainfall)
        return self.months[idx], self.rainfall[idx]

    def coefficient_of_variation(self):
        # CV = Standard Deviation / Mean (using sample std ddof=1)
        return np.std(self.rainfall, ddof=1) / self.mean_monthly()


# --- TASK 2: CropRule Class ---
class CropRule:
    """Defines suitable rainfall ranges and classifies monthly suitability based on agronomic thresholds."""
    def __init__(self, name, min_rain, max_rain, source="FAO / MAAIF Agricultural Guidelines"):
        self.name = name
        self.min_rain = min_rain
        self.max_rain = max_rain
        self.source = source

    def evaluate_month(self, mm):
        if mm < self.min_rain:
            return "Drought risk"
        elif mm > self.max_rain:
            return "Waterlogging risk"
        else:
            return f"Good for {self.name}"


# --- TASK 3: Custom Cosine Similarity ---
def numpy_cosine_similarity(v1, v2):
    """Computes proper vector cosine similarity: dot product divided by product of norms."""
    dot_prod = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_prod / (norm_v1 * norm_v2)


if __name__ == "__main__":
    print("=" * 60)
    print("MINI-PROJECT 4: RAINFALL PATTERN & CROP SUITABILITY ANALYSER")
    print("=" * 60)

    # Raw Data Setup
    data = {
        "Kampala": [120, 140, 180, 200, 220, 180, 90, 70, 60, 100, 110, 130],
        "Gulu":    [  8,  25,  75, 160, 190, 145, 170, 215, 175, 150,  60,  15],
        "Mbarara": [ 70,  85, 120, 140,  90,  25,  20,  55, 100, 125, 120,  90]
    }

    regions = {name: Region(name, vals) for name, vals in data.items()}

    # --- Task 1 Execution ---
    print("\n--- Task 1: Region Statistical Summary ---")
    for name, reg in regions.items():
        wet_m, wet_val = reg.wettest_month()
        dry_m, dry_val = reg.driest_month()
        print(f"Region: {name}")
        print(f"  Annual Total: {reg.annual_total():.1f} mm | Mean Monthly: {reg.mean_monthly():.1f} mm")
        print(f"  Wettest Month: {wet_m} ({wet_val} mm) | Driest Month: {dry_m} ({dry_val} mm)")
        print(f"  Coefficient of Variation (CV): {reg.coefficient_of_variation():.3f}")

    # --- Task 2 Execution ---
    crops = {
        "Maize": CropRule("Maize", min_rain=100.0, max_rain=200.0),
        "Beans": CropRule("Beans", min_rain=50.0, max_rain=120.0),
        "Coffee": CropRule("Coffee", min_rain=130.0, max_rain=250.0)
    }

    print("\n--- Task 2: Crop Suitability Classification Sample (Kampala) ---")
    kampala_rain = regions["Kampala"].rainfall
    for i, month in enumerate(regions["Kampala"].months):
        print(f"  {month} ({kampala_rain[i]} mm):", end=" ")
        for crop_name, rule in crops.items():
            print(f"[{crop_name}: {rule.evaluate_month(kampala_rain[i])}]", end=" ")
        print()

    # --- Task 3 Verification ---
    print("\n--- Task 3: Cosine Similarity Verification ---")
    v1, v2 = regions["Kampala"].rainfall, regions["Gulu"].rainfall
    my_sim = numpy_cosine_similarity(v1, v2)
    # SciPy distance returns 1 - similarity for cosine distance
    scipy_sim = 1.0 - cosine(v1, v2)
    print(f"  Custom NumPy Cosine Similarity: {my_sim:.4f}")
    print(f"  SciPy Spatial Cosine Similarity:  {scipy_sim:.4f}")

    # --- Task 4: Similarity & Distance Matrices ---
    print("\n--- Task 4: Regional Similarity & Distance Matrices ---")
    region_names = list(regions.keys())
    n = len(region_names)
    cosine_mat = np.zeros((n, n))
    pearson_mat = np.zeros((n, n))
    euclid_mat = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            r_i = regions[region_names[i]].rainfall
            r_j = regions[region_names[j]].rainfall
            cosine_mat[i, j] = numpy_cosine_similarity(r_i, r_j)
            pearson_mat[i, j] = np.corrcoef(r_i, r_j)[0, 1]
            euclid_mat[i, j] = np.linalg.norm(r_i - r_j)

    print("Cosine Similarity Matrix:\n", np.round(cosine_mat, 3))
    print("Pearson Correlation Matrix:\n", np.round(pearson_mat, 3))
    print("Euclidean Distance Matrix (mm):\n", np.round(euclid_mat, 2))

    # --- Task 5: Peak Detection & Climate Zone Classification ---
    print("\n--- Task 5: Rainy Season Detection (SciPy Peak Analysis) ---")
    for name, reg in regions.items():
        # find_peaks with prominence or height threshold
        peaks, _ = find_peaks(reg.rainfall, distance=3, prominence=20)
        regime = "Bimodal (Two rainy seasons)" if len(peaks) >= 2 else "Unimodal (Single rainy season)"
        print(f"  {name}: Detected {len(peaks)} peak(s) at month indices {peaks} -> Classified as: {regime}")

    # --- Task 6 & 7: Visualizations ---
    # Line chart of all regions
    plt.figure(figsize=(10, 5))
    for name, reg in regions.items():
        plt.plot(reg.months, reg.rainfall, marker='o', label=f"{name} (Total: {reg.annual_total():.0f}mm)")
    plt.title("Monthly Rainfall Regimes Across Ugandan Regions")
    plt.xlabel("Month")
    plt.ylabel("Rainfall (mm)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --- EXTENSION: Multi-Year Historical Variability & Box Plots ---
def run_extension_boxplots():
    """Simulates 10 years of historical monthly rainfall data to showcase inter-annual variability."""
    np.random.seed(42)
    months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Base monthly profiles with realistic year-to-year noise (standard deviation factor)
    base_profiles = {
        "Kampala": [120, 140, 180, 200, 220, 180, 90, 70, 60, 100, 110, 130],
        "Gulu":    [  8,  25,  75, 160, 190, 145, 170, 215, 175, 150,  60,  15],
        "Mbarara": [ 70,  85, 120, 140,  90,  25,  20,  55, 100, 125, 120,  90]
    }
    
    print("\n" + "=" * 60)
    print("EXTENSION: 10-YEAR HISTORICAL VARIABILITY ANALYSIS")
    print("=" * 60)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)
    
    for idx, (region_name, base_vals) in enumerate(base_profiles.items()):
        # Generate 10 years x 12 months data with normal distribution noise (relative to mean)
        # shape: (10 years, 12 months)
        simulated_10_years = np.zeros((10, 12))
        for m_idx, base_rain in enumerate(base_vals):
            # Add random noise (standard deviation = 20% of monthly mean rainfall, clipped at 0)
            noise = np.random.normal(loc=0.0, scale=max(5.0, 0.2 * base_rain), size=10)
            simulated_10_years[:, m_idx] = np.clip(base_rain + noise, 0, None)
            
        # Plot box plots for each month
        ax = axes[idx]
        ax.boxplot(simulated_10_years, tick_labels=months_list)
        ax.set_title(f"{region_name} (10-Year Variability)")
        ax.set_xlabel("Month")
        if idx == 0:
            ax.set_ylabel("Monthly Rainfall (mm)")
        ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Run the extension after the main script execution
    run_extension_boxplots()