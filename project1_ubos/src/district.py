"""
district.py
Module for managing and analyzing population data for UBOS districts .
"""

from typing import List, Union
import numpy as np
import pandas as pd


class DistrictPopulation:
    """
    Represents and analyzes population data for a specific district over time.
    """
    def __init__(self, district_name:str, years: List[int], populations: List[Union[int,float]]):
        """
        Initialize a DistrictPopulation instance.
        :param district_name: The name of the district.
        :param years: List of years.
        :param populations: List of population counts corresponding to the years.
        """
        if not district_name or not isinstance(district_name, str): 
           raise ValueError("District name must be a non-empty string.")
        
        if not years or not populations :
            raise ValueError("Years and population data list cannot be empty.")
        if len(years) != len(populations):
            raise  ValueError("Years and populations arrays must have equal lengths")

        years_arr = np.array(years,dtype=int)
        pop_arr = np.array(populations,dtype=float)

        if np.any(pop_arr < 0):
            raise ValueError("Population values cannot be negative.")
        
        self.district_name = district_name
        self.years =years_arr
        self.data = pop_arr #populations

    def __len__(self) -> int:
        """Return the number of data points(years) available"""
        return len(self.years)
    
    def __repr__(self) -> str:
        return f"<DistrictPopulation(name)='{self.district_name}', years={len(self.years)} entries)>"

    def get_total_population(self)-> float:
        """Calculate and return the total population across all the years."""
        return float(np.sum(self.data))

    def get_mean_population(self) -> float:
        """Calculate and return the mean population."""
        return float(np.mean(self.data))
    
    def get_median_population(self) -> float:
        """Calculate and return the median population."""
        return float(np.median(self.data))

    def get_std_dev(self, ddof: int =1) -> float:
        """Calculate and return the standard deviation of the population data."""
        return float(np.std(self.data,ddof=ddof)) if len(self.data) >1 else 0.0

    def get_variance(self,ddof: int=1) -> float:
        """Calculate and return of the variance of the population data."""
        return float(np.variance(self.data, ddof=ddof)) if len(self.data) > 1 else 0.0
    
    def get_yoy_growth_rates(self) -> np.ndarray:
        """Calculate year-on-year percentage growth rates."""
        # Using numpy diff for YoY change: (pop[t] - pop[t-1]) / pop[t-1]
        current = self.data[1:]
        previous = self.data[:-1]
        return ((current - previous) / previous) * 100

    def get_cagr(self) -> float:
        """Calculate Compound Annual Growth Rate (CAGR) over the full period."""
        begin_val = self.data[0]
        end_val = self.data[-1]
        n_years = len(self.years) - 1
        return (float((end_val / begin_val) ** (1 / n_years) - 1)) * 100

    

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the district population data into a pandas DataFrame"""

        return pd.DataFrame({
            "Year": self.years,
            "District": [self.district_name]*len(self.years),
            "Population": self.data
        })
    
    
    


