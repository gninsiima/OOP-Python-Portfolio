# Uganda Tax Engine (Mini-Project 2)

An object-oriented Python tax calculation engine designed to handle Ugandan statutory deductions (PAYE and NSSF) with high financial precision.

## Features
- **Object-Oriented Design:** Uses Abstract Base Classes (`abc.ABC`) to define standardized tax calculators.
- **Absolute Financial Precision:** Built using Python's `decimal.Decimal` to avoid floating-point rounding errors.
- **Robust Exception Handling:** Custom exception classes (`InvalidIncomeError`) for invalid inputs.
- **Tested & Verified:** Comprehensive test suite with `pytest` and JSON fixtures.

## Project Structure
## 📁 Project Structure

```text
project2_tax_engine/
│
├── src/
│   └── tax_engine.py       # Core logic for PAYE, VAT, and tax bracket calculations
│
├── tests/
│   └── test_tax_engine.py  # Unit test suite verifying tax calculations and edge cases
│
├── .gitignore              # Standard Python gitignore rules
├── README.md               # Project documentation and summary of findings
└── requirements.txt        # Project dependencies (pytest, etc.)

# Summary of Findings & Key Insights

1. **Progressive Tax Structure:**
   * Ugandan Pay As You Earn (PAYE) follows a multi-tiered progressive bracket system. Standard income up to 235,000 UGX is exempt, while higher income tiers are taxed incrementally (10%, 20%, and 30%).
   * For ultra-high earners (monthly gross > 10,000,000 UGX), an additional 10% surtax applies to chargeable income above the 10M threshold, ensuring proper statutory compliance.

2. **Validation & Edge Case Handling:**
   * Input validation prevents calculations on negative income amounts or invalid VAT inputs by raising explicit `ValueError` exceptions.
   * Statutory calculations are rounded to two decimal places to ensure monetary precision and prevent cumulative floating-point rounding errors across payroll calculations.

3. **Test Automation & Reliability:**
   * Automated testing using `pytest` guarantees accurate calculation across all tax brackets, boundary thresholds (e.g., exactly 235,000 UGX or 335,000 UGX), and special exemption cases.

   ## AI Assistance & Academic Integrity Declaration

In accordance with course guidelines, AI coding assistants (specifically Gemini) were utilized during the development of this project as collaborative tools for:
* Structuring project files and drafting initial boilerplate unit test templates.
* Refining documentation, including drafting the project structure and summary of findings.
* Troubleshooting Git workflow commands and terminal errors.

All core logic, implementation details, test verifications, and final code execution were thoroughly reviewed, understood, and validated by the author.