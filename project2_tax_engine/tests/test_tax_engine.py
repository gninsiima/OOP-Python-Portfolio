import json
from decimal import Decimal
from pathlib import Path
import pytest

from src.tax_engine import (
    UgandaPAYECalculator,
    UgandaNSSFCalculator,
    InvalidIncomeError,
)

def test_negative_income_raises_error():
    """Ensure that passing negative income throws our custom exception."""
    paye_calc = UgandaPAYECalculator()
    nssf_calc = UgandaNSSFCalculator()
    
    with pytest.raises(InvalidIncomeError):
        paye_calc.calculate_tax(Decimal("-50000"))
        
    with pytest.raises(InvalidIncomeError):
        nssf_calc.calculate_tax(Decimal("-10000"))


def test_nssf_calculation():
    """Verify NSSF is correctly calculated at 5%."""
    nssf_calc = UgandaNSSFCalculator()
    # 5% of 400,000 is 20,000
    assert nssf_calc.calculate_tax(Decimal("400000")) == Decimal("20000.00")


def test_paye_with_fixture_data():
    """Load test cases from JSON fixture and test PAYE and NSSF calculations."""
    fixture_path = Path(__file__).parent / "fixtures" / "tax_sample.json"
    with open(fixture_path, "r") as f:
        test_cases = json.load(f)
        
    paye_calc = UgandaPAYECalculator()
    nssf_calc = UgandaNSSFCalculator()
    
    for case in test_cases:
        income = Decimal(case["gross_income"])
        expected_paye = Decimal(case["expected_paye"])
        expected_nssf = Decimal(case["expected_nssf"])
        
        assert paye_calc.calculate_tax(income) == expected_paye, f"Failed on PAYE for {case['description']}"
        assert nssf_calc.calculate_tax(income) == expected_nssf, f"Failed on NSSF for {case['description']}"