from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

class TaxEngineError(Exception):
    """Base custom exception for all tax engine-related errors."""
    pass

class InvalidIncomeError(TaxEngineError):
    """Raised when income is negative or invalid."""
    pass


class BaseTaxCalculator(ABC):
    """
    Abstract Base Class establishing a strict contract 
    for all tax calculation modules in Uganda.
    """
    
    @abstractmethod
    def calculate_tax(self, gross_income: Decimal) -> Decimal:
        """Calculate the tax liability for a given gross income."""
        pass


class UgandaPAYECalculator(BaseTaxCalculator):
    """
    Computes Uganda's Pay As You Earn (PAYE) monthly individual tax brackets 
    using precise Decimal arithmetic.
    
    Monthly Brackets (Example standard tiers):
    - Up to 235,000 UGX: Exempt (0%)
    - 235,001 to 335,000 UGX: 10% on the excess above 235,000
    - 335,001 to 410,000 UGX: 20% on the excess above 335,000 (+ fixed amount)
    - Above 410,000 UGX: 30% on the excess above 410,000 (+ fixed amounts)
    *(Plus 10% surcharge on monthly income exceeding 10,000,000 UGX if applicable)*
    """
    
    def calculate_tax(self, gross_income: Decimal) -> Decimal:
        if not isinstance(gross_income, Decimal):
            gross_income = Decimal(str(gross_income))
            
        if gross_income < Decimal("0"):
            raise InvalidIncomeError("Gross income cannot be negative.")
            
        tax = Decimal("0.00")
        
        # Tier 1: Up to 235,000 is 0%
        if gross_income <= Decimal("235000"):
            return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
        # Tier 2: Next band (235,001 to 335,000) -> 10%
        excess = gross_income - Decimal("235000")
        if gross_income <= Decimal("335000"):
            tax += excess * Decimal("0.10")
            return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            tax += (Decimal("335000") - Decimal("235000")) * Decimal("0.10")
            
        # Tier 3: Next band (335,001 to 410,000) -> 20%
        if gross_income <= Decimal("410000"):
            excess = gross_income - Decimal("335000")
            tax += excess * Decimal("0.20")
            return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            tax += (Decimal("410000") - Decimal("335000")) * Decimal("0.20")
            
        # Tier 4: Above 410,000 -> 30%
        excess = gross_income - Decimal("410000")
        tax += excess * Decimal("0.30")
        
        # High earner surcharge (30% total or extra 10% on income > 10,000,000)
        if gross_income > Decimal("10000000"):
            surcharge_excess = gross_income - Decimal("10000000")
            tax += surcharge_excess * Decimal("0.10")
            
        return tax.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class UgandaNSSFCalculator(BaseTaxCalculator):
    """
    Computes standard employee NSSF contribution (typically 5% of gross salary).
    """
    def calculate_tax(self, gross_income: Decimal) -> Decimal:
        if not isinstance(gross_income, Decimal):
            gross_income = Decimal(str(gross_income))
            
        if gross_income < Decimal("0"):
            raise InvalidIncomeError("Gross income cannot be negative.")
            
        # Standard employee NSSF is 5%
        contribution = gross_income * Decimal("0.05")
        return contribution.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)