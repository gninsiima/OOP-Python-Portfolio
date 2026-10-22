"""
task8_planning.py
Translates 2030 population projections into school classroom requirements for UBOS districts.
"""

import pandas as pd
import numpy as np
from src.data_loader import load_all_districts
from src.forecasters import ExponentialForecaster

def run_task8():
    districts = load_all_districts()
    model = ExponentialForecaster()
    
    # Planning parameters
    SCHOOL_AGE_PCT = 0.25      # 25% of population is school-age
    ENROLLMENT_RATE = 0.80     # 80% enrollment rate
    STUDENTS_PER_CLASS = 45    # Target policy limit per classroom
    
    horizon = 6  # 2024 to 2030
    
    planning_results = []
    
    for name, dist in districts.items():
        # Fit on full historical data and project to 2030
        model.fit(dist.years, dist.data)
        preds = model.predict(horizon)
        pop_2030_thousands = preds[-1]  # 2030 value is the last element in horizon
        pop_2030_actual = pop_2030_thousands * 1000  # convert thousands to actual persons
        
        pop_2024_actual = dist.data[-1] * 1000
        
        # Calculations for 2024 (Baseline)
        students_2024 = pop_2024_actual * SCHOOL_AGE_PCT * ENROLLMENT_RATE
        classrooms_2024 = np.ceil(students_2024 / STUDENTS_PER_CLASS)
        
        # Calculations for 2030 (Projected)
        students_2030 = pop_2030_actual * SCHOOL_AGE_PCT * ENROLLMENT_RATE
        classrooms_2030 = np.ceil(students_2030 / STUDENTS_PER_CLASS)
        
        new_classrooms_needed = classrooms_2030 - classrooms_2024
        
        planning_results.append({
            "District": name,
            "2030 Pop (k)": round(pop_2030_thousands, 1),
            "Est. Students (2030)": int(students_2030),
            "Required Classrooms (2030)": int(classrooms_2030),
            "Current Classrooms (2024)": int(classrooms_2024),
            "New Classrooms to Build": int(new_classrooms_needed)
        })
        
    df_plan = pd.DataFrame(planning_results)
    
    print("=" * 85)
    print("TASK 8: 2030 EDUCATIONAL RESOURCE PLANNING (Classroom Requirements)")
    print("=" * 85)
    print(df_plan.to_string(index=False))
    print("=" * 85)

if __name__ == "__main__":
    run_task8()