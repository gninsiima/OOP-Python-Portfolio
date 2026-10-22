import pytest
from src.district import DistrictPopulation

def test_district_calculations():
    # Arrange 
    data = [1000, 2000, 3000, 4000]
    district = DistrictPopulation("North", data)

    #Act & Assert
    assert district.get_total_population()==10000.0
    assert district.get_mean_population()==2500.0
    assert district.get_median_population()==2500.0
    assert district.get_std_dev() > 0
    assert district.get_summary_stats()["min"]==1000.0
    assert district.get_summary_stats()["max"]==4000.0

def test_district_validation():
    #Ensure invalid inputs raise a ValueError
    with pytest.raises(ValueError):
        DistrictPopulation("",[100,200])

    with pytest.raises(ValueError):
        DistrictPopulation("Empty",[])