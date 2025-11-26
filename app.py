from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
import math
import random
from collections import Counter

app = Flask(__name__)

# Define all 100 calculators with their metadata
CALCULATORS = [
    {'id': 'acceleration', 'name': 'Acceleration', 'category': 'Physics', 'description': 'Calculate acceleration'},
    {'id': 'date_add', 'name': 'Add Days to Date', 'category': 'Date & Time', 'description': 'Add days to a date'},
    {'id': 'age', 'name': 'Age Calculator', 'category': 'Date & Time', 'description': 'Calculate your exact age'},
    {'id': 'age_difference', 'name': 'Age Difference', 'category': 'Date & Time', 'description': 'Calculate age difference'},
    {'id': 'alcohol_units', 'name': 'Alcohol Units', 'category': 'Health', 'description': 'Calculate alcohol units'},
    {'id': 'area-converter', 'name': 'Area Converter', 'category': 'Unit Conversion', 'description': 'Convert area units'},
    {'id': 'bmi', 'name': 'BMI Calculator', 'category': 'Health', 'description': 'Calculate Body Mass Index'},
    {'id': 'bmr', 'name': 'BMR Calculator', 'category': 'Health', 'description': 'Calculate Basal Metabolic Rate'},
    {'id': 'binary', 'name': 'Binary Converter', 'category': 'Math', 'description': 'Convert decimal to binary'},
    {'id': 'body_fat', 'name': 'Body Fat Percentage', 'category': 'Health', 'description': 'Estimate body fat percentage'},
    {'id': 'cgpa', 'name': 'CGPA Calculator', 'category': 'Education', 'description': 'Calculate Cumulative GPA'},
    {'id': 'calories_burned', 'name': 'Calories Burned', 'category': 'Health', 'description': 'Calculate calories burned'},
    {'id': 'car_loan', 'name': 'Car Loan', 'category': 'Automotive', 'description': 'Calculate car loan payment'},
    {'id': 'carbon_footprint', 'name': 'Carbon Footprint', 'category': 'Environment', 'description': 'Calculate carbon footprint'},
    {'id': 'carbs_needs', 'name': 'Carbs Needs', 'category': 'Health', 'description': 'Calculate daily carbs'},
    {'id': 'area_circle', 'name': 'Circle Area', 'category': 'Math', 'description': 'Calculate circle area'},
    {'id': 'combination', 'name': 'Combination', 'category': 'Math', 'description': 'Calculate combinations'},
    {'id': 'compound_interest', 'name': 'Compound Interest', 'category': 'Finance', 'description': 'Calculate compound interest'},
    {'id': 'concrete', 'name': 'Concrete Calculator', 'category': 'Home', 'description': 'Calculate concrete needed'},
    {'id': 'cooking_time', 'name': 'Cooking Time', 'category': 'Cooking', 'description': 'Calculate cooking time'},
    {'id': 'correlation', 'name': 'Correlation Coefficient', 'category': 'Statistics', 'description': 'Calculate correlation'},
    {'id': 'countdown', 'name': 'Countdown Timer', 'category': 'Date & Time', 'description': 'Calculate time until event'},
    {'id': 'volume_cube', 'name': 'Cube Volume', 'category': 'Math', 'description': 'Calculate cube volume'},
    {'id': 'currency_converter', 'name': 'Currency Converter', 'category': 'Finance', 'description': 'Convert between currencies'},
    {'id': 'volume_cylinder', 'name': 'Cylinder Volume', 'category': 'Math', 'description': 'Calculate cylinder volume'},
    {'id': 'water_intake', 'name': 'Daily Water Intake', 'category': 'Health', 'description': 'Calculate daily water needs'},
    {'id': 'weekday', 'name': 'Day of Week', 'category': 'Date & Time', 'description': 'Find day of week for a date'},
    {'id': 'days_between', 'name': 'Days Between Dates', 'category': 'Date & Time', 'description': 'Calculate days between two dates'},
    {'id': 'density', 'name': 'Density Calculator', 'category': 'Physics', 'description': 'Calculate density'},
    {'id': 'discount', 'name': 'Discount Calculator', 'category': 'Finance', 'description': 'Calculate discount price'},
    {'id': 'distance', 'name': 'Distance Calculator', 'category': 'Math', 'description': 'Calculate distance between points'},
    {'id': 'electricity_cost', 'name': 'Electricity Cost', 'category': 'Home', 'description': 'Calculate electricity cost'},
    {'id': 'unit_energy', 'name': 'Energy Converter', 'category': 'Unit Conversion', 'description': 'Convert energy units'},
    {'id': 'factorial', 'name': 'Factorial Calculator', 'category': 'Math', 'description': 'Calculate factorial'},
    {'id': 'fence', 'name': 'Fence Calculator', 'category': 'Home', 'description': 'Calculate fence materials'},
    {'id': 'fiber_needs', 'name': 'Fiber Needs', 'category': 'Health', 'description': 'Calculate daily fiber'},
    {'id': 'fibonacci', 'name': 'Fibonacci Sequence', 'category': 'Math', 'description': 'Generate Fibonacci sequence'},
    {'id': 'final_grade', 'name': 'Final Grade Needed', 'category': 'Education', 'description': 'Calculate grade needed on final'},
    {'id': 'flooring', 'name': 'Flooring Calculator', 'category': 'Home', 'description': 'Calculate flooring needed'},
    {'id': 'force', 'name': 'Force Calculator', 'category': 'Physics', 'description': 'Calculate force (F=ma)'},
    {'id': 'fuel_cost', 'name': 'Fuel Cost', 'category': 'Automotive', 'description': 'Calculate trip fuel cost'},
    {'id': 'fuel_efficiency', 'name': 'Fuel Efficiency', 'category': 'Automotive', 'description': 'Calculate MPG/KPL'},
    {'id': 'gcd', 'name': 'GCD Calculator', 'category': 'Math', 'description': 'Find Greatest Common Divisor'},
    {'id': 'gpa', 'name': 'GPA Calculator', 'category': 'Education', 'description': 'Calculate Grade Point Average'},
    {'id': 'grade', 'name': 'Grade Calculator', 'category': 'Education', 'description': 'Calculate grade percentage'},
    {'id': 'hex', 'name': 'Hexadecimal Converter', 'category': 'Math', 'description': 'Convert to hexadecimal'},
    {'id': 'ideal_weight', 'name': 'Ideal Weight', 'category': 'Health', 'description': 'Calculate ideal body weight'},
    {'id': 'investment_return', 'name': 'Investment Return', 'category': 'Finance', 'description': 'Calculate investment returns'},
    {'id': 'kinetic_energy', 'name': 'Kinetic Energy', 'category': 'Physics', 'description': 'Calculate kinetic energy'},
    {'id': 'lcm', 'name': 'LCM Calculator', 'category': 'Math', 'description': 'Find Least Common Multiple'},
    {'id': 'leap_year', 'name': 'Leap Year Checker', 'category': 'Date & Time', 'description': 'Check if a year is a leap year'},
    {'id': 'lease_vs_buy', 'name': 'Lease vs Buy', 'category': 'Automotive', 'description': 'Compare lease vs buy'},
    {'id': 'unit_length', 'name': 'Length Converter', 'category': 'Unit Conversion', 'description': 'Convert length units'},
    {'id': 'loan_payment', 'name': 'Loan Payment', 'category': 'Finance', 'description': 'Calculate monthly loan payment'},
    {'id': 'mean', 'name': 'Mean Calculator', 'category': 'Statistics', 'description': 'Calculate mean/average'},
    {'id': 'median', 'name': 'Median Calculator', 'category': 'Statistics', 'description': 'Calculate median'},
    {'id': 'mode', 'name': 'Mode Calculator', 'category': 'Statistics', 'description': 'Calculate mode'},
    {'id': 'momentum', 'name': 'Momentum', 'category': 'Physics', 'description': 'Calculate momentum'},
    {'id': 'mortgage', 'name': 'Mortgage Calculator', 'category': 'Finance', 'description': 'Calculate mortgage payments'},
    {'id': 'next_birthday', 'name': 'Next Birthday', 'category': 'Date & Time', 'description': 'Days until next birthday'},
    {'id': 'octal', 'name': 'Octal Converter', 'category': 'Math', 'description': 'Convert to octal'},
    {'id': 'oven_temp', 'name': 'Oven Temperature', 'category': 'Cooking', 'description': 'Convert oven temperatures'},

    {'id': 'paint_needed', 'name': 'Paint Needed', 'category': 'Home', 'description': 'Calculate paint needed'},
    {'id': 'percentage', 'name': 'Percentage Calculator', 'category': 'Math', 'description': 'Calculate percentages'},
    {'id': 'percentage_change', 'name': 'Percentage Change', 'category': 'Math', 'description': 'Calculate percentage change'},
    {'id': 'percentage_of', 'name': 'Percentage Of', 'category': 'Math', 'description': 'Find percentage of a number'},
    {'id': 'permutation', 'name': 'Permutation', 'category': 'Math', 'description': 'Calculate permutations'},
    {'id': 'potential_energy', 'name': 'Potential Energy', 'category': 'Physics', 'description': 'Calculate potential energy'},
    {'id': 'power_physics', 'name': 'Power (Physics)', 'category': 'Physics', 'description': 'Calculate power'},
    {'id': 'unit_power', 'name': 'Power Converter', 'category': 'Unit Conversion', 'description': 'Convert power units'},

    {'id': 'pressure_physics', 'name': 'Pressure (Physics)', 'category': 'Physics', 'description': 'Calculate pressure'},
    {'id': 'unit_pressure', 'name': 'Pressure Converter', 'category': 'Unit Conversion', 'description': 'Convert pressure units'},
    {'id': 'prime_check', 'name': 'Prime Number Checker', 'category': 'Math', 'description': 'Check if number is prime'},
    {'id': 'protein_needs', 'name': 'Protein Needs', 'category': 'Health', 'description': 'Calculate daily protein'},
    {'id': 'pythagorean', 'name': 'Pythagorean Theorem', 'category': 'Math', 'description': 'Calculate triangle sides'},
    {'id': 'quadratic', 'name': 'Quadratic Equation', 'category': 'Math', 'description': 'Solve quadratic equations'},
    {'id': 'random_number', 'name': 'Random Number', 'category': 'Math', 'description': 'Generate random numbers'},
    {'id': 'recipe_scaler', 'name': 'Recipe Scaler', 'category': 'Cooking', 'description': 'Scale recipe ingredients'},
    {'id': 'area_rectangle', 'name': 'Rectangle Area', 'category': 'Math', 'description': 'Calculate rectangle area'},
    {'id': 'recycling', 'name': 'Recycling Impact', 'category': 'Environment', 'description': 'Calculate recycling impact'},
    {'id': 'retirement', 'name': 'Retirement Savings', 'category': 'Finance', 'description': 'Calculate retirement savings'},
    {'id': 'roman_numeral', 'name': 'Roman Numeral', 'category': 'Math', 'description': 'Convert to/from Roman numerals'},
    {'id': 'roofing', 'name': 'Roofing Calculator', 'category': 'Home', 'description': 'Calculate roofing materials'},
    {'id': 'savings_goal', 'name': 'Savings Goal', 'category': 'Finance', 'description': 'Calculate savings needed for goal'},
    {'id': 'simple_interest', 'name': 'Simple Interest', 'category': 'Finance', 'description': 'Calculate simple interest'},
    {'id': 'sleep_hours', 'name': 'Sleep Hours', 'category': 'Health', 'description': 'Calculate sleep cycles'},
    {'id': 'slope', 'name': 'Slope Calculator', 'category': 'Math', 'description': 'Calculate line slope'},
    {'id': 'solar_panels', 'name': 'Solar Panels', 'category': 'Home', 'description': 'Calculate solar panel needs'},
    {'id': 'speed', 'name': 'Speed Calculator', 'category': 'Physics', 'description': 'Calculate speed'},
    {'id': 'unit_speed', 'name': 'Speed Converter', 'category': 'Unit Conversion', 'description': 'Convert speed units'},
    {'id': 'volume_sphere', 'name': 'Sphere Volume', 'category': 'Math', 'description': 'Calculate sphere volume'},
    {'id': 'standard_deviation', 'name': 'Standard Deviation', 'category': 'Statistics', 'description': 'Calculate standard deviation'},
    {'id': 'heart_rate', 'name': 'Target Heart Rate', 'category': 'Health', 'description': 'Calculate target heart rate zone'},
    {'id': 'unit_temperature', 'name': 'Temperature Converter', 'category': 'Unit Conversion', 'description': 'Convert temperature'},
    {'id': 'test_score', 'name': 'Test Score', 'category': 'Education', 'description': 'Calculate test score percentage'},
    {'id': 'tile_needed', 'name': 'Tile Needed', 'category': 'Home', 'description': 'Calculate tiles needed'},
    {'id': 'unit_time', 'name': 'Time Converter', 'category': 'Unit Conversion', 'description': 'Convert time units'},
    {'id': 'time_zone', 'name': 'Time Zone Converter', 'category': 'Date & Time', 'description': 'Convert time zones'},
    {'id': 'tip_calculator', 'name': 'Tip Calculator', 'category': 'Finance', 'description': 'Calculate tip amount'},
    {'id': 'tire_size', 'name': 'Tire Size', 'category': 'Automotive', 'description': 'Calculate tire dimensions'},
    {'id': 'area_trapezoid', 'name': 'Trapezoid Area', 'category': 'Math', 'description': 'Calculate trapezoid area'},
    {'id': 'tree_offset', 'name': 'Tree Offset', 'category': 'Environment', 'description': 'Calculate trees to offset CO2'},
    {'id': 'area_triangle', 'name': 'Triangle Area', 'category': 'Math', 'description': 'Calculate triangle area'},
    {'id': 'variance', 'name': 'Variance Calculator', 'category': 'Statistics', 'description': 'Calculate variance'},
    {'id': 'unit_volume', 'name': 'Volume Converter', 'category': 'Unit Conversion', 'description': 'Convert volume units'},
    {'id': 'unit_weight', 'name': 'Weight Converter', 'category': 'Unit Conversion', 'description': 'Convert weight units'},
    {'id': 'work', 'name': 'Work Calculator', 'category': 'Physics', 'description': 'Calculate work done'},
    {'id': 'work_days', 'name': 'Work Days', 'category': 'Date & Time', 'description': 'Calculate work days between dates'},
]

def get_float_value(data, key, default=None, required=True):
    """Helper function to safely get and validate float values"""
    value = data.get(key)
    if value is None or value == "":
        if required:
            return None, f"Error: Please provide {key.replace('_', ' ')}"
        return default, None
    try:
        return float(value), None
    except (ValueError, TypeError):
        return None, f"Error: {key.replace('_', ' ')} must be a valid number"

def calculate(calc_id, data):
    """Perform calculations based on calculator ID"""
    try:
        # Date & Time Calculators
        if calc_id == "age":
            dob_str = data.get("dob")
            if not dob_str:
                return "Error: Please provide a date of birth"
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            today = datetime.today()
            years = today.year - dob.year
            months = today.month - dob.month
            days = today.day - dob.day
            if months < 0:
                years -= 1
                months += 12
            if days < 0:
                months -= 1
                prev_month = today.replace(day=1) - timedelta(days=1)
                days += (today - prev_month).days
            return f"Age: {years} years, {months} months, {days} days"
        
        elif calc_id == "days_between":
            date1_str = data.get("date1")
            date2_str = data.get("date2")
            if not date1_str or not date2_str:
                return "Error: Please provide both dates"
            date1 = datetime.strptime(date1_str, "%Y-%m-%d")
            date2 = datetime.strptime(date2_str, "%Y-%m-%d")
            days = abs((date2 - date1).days)
            return f"Days between: {days} days"
        
        elif calc_id == "date_add":
            date_str = data.get("date")
            if not date_str:
                return "Error: Please provide a date"
            date = datetime.strptime(date_str, "%Y-%m-%d")
            days = int(float(data.get("days", 0)))
            result_date = date + timedelta(days=days)
            return f"Result Date: {result_date.strftime('%Y-%m-%d')}"
        
        elif calc_id == "weekday":
            date_str = data.get("date")
            if not date_str:
                return "Error: Please provide a date"
            date = datetime.strptime(date_str, "%Y-%m-%d")
            weekday = date.strftime("%A")
            return f"Day of Week: {weekday}"
        
        elif calc_id == "leap_year":
            year = int(float(data.get("year")))
            is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
            return f"{year} is {'a leap year' if is_leap else 'not a leap year'}"
        
        elif calc_id == "age_difference":
            date1_str = data.get("date1")
            date2_str = data.get("date2")
            if not date1_str or not date2_str:
                return "Error: Please provide both dates"
            date1 = datetime.strptime(date1_str, "%Y-%m-%d")
            date2 = datetime.strptime(date2_str, "%Y-%m-%d")
            diff = abs((date2 - date1).days)
            years = diff // 365
            months = (diff % 365) // 30
            days = (diff % 365) % 30
            return f"Age Difference: {years} years, {months} months, {days} days"
        
        elif calc_id == "countdown":
            date_str = data.get("date")
            if not date_str:
                return "Error: Please provide a target date"
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.today()
            days = (target_date - today).days
            return f"Days Until Event: {days} days"

        
        elif calc_id == "area-converter":
            value = data.get("value")
            from_unit = data.get("fromUnit")
            to_unit = data.get("toUnit")

            if value is None or value == "":
                return "Error: Please enter a value"

            if not from_unit or not to_unit:
                return "Error: Please select both units"

            try:
                value = float(value)
            except:
                return "Error: Please enter a valid number"

            conversion = {
        "sqm": 1,
        "sqcm": 0.0001,
        "sqkm": 1000000,
        "sqft": 0.092903,
        "sqin": 0.00064516,
        "sqyd": 0.836127,
        "acre": 4046.8564224,
        "hectare": 10000
    }

            if from_unit not in conversion or to_unit not in conversion:
                return "Error: Invalid unit selected"

            value_in_sqm = value * conversion[from_unit]
            result = value_in_sqm / conversion[to_unit]

            return f"Converted Value: {result:.4f} {to_unit}"


        
        elif calc_id == "next_birthday":
            dob_str = data.get("dob")
            if not dob_str:
                return "Error: Please provide a date of birth"
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
            today = datetime.today()
            next_bday = dob.replace(year=today.year)
            if next_bday < today:
                next_bday = dob.replace(year=today.year + 1)
            days = (next_bday - today).days
            return f"Days Until Next Birthday: {days} days"
        
        elif calc_id == "work_days":
            date1_str = data.get("date1")
            date2_str = data.get("date2")
            if not date1_str or not date2_str:
                return "Error: Please provide both dates"
            date1 = datetime.strptime(date1_str, "%Y-%m-%d")
            date2 = datetime.strptime(date2_str, "%Y-%m-%d")
            workdays = 0
            current = date1
            while current <= date2:
                if current.weekday() < 5:
                    workdays += 1
                current += timedelta(days=1)
            return f"Work Days: {workdays} days"
        
        elif calc_id == "time_zone":
            time_str = data.get("time")
            if not time_str:
                return "Error: Please provide a time"
            from_offset = float(data.get("from_offset", 0))
            to_offset = float(data.get("to_offset", 0))
            time_obj = datetime.strptime(time_str, "%H:%M")
            diff = to_offset - from_offset
            new_time = time_obj + timedelta(hours=diff)
            return f"Converted Time: {new_time.strftime('%H:%M')}"
        
        # Health Calculators
        elif calc_id == "bmi":
            weight, error = get_float_value(data, "weight")
            if error: return error
            height, error = get_float_value(data, "height")
            if error: return error
            if height <= 0 or weight <= 0:
                return "Error: Weight and height must be positive numbers"
            height = height / 100
            bmi = weight / (height ** 2)
            category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
            return f"BMI: {bmi:.2f} ({category})"
        
        elif calc_id == "bmr":
            weight, error = get_float_value(data, "weight")
            if error: return error
            height, error = get_float_value(data, "height")
            if error: return error
            age, error = get_float_value(data, "age")
            if error: return error
            if weight <= 0 or height <= 0 or age <= 0:
                return "Error: Weight, height, and age must be positive"
            gender = data.get("gender")
            if gender == "male":
                bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
            else:
                bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
            return f"BMR: {bmr:.2f} calories/day"
        
        elif calc_id == "body_fat":
            height = float(data.get("height"))
            weight = float(data.get("weight"))
            waist = float(data.get("waist", 0))
            gender = data.get("gender", "male")
            if waist > 0:
                if gender == "male":
                    bf = 64 - (20 * (height / waist))
                else:
                    bf = 76 - (20 * (height / waist))
                return f"Estimated Body Fat: {bf:.1f}%"
            return "Please provide waist measurement"
        
        elif calc_id == "ideal_weight":
            height = float(data.get("height"))
            gender = data.get("gender", "male")
            if gender == "male":
                ideal = 50 + 2.3 * ((height / 2.54) - 60)
            else:
                ideal = 45.5 + 2.3 * ((height / 2.54) - 60)
            return f"Ideal Weight: {max(30, ideal):.1f} kg ({max(30, ideal) * 2.20462:.1f} lbs)"
        
        elif calc_id == "calories_burned":
            weight = float(data.get("weight"))
            duration = float(data.get("duration"))
            activity = data.get("activity", "moderate")
            mets = {"light": 3, "moderate": 5, "vigorous": 8}.get(activity, 5)
            calories = mets * weight * (duration / 60)
            return f"Calories Burned: {calories:.0f}"
        
        elif calc_id == "water_intake":
            weight = float(data.get("weight"))
            activity = float(data.get("activity", 0))
            base = weight * 0.033
            additional = activity * 0.5
            total = base + additional
            return f"Daily Water Intake: {total:.1f} liters ({total * 33.814:.1f} oz)"
        
        elif calc_id == "heart_rate":
            age = float(data.get("age"))
            max_hr = 220 - age
            target_min = max_hr * 0.5
            target_max = max_hr * 0.85
            return f"Max HR: {max_hr:.0f} bpm, Target Zone: {target_min:.0f}-{target_max:.0f} bpm"
        
        elif calc_id == "protein_needs":
            weight = float(data.get("weight"))
            activity = data.get("activity", "moderate")
            multipliers = {"sedentary": 0.8, "moderate": 1.2, "active": 1.6, "athlete": 2.0}
            protein = weight * multipliers.get(activity, 1.2)
            return f"Daily Protein Needs: {protein:.1f}g"
        
        elif calc_id == "carbs_needs":
            weight = float(data.get("weight"))
            activity = data.get("activity", "moderate")
            multipliers = {"sedentary": 3, "moderate": 5, "active": 7, "athlete": 10}
            carbs = weight * multipliers.get(activity, 5)
            return f"Daily Carbs Needs: {carbs:.1f}g"
        
        elif calc_id == "fiber_needs":
            age = int(float(data.get("age")))
            gender = data.get("gender", "male")
            if gender == "male":
                fiber = 38 if age < 50 else 30
            else:
                fiber = 25 if age < 50 else 21
            return f"Daily Fiber Needs: {fiber}g"
        
        elif calc_id == "sleep_hours":
            bedtime = data.get("bedtime")
            waketime = data.get("waketime")
            if not bedtime or not waketime:
                return "Error: Please provide both bedtime and wake time"
            bed = datetime.strptime(bedtime, "%H:%M")
            wake = datetime.strptime(waketime, "%H:%M")
            if wake < bed:
                wake += timedelta(days=1)
            hours = (wake - bed).seconds / 3600
            cycles = hours / 1.5
            return f"Sleep Duration: {hours:.1f} hours ({cycles:.1f} sleep cycles)"
        
        
        elif calc_id == "alcohol_units":
            volume = float(data.get("volume"))
            abv = float(data.get("abv"))
            units = (volume * abv) / 1000
            return f"Alcohol Units: {units:.2f} units"
        
        # Finance Calculators
        elif calc_id == "simple_interest":
            principal, error = get_float_value(data, "principal")
            if error: return error
            rate, error = get_float_value(data, "rate")
            if error: return error
            time, error = get_float_value(data, "time")
            if error: return error
            if principal <= 0 or rate < 0 or time <= 0:
                return "Error: Principal and time must be positive, rate cannot be negative"
            interest = (principal * rate * time) / 100
            return f"Interest: ${interest:,.2f}, Total: ${principal + interest:,.2f}"
        
        elif calc_id == "compound_interest":
            principal, error = get_float_value(data, "principal")
            if error: return error
            rate, error = get_float_value(data, "rate")
            if error: return error
            time, error = get_float_value(data, "time")
            if error: return error
            n, error = get_float_value(data, "compounds", 12, False)
            if error: return error
            if principal <= 0 or rate < 0 or time <= 0 or n <= 0:
                return "Error: All values must be positive"
            rate = rate / 100
            amount = principal * (1 + rate/n) ** (n * time)
            return f"Amount: ${amount:,.2f}, Interest: ${amount - principal:,.2f}"
        
        elif calc_id == "loan_payment":
            principal, error = get_float_value(data, "principal")
            if error: return error
            rate, error = get_float_value(data, "rate")
            if error: return error
            months, error = get_float_value(data, "months")
            if error: return error
            if principal <= 0 or rate < 0 or months <= 0:
                return "Error: Principal and months must be positive, rate cannot be negative"
            rate = rate / 100 / 12
            if rate == 0:
                payment = principal / months
            else:
                payment = principal * (rate * (1 + rate)**months) / ((1 + rate)**months - 1)
            return f"Monthly Payment: ${payment:,.2f}"
        
        elif calc_id == "mortgage":
            price, error = get_float_value(data, "price")
            if error: return error
            down, error = get_float_value(data, "down")
            if error: return error
            rate, error = get_float_value(data, "rate")
            if error: return error
            years, error = get_float_value(data, "years")
            if error: return error
            if price <= 0 or down < 0 or rate < 0 or years <= 0:
                return "Error: All values must be positive"
            loan_amount = price - down
            monthly_rate = rate / 100 / 12
            months = years * 12
            if monthly_rate == 0:
                payment = loan_amount / months
            else:
                payment = loan_amount * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
            return f"Monthly Payment: ${payment:,.2f}, Loan Amount: ${loan_amount:,.2f}"
        
        elif calc_id == "discount":
            price, error = get_float_value(data, "price")
            if error: return error
            discount, error = get_float_value(data, "discount (%)")
            if error: return error
            if price <= 0:
                return "Error: Original price must be positive"
            if discount < 0 or discount > 100:
                return "Error: Discount must be between 0 and 100 percent"
            final = price * (1 - discount / 100)
            saved = price - final
            return f"Final Price: ${final:.2f}, Saved: ${saved:.2f}"
        
        elif calc_id == "tip_calculator":
            bill, error = get_float_value(data, "bill")
            if error: return error
            tip_percent, error = get_float_value(data, "tip")
            if error: return error
            if bill <= 0:
                return "Error: Bill amount must be positive"
            tip = bill * (tip_percent / 100)
            total = bill + tip
            return f"Tip: ${tip:.2f}, Total: ${total:.2f}"
        
        elif calc_id == "investment_return":
            initial, error = get_float_value(data, "initial")
            if error: return error
            rate, error = get_float_value(data, "rate")
            if error: return error
            years, error = get_float_value(data, "years")
            if error: return error
            amount = initial * (1 + rate/100) ** years
            return f"Future Value: ${amount:,.2f}, Return: ${amount - initial:,.2f}"
        
        elif calc_id == "savings_goal":
            goal, error = get_float_value(data, "goal")
            if error: return error
            rate, error = get_float_value(data, "rate", 0, False)
            if error: return error
            months, error = get_float_value(data, "months")
            if error: return error
            rate = rate / 100 / 12
            if rate > 0:
                payment = goal * rate / ((1 + rate)**months - 1)
            else:
                payment = goal / months
            return f"Monthly Savings Needed: ${payment:,.2f}"
        
        elif calc_id == "retirement":
            age, error = get_float_value(data, "age")
            if error: return error
            retire_age, error = get_float_value(data, "retire_age")
            if error: return error
            monthly, error = get_float_value(data, "monthly")
            if error: return error
            annual_return, error = get_float_value(data, "return")
            if error: return error
            if age >= retire_age:
                return "Error: Retirement age must be greater than current age"
            years = retire_age - age
            monthly_rate = annual_return / 100 / 12
            months = years * 12
            if monthly_rate == 0:
                total = monthly * months
            else:
                total = monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
            return f"Retirement Savings: ${total:,.2f} after {years} years"
        
        elif calc_id == "currency_converter":
            amount = float(data.get("amount"))
            from_curr = float(data.get("from_rate", 1))
            to_curr = float(data.get("to_rate", 1))
            result = (amount / from_curr) * to_curr
            return f"Converted Amount: {result:,.2f}"
        
        # Math Calculators
        elif calc_id == "percentage":
            value, error = get_float_value(data, "value")
            if error: return error
            percent, error = get_float_value(data, "percent")
            if error: return error
            result = (value * percent) / 100
            return f"{percent}% of {value} = {result}"
        
        elif calc_id == "percentage_change":
            old_val = float(data.get("old"))
            new_val = float(data.get("new"))
            change = ((new_val - old_val) / old_val) * 100
            return f"Percentage Change: {change:.2f}%"
        
        elif calc_id == "percentage_of":
            value = float(data.get("value"))
            percent = float(data.get("percent"))
            result = (value * percent) / 100
            return f"{percent}% of {value} = {result:.2f}"
        
        elif calc_id == "area_circle":
            radius, error = get_float_value(data, "radius")
            if error: return error
            if radius <= 0:
                return "Error: Radius must be positive"
            area = math.pi * radius ** 2
            return f"Area: {area:.2f} square units"
        
        elif calc_id == "area_rectangle":
            length, error = get_float_value(data, "length")
            if error: return error
            width, error = get_float_value(data, "width")
            if error: return error
            if length <= 0 or width <= 0:
                return "Error: Length and width must be positive"
            area = length * width
            return f"Area: {area:.2f} square units"
        
        elif calc_id == "area_triangle":
            base, error = get_float_value(data, "base")
            if error: return error
            height, error = get_float_value(data, "height")
            if error: return error
            if base <= 0 or height <= 0:
                return "Error: Base and height must be positive"
            area = 0.5 * base * height
            return f"Area: {area:.2f} square units"
        
        elif calc_id == "area_trapezoid":
            base1 = float(data.get("base1"))
            base2 = float(data.get("base2"))
            height = float(data.get("height"))
            area = 0.5 * (base1 + base2) * height
            return f"Area: {area:.2f} square units"
        
        elif calc_id == "volume_sphere":
            radius, error = get_float_value(data, "radius")
            if error: return error
            if radius <= 0:
                return "Error: Radius must be positive"
            volume = (4/3) * math.pi * radius ** 3
            return f"Volume: {volume:.2f} cubic units"
        
        elif calc_id == "volume_cube":
            side = float(data.get("side"))
            volume = side ** 3
            return f"Volume: {volume:.2f} cubic units"
        
        elif calc_id == "volume_cylinder":
            radius = float(data.get("radius"))
            height = float(data.get("height"))
            volume = math.pi * radius ** 2 * height
            return f"Volume: {volume:.2f} cubic units"
        
        elif calc_id == "pythagorean":
            a_str = data.get("a")
            b_str = data.get("b")
            c_str = data.get("c")
            provided = sum(1 for x in [a_str, b_str, c_str] if x and x.strip())
            if provided != 2:
                return "Error: Please provide exactly 2 values to calculate the third"
            try:
                if not c_str or not c_str.strip():
                    a, b = float(a_str), float(b_str)
                    if a <= 0 or b <= 0:
                        return "Error: All sides must be positive"
                    c = math.sqrt(a**2 + b**2)
                    return f"Hypotenuse (c): {c:.2f}"
                elif not a_str or not a_str.strip():
                    b, c = float(b_str), float(c_str)
                    if b <= 0 or c <= 0 or c <= b:
                        return "Error: All sides must be positive and hypotenuse must be largest"
                    a = math.sqrt(c**2 - b**2)
                    return f"Side (a): {a:.2f}"
                else:
                    a, c = float(a_str), float(c_str)
                    if a <= 0 or c <= 0 or c <= a:
                        return "Error: All sides must be positive and hypotenuse must be largest"
                    b = math.sqrt(c**2 - a**2)
                    return f"Side (b): {b:.2f}"
            except ValueError:
                return "Error: Please provide valid numbers"
        
        elif calc_id == "distance":
            x1 = float(data.get("x1"))
            y1 = float(data.get("y1"))
            x2 = float(data.get("x2"))
            y2 = float(data.get("y2"))
            dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            return f"Distance: {dist:.2f} units"
        
        elif calc_id == "slope":
            x1 = float(data.get("x1"))
            y1 = float(data.get("y1"))
            x2 = float(data.get("x2"))
            y2 = float(data.get("y2"))
            slope = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else "undefined"
            return f"Slope: {slope}"
        
        elif calc_id == "factorial":
            n_val, error = get_float_value(data, "n")
            if error: return error
            n = int(n_val)
            if n < 0:
                return "Error: Factorial not defined for negative numbers"
            if n > 170:
                return "Error: Number too large for factorial calculation"
            result = math.factorial(n)
            return f"{n}! = {result:,}"
        
        elif calc_id == "gcd":
            a_val, error = get_float_value(data, "a")
            if error: return error
            b_val, error = get_float_value(data, "b")
            if error: return error
            a, b = int(a_val), int(b_val)
            if a == 0 and b == 0:
                return "Error: GCD is undefined when both numbers are zero"
            result = math.gcd(a, b)
            return f"GCD({a}, {b}) = {result}"
        
        elif calc_id == "lcm":
            a_val, error = get_float_value(data, "a")
            if error: return error
            b_val, error = get_float_value(data, "b")
            if error: return error
            a, b = int(a_val), int(b_val)
            if a == 0 or b == 0:
                return "Error: LCM is undefined when either number is zero"
            result = abs(a * b) // math.gcd(a, b)
            return f"LCM({a}, {b}) = {result}"
        
        elif calc_id == "quadratic":
            a = float(data.get("a"))
            b = float(data.get("b"))
            c = float(data.get("c"))
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return "No real solutions"
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return f"Solutions: x1 = {x1:.2f}, x2 = {x2:.2f}"
        
        elif calc_id == "permutation":
            n = int(float(data.get("n")))
            r = int(float(data.get("r")))
            result = math.factorial(n) // math.factorial(n - r)
            return f"P({n},{r}) = {result:,}"
        
        elif calc_id == "combination":
            n = int(float(data.get("n")))
            r = int(float(data.get("r")))
            result = math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
            return f"C({n},{r}) = {result:,}"
        
        elif calc_id == "binary":
            num = int(float(data.get("number")))
            return f"Binary: {bin(num)[2:]}"
        
        elif calc_id == "hex":
            num = int(float(data.get("number")))
            return f"Hexadecimal: {hex(num)[2:].upper()}"
        
        elif calc_id == "octal":
            num = int(float(data.get("number")))
            return f"Octal: {oct(num)[2:]}"
        
        elif calc_id == "prime_check":
            num = int(float(data.get("number")))
            if num < 2:
                return f"{num} is not prime"
            for i in range(2, int(math.sqrt(num)) + 1):
                if num % i == 0:
                    return f"{num} is not prime"
            return f"{num} is prime"
        
        elif calc_id == "fibonacci":
            n = int(float(data.get("n")))
            if n <= 0:
                return "Please enter a positive number"
            fib = [0, 1]
            for i in range(2, n):
                fib.append(fib[i-1] + fib[i-2])
            return f"Fibonacci Sequence: {', '.join(map(str, fib[:n]))}"
        
        elif calc_id == "random_number":
            min_val = int(float(data.get("min", 1)))
            max_val = int(float(data.get("max", 100)))
            result = random.randint(min_val, max_val)
            return f"Random Number: {result}"
        
        elif calc_id == "roman_numeral":
            number = int(float(data.get("number")))
            if number <= 0 or number > 3999:
                return "Number must be between 1 and 3999"
            values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
            numerals = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
            result = ""
            for i in range(len(values)):
                count = number // values[i]
                result += numerals[i] * count
                number -= values[i] * count
            return f"Roman Numeral: {result}"
        
        # Statistics Calculators
        elif calc_id == "mean":
            numbers = [float(x.strip()) for x in data.get("numbers", "").split(",")]
            mean = sum(numbers) / len(numbers) if numbers else 0
            return f"Mean: {mean:.2f}"
        
        elif calc_id == "median":
            numbers = sorted([float(x.strip()) for x in data.get("numbers", "").split(",")])
            n = len(numbers)
            if n == 0:
                return "No numbers provided"
            if n % 2 == 0:
                median = (numbers[n//2 - 1] + numbers[n//2]) / 2
            else:
                median = numbers[n//2]
            return f"Median: {median:.2f}"
        
        elif calc_id == "mode":
            numbers = [float(x.strip()) for x in data.get("numbers", "").split(",")]
            counter = Counter(numbers)
            max_count = max(counter.values())
            modes = [k for k, v in counter.items() if v == max_count]
            return f"Mode: {modes}"
        
        elif calc_id == "standard_deviation":
            numbers = [float(x.strip()) for x in data.get("numbers", "").split(",")]
            mean = sum(numbers) / len(numbers)
            variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
            std_dev = math.sqrt(variance)
            return f"Standard Deviation: {std_dev:.2f}"
        
        elif calc_id == "variance":
            numbers = [float(x.strip()) for x in data.get("numbers", "").split(",")]
            mean = sum(numbers) / len(numbers)
            variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
            return f"Variance: {variance:.2f}"
        
        elif calc_id == "correlation":
            x_values = [float(x.strip()) for x in data.get("x_values", "").split(",")]
            y_values = [float(y.strip()) for y in data.get("y_values", "").split(",")]
            if len(x_values) != len(y_values):
                return "Error: X and Y must have same number of values"
            n = len(x_values)
            mean_x = sum(x_values) / n
            mean_y = sum(y_values) / n
            numerator = sum((x_values[i] - mean_x) * (y_values[i] - mean_y) for i in range(n))
            denom_x = sum((x - mean_x) ** 2 for x in x_values) ** 0.5
            denom_y = sum((y - mean_y) ** 2 for y in y_values) ** 0.5
            correlation = numerator / (denom_x * denom_y) if denom_x * denom_y != 0 else 0
            return f"Correlation Coefficient: {correlation:.4f}"
        
        # Physics Calculators
        elif calc_id == "speed":
            distance, error = get_float_value(data, "distance")
            if error: return error
            time, error = get_float_value(data, "time")
            if error: return error
            if distance <= 0 or time <= 0:
                return "Error: Distance and time must be positive"
            speed = distance / time
            return f"Speed: {speed:.2f} units/time"
        
        elif calc_id == "force":
            mass, error = get_float_value(data, "mass")
            if error: return error
            acceleration, error = get_float_value(data, "acceleration")
            if error: return error
            if mass <= 0:
                return "Error: Mass must be positive"
            force = mass * acceleration
            return f"Force: {force:.2f} N"
        
        elif calc_id == "kinetic_energy":
            mass, error = get_float_value(data, "mass")
            if error: return error
            velocity, error = get_float_value(data, "velocity")
            if error: return error
            if mass <= 0:
                return "Error: Mass must be positive"
            ke = 0.5 * mass * velocity ** 2
            return f"Kinetic Energy: {ke:.2f} J"
        
        elif calc_id == "potential_energy":
            mass = float(data.get("mass"))
            height = float(data.get("height"))
            g = 9.81
            pe = mass * g * height
            return f"Potential Energy: {pe:.2f} J"
        
        elif calc_id == "power_physics":
            work = float(data.get("work", 0))
            time = float(data.get("time", 0))
            if work > 0 and time > 0:
                power = work / time
                return f"Power: {power:.2f} W"
            return "Please provide work & time"
        
        elif calc_id == "density":
            mass = float(data.get("mass"))
            volume = float(data.get("volume"))
            density = mass / volume
            return f"Density: {density:.2f} kg/m³"
        
        elif calc_id == "pressure_physics":
            force = float(data.get("force"))
            area = float(data.get("area"))
            pressure = force / area
            return f"Pressure: {pressure:.2f} Pa"
        
        elif calc_id == "work":
            force = float(data.get("force"))
            distance = float(data.get("distance"))
            work = force * distance
            return f"Work: {work:.2f} J"
        
        elif calc_id == "momentum":
            mass = float(data.get("mass"))
            velocity = float(data.get("velocity"))
            momentum = mass * velocity
            return f"Momentum: {momentum:.2f} kg·m/s"
        
        elif calc_id == "acceleration":
            initial_velocity = float(data.get("initial_velocity", 0))
            final_velocity = float(data.get("final_velocity"))
            time = float(data.get("time"))
            acceleration = (final_velocity - initial_velocity) / time
            return f"Acceleration: {acceleration:.2f} m/s²"
        
        # Education Calculators
        elif calc_id == "gpa":
            points, error = get_float_value(data, "points")
            if error: return error
            credits, error = get_float_value(data, "credits")
            if error: return error
            if credits <= 0:
                return "Error: Credit hours must be positive"
            gpa = points / credits
            return f"GPA: {gpa:.2f}"
        
        elif calc_id == "cgpa":
            grades_str = data.get("grades", "")
            if not grades_str.strip():
                return "Error: Please provide GPAs separated by commas"
            try:
                grades = [float(g.strip()) for g in grades_str.split(",") if g.strip()]
                if not grades:
                    return "Error: Please provide at least one GPA"
                for gpa in grades:
                    if gpa < 0.0 or gpa > 4.0:
                        return f"Error: GPA {gpa} is out of range (0.0 - 4.0)"
                cgpa = sum(grades) / len(grades)
                return f"CGPA: {cgpa:.2f} (based on {len(grades)} courses)"
            except ValueError:
                return "Error: Please enter valid numbers separated by commas"
        
        elif calc_id == "grade":
            score = float(data.get("score"))
            total = float(data.get("total"))
            percentage = (score / total) * 100
            letter = "A" if percentage >= 90 else "B" if percentage >= 80 else "C" if percentage >= 70 else "D" if percentage >= 60 else "F"
            return f"Grade: {percentage:.1f}% ({letter})"
        
        elif calc_id == "test_score":
            correct = float(data.get("correct"))
            total = float(data.get("total"))
            percentage = (correct / total) * 100
            return f"Test Score: {percentage:.2f}%"
        
        elif calc_id == "final_grade":
            current_grade = float(data.get("current_grade"))
            desired_grade = float(data.get("desired_grade"))
            final_weight = float(data.get("final_weight")) / 100
            needed = (desired_grade - current_grade * (1 - final_weight)) / final_weight
            return f"Grade Needed on Final: {needed:.2f}%"
        
        # Home Calculators
        elif calc_id == "paint_needed":
            length = float(data.get("length"))
            width = float(data.get("width"))
            height = float(data.get("height", 0))
            coats = float(data.get("coats", 1))
            if height > 0:
                area = 2 * (length * width + length * height + width * height)
            else:
                area = length * width
            coverage = float(data.get("coverage", 350))
            gallons = (area * coats) / coverage
            return f"Paint Needed: {gallons:.2f} gallons"
        
        elif calc_id == "flooring":
            length = float(data.get("length"))
            width = float(data.get("width"))
            area = length * width
            waste = float(data.get("waste", 10)) / 100
            total = area * (1 + waste)
            return f"Flooring Needed: {total:.2f} sq units (including {waste*100:.0f}% waste)"
        
        elif calc_id == "tile_needed":
            length = float(data.get("length"))
            width = float(data.get("width"))
            tile_size = float(data.get("tile_size"))
            area = length * width
            tiles = math.ceil(area / (tile_size ** 2))
            return f"Tiles Needed: {tiles} ({tiles * tile_size ** 2:.2f} sq units)"
        
        elif calc_id == "concrete":
            length = float(data.get("length"))
            width = float(data.get("width"))
            depth = float(data.get("depth"))
            volume = length * width * depth
            cubic_yards = volume / 27
            return f"Concrete Needed: {cubic_yards:.2f} cubic yards"
        
        elif calc_id == "fence":
            length = float(data.get("length"))
            width = float(data.get("width"))
            perimeter = 2 * (length + width)
            return f"Fence Length Needed: {perimeter:.2f} ft"
        
        elif calc_id == "roofing":
            length = float(data.get("length"))
            width = float(data.get("width"))
            pitch = float(data.get("pitch", 0))
            area = length * width
            if pitch > 0:
                area *= (1 + (pitch / 12) ** 2) ** 0.5
            squares = area / 100
            return f"Roofing Needed: {squares:.2f} squares ({area:.2f} sq ft)"
        
        elif calc_id == "electricity_cost":
            watts = float(data.get("watts"))
            hours = float(data.get("hours"))
            rate = float(data.get("rate"))
            kwh = (watts * hours) / 1000
            cost = kwh * rate
            return f"Electricity Cost: ${cost:.2f} ({kwh:.2f} kWh)"
        
        elif calc_id == "solar_panels":
            monthly_bill = float(data.get("monthly_bill"))
            rate = float(data.get("rate", 0.12))
            kwh_per_month = monthly_bill / rate
            kwh_per_day = kwh_per_month / 30
            panels = kwh_per_day / 1.5
            return f"Solar Panels Needed: {math.ceil(panels)} panels (250W each)"
        
        # Automotive Calculators
        elif calc_id == "car_loan":
            principal = float(data.get("principal"))
            rate = float(data.get("rate")) / 100 / 12
            months = float(data.get("months"))
            payment = principal * (rate * (1 + rate)**months) / ((1 + rate)**months - 1)
            return f"Monthly Car Payment: ${payment:,.2f}"
        
        elif calc_id == "fuel_cost":
            distance = float(data.get("distance"))
            mpg = float(data.get("mpg"))
            price_per_gallon = float(data.get("price"))
            gallons = distance / mpg
            cost = gallons * price_per_gallon
            return f"Fuel Cost: ${cost:.2f} ({gallons:.2f} gallons)"
        
        elif calc_id == "fuel_efficiency":
            distance, error = get_float_value(data, "distance")
            if error: return error
            fuel, error = get_float_value(data, "fuel")
            if error: return error
            if distance <= 0 or fuel <= 0:
                return "Error: Distance and fuel must be positive"
            mpg = distance / fuel
            kpl = mpg * 0.425144
            return f"MPG: {mpg:.2f}, KPL: {kpl:.2f}"
        
        elif calc_id == "tire_size":
            width = float(data.get("width"))
            aspect = float(data.get("aspect"))
            diameter = float(data.get("diameter"))
            sidewall = width * aspect / 100
            total_diameter = (diameter * 25.4) + (2 * sidewall)
            circumference = total_diameter * 3.14159
            return f"Tire Diameter: {total_diameter:.2f}mm, Circumference: {circumference:.2f}mm"
        
        elif calc_id == "lease_vs_buy":
            lease_payment = float(data.get("lease_payment"))
            lease_months = float(data.get("lease_months"))
            loan_payment = float(data.get("loan_payment"))
            loan_months = float(data.get("loan_months"))
            lease_total = lease_payment * lease_months
            loan_total = loan_payment * loan_months
            savings = abs(lease_total - loan_total)
            better = "Leasing" if lease_total < loan_total else "Buying"
            return f"{better} is better. Lease: ${lease_total:,.2f}, Buy: ${loan_total:,.2f}, Savings: ${savings:,.2f}"
        
        # Cooking Calculators
        elif calc_id == "recipe_scaler":
            original_servings = float(data.get("original_servings"))
            desired_servings = float(data.get("desired_servings"))
            multiplier = desired_servings / original_servings
            return f"Recipe Multiplier: {multiplier:.2f}x (multiply all ingredients by this)"
        
        elif calc_id == "oven_temp":
            temp = float(data.get("temp"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            if from_unit == "fahrenheit" and to_unit == "celsius":
                result = (temp - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "fahrenheit":
                result = (temp * 9/5) + 32
            else:
                result = temp
            return f"{temp}° {from_unit} = {result:.0f}° {to_unit}"
        
        elif calc_id == "cooking_time":
            weight = float(data.get("weight"))
            time_per_unit = float(data.get("time_per_unit", 20))
            total_time = weight * time_per_unit
            return f"Cooking Time: {total_time:.0f} minutes"
        
        # Environment Calculators
        elif calc_id == "carbon_footprint":
            electricity = float(data.get("electricity", 0))
            gas = float(data.get("gas", 0))
            car_miles = float(data.get("car_miles", 0))
            flights = float(data.get("flights", 0))
            total = (electricity * 0.92) + (gas * 5.3) + (car_miles * 0.404) + (flights * 90)
            return f"Annual Carbon Footprint: {total:.2f} kg CO2"
        
        elif calc_id == "tree_offset":
            co2 = float(data.get("co2"))
            trees = co2 / 21.77
            return f"Trees Needed: {math.ceil(trees)} trees to offset {co2:.2f} kg CO2/year"
        
        elif calc_id == "recycling":
            paper = float(data.get("paper", 0))
            plastic = float(data.get("plastic", 0))
            glass = float(data.get("glass", 0))
            metal = float(data.get("metal", 0))
            co2_saved = (paper * 3.3) + (plastic * 1.5) + (glass * 0.3) + (metal * 1.5)
            return f"CO2 Saved by Recycling: {co2_saved:.2f} kg CO2/year"
        
        # Unit Conversion Calculators
        elif calc_id == "unit_temperature":
            temp, error = get_float_value(data, "temp")
            if error: return error
            from_unit = data.get("from")
            to_unit = data.get("to")
            if not from_unit or not to_unit:
                return "Error: Please select both temperature units"
            if from_unit == "celsius" and to_unit == "fahrenheit":
                result = (temp * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                result = (temp - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                result = temp + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                result = temp - 273.15
            else:
                result = temp
            return f"{temp}° {from_unit} = {result:.2f}° {to_unit}"
        
        elif calc_id == "unit_length":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"meters": 1, "kilometers": 1000, "centimeters": 0.01,
                          "millimeters": 0.001, "miles": 1609.34, "yards": 0.9144,
                          "feet": 0.3048, "inches": 0.0254}
            meters = value * conversions.get(from_unit, 1)
            result = meters / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_weight":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"kilograms": 1, "grams": 0.001, "milligrams": 0.000001,
                          "pounds": 0.453592, "ounces": 0.0283495, "tons": 1000}
            kg = value * conversions.get(from_unit, 1)
            result = kg / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_volume":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"liters": 1, "milliliters": 0.001, "gallons": 3.78541,
                          "quarts": 0.946353, "pints": 0.473176, "cups": 0.236588,
                          "fluid_ounces": 0.0295735, "cubic_meters": 1000}
            liters = value * conversions.get(from_unit, 1)
            result = liters / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        
        elif calc_id == "unit_speed":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"meters_per_second": 1, "kilometers_per_hour": 0.277778,
                          "miles_per_hour": 0.44704, "feet_per_second": 0.3048,
                          "knots": 0.514444}
            mps = value * conversions.get(from_unit, 1)
            result = mps / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_time":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"seconds": 1, "minutes": 60, "hours": 3600,
                          "days": 86400, "weeks": 604800, "years": 31536000}
            seconds = value * conversions.get(from_unit, 1)
            result = seconds / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_energy":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"joules": 1, "kilojoules": 1000, "calories": 4.184,
                          "kilocalories": 4184, "watt_hours": 3600, "kilowatt_hours": 3600000}
            joules = value * conversions.get(from_unit, 1)
            result = joules / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_power":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"watts": 1, "kilowatts": 1000, "horsepower": 745.7,
                          "btu_per_hour": 0.293071}
            watts = value * conversions.get(from_unit, 1)
            result = watts / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_pressure":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {"pascals": 1, "kilopascals": 1000, "bar": 100000,
                          "psi": 6894.76, "atmospheres": 101325}
            pascals = value * conversions.get(from_unit, 1)
            result = pascals / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        else:
            return "Calculator not yet implemented"
    
    except ValueError as e:
        return f"Error: Invalid input - please check your numbers"
    except ZeroDivisionError:
        return f"Error: Division by zero - please check your inputs"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html", calculators=CALCULATORS)

@app.route("/calculate", methods=["POST"])
def calculate_route():
    data = request.json
    calc_id = data.get("calc_id")
    result = calculate(calc_id, data.get("data", {}))
    return jsonify({"result": result})

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy.html")

@app.route("/terms-and-conditions")
def terms():
    return render_template("terms.html")

if __name__ == "__main__":
    app.run(debug = True)
