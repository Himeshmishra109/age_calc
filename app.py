from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'calcmaster'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def get_db_connection():
    """Get database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def init_database():
    """Initialize database tables"""
    try:
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        # Create feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                subject VARCHAR(500) NOT NULL,
                message TEXT NOT NULL,
                rating INT,
                feedback_type VARCHAR(100),
                wants_updates BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create contact table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contact (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                subject VARCHAR(500) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        connection.commit()
        cursor.close()
        connection.close()
        print("Database tables initialized successfully")
        return True
        
    except mysql.connector.Error as e:
        print(f"Database initialization error: {e}")
        return False

# Initialize database on startup (if available)
try:
    init_database()
except Exception as e:
    print(f"Database initialization failed: {e}")
    print("Running in fallback mode - feedback will be logged to console")

# Define all 100 calculators with their metadata
CALCULATORS = [
    {'id': 'acceleration', 'name': 'Acceleration', 'category': 'Physics', 'description': 'Calculate acceleration'},
    {'id': 'date_add', 'name': 'Add Days to Date', 'category': 'Date & Time', 'description': 'Add days to a date'},
    {'id': 'age', 'name': 'Age Calculator', 'category': 'Date & Time', 'description': 'Calculate your exact age'},
    {'id': 'age_difference', 'name': 'Age Difference', 'category': 'Date & Time', 'description': 'Calculate age difference'},
    {'id': 'alcohol_units', 'name': 'Alcohol Units', 'category': 'Health', 'description': 'Calculate alcohol units'},
    {'id': 'unit_area', 'name': 'Area Converter', 'category': 'Unit Conversion', 'description': 'Convert area units'},
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
    {'id': 'ovulation', 'name': 'Ovulation Calculator', 'category': 'Health', 'description': 'Calculate ovulation date'},
    {'id': 'paint_needed', 'name': 'Paint Needed', 'category': 'Home', 'description': 'Calculate paint needed'},
    {'id': 'percentage', 'name': 'Percentage Calculator', 'category': 'Math', 'description': 'Calculate percentages'},
    {'id': 'percentage_change', 'name': 'Percentage Change', 'category': 'Math', 'description': 'Calculate percentage change'},
    {'id': 'percentage_of', 'name': 'Percentage Of', 'category': 'Math', 'description': 'Find percentage of a number'},
    {'id': 'permutation', 'name': 'Permutation', 'category': 'Math', 'description': 'Calculate permutations'},
    {'id': 'potential_energy', 'name': 'Potential Energy', 'category': 'Physics', 'description': 'Calculate potential energy'},
    {'id': 'power_physics', 'name': 'Power (Physics)', 'category': 'Physics', 'description': 'Calculate power'},
    {'id': 'unit_power', 'name': 'Power Converter', 'category': 'Unit Conversion', 'description': 'Convert power units'},
    {'id': 'pregnancy_due', 'name': 'Pregnancy Due Date', 'category': 'Health', 'description': 'Calculate due date'},
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
        
        elif calc_id == "bmi":
            weight, error = get_float_value(data, "weight")
            if error: return error
            height, error = get_float_value(data, "height")
            if error: return error
            if height <= 0 or weight <= 0:
                return "Error: Weight and height must be positive numbers"
            height = height / 100  # convert cm to meters
            bmi = weight / (height ** 2)
            category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
            return f"BMI: {bmi:.2f} ({category})"
        
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
        
        elif calc_id == "percentage":
            value, error = get_float_value(data, "value")
            if error: return error
            percent, error = get_float_value(data, "percent")
            if error: return error
            result = (value * percent) / 100
            return f"{percent}% of {value} = {result}"
        
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
        
        elif calc_id == "volume_sphere":
            radius, error = get_float_value(data, "radius")
            if error: return error
            if radius <= 0:
                return "Error: Radius must be positive"
            volume = (4/3) * math.pi * radius ** 3
            return f"Volume: {volume:.2f} cubic units"
        
        elif calc_id == "pythagorean":
            a_str = data.get("a")
            b_str = data.get("b")
            c_str = data.get("c")
            
            # Count how many values are provided
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
        
        elif calc_id == "discount":
            price, error = get_float_value(data, "price")
            if error: return error
            discount, error = get_float_value(data, "discount")
            if error: return error
            if price <= 0:
                return "Error: Original price must be positive"
            if discount < 0 or discount > 100:
                return "Error: Discount must be between 0 and 100 percent"
            final = price * (1 - discount / 100)
            saved = price - final
            return f"Final Price: ${final:.2f}, Saved: ${saved:.2f}"
        
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
        
        elif calc_id == "gpa":
            points, error = get_float_value(data, "points")
            if error: return error
            credits, error = get_float_value(data, "credits")
            if error: return error
            if credits <= 0:
                return "Error: Credit hours must be positive"
            gpa = points / credits
            return f"GPA: {gpa:.2f}"
        
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
        
        elif calc_id == "mean":
            numbers = [float(x.strip()) for x in data.get("numbers", "").split(",")]
            mean = sum(numbers) / len(numbers) if numbers else 0
            return f"Mean: {mean:.2f}"
        
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
        
        elif calc_id == "body_fat":
            weight = float(data.get("weight"))
            waist = float(data.get("waist", 0))
            gender = data.get("gender", "male")
            if waist > 0:
                if gender == "male":
                    bf = 64 - (20 * (height / waist)) if "height" in data else 0
                else:
                    bf = 76 - (20 * (height / waist)) if "height" in data else 0
                return f"Estimated Body Fat: {bf:.1f}%"
            return "Please provide waist measurement"
        
        elif calc_id == "ideal_weight":
            height = float(data.get("height"))
            gender = data.get("gender", "male")
            if gender == "male":
                ideal = 50 + 2.3 * ((height / 2.54) - 60)
            else:
                ideal = 45.5 + 2.3 * ((height / 2.54) - 60)
            return f"Ideal Weight: {ideal:.1f} kg ({ideal * 2.20462:.1f} lbs)"
        
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
        

        elif calc_id == "investment_return":
            principal = float(data.get("principal"))
            rate = float(data.get("rate")) / 100
            time = float(data.get("time"))
            amount = principal * (1 + rate) ** time
            return f"Future Value: ${amount:,.2f}, Return: ${amount - principal:,.2f}"
        
        elif calc_id == "savings_goal":
            goal = float(data.get("goal"))
            rate = float(data.get("rate", 0)) / 100 / 12
            months = float(data.get("months"))
            if rate > 0:
                payment = goal * rate / ((1 + rate)**months - 1)
            else:
                payment = goal / months
            return f"Monthly Savings Needed: ${payment:,.2f}"
        
        elif calc_id == "retirement":
            current_age = float(data.get("current_age"))
            retire_age = float(data.get("retire_age"))
            current_savings = float(data.get("current_savings", 0))
            monthly_contribution = float(data.get("monthly_contribution", 0))
            rate = float(data.get("rate", 5)) / 100 / 12
            months = (retire_age - current_age) * 12
            future_value = current_savings * (1 + rate) ** months
            if monthly_contribution > 0:
                future_value += monthly_contribution * (((1 + rate) ** months - 1) / rate)
            return f"Retirement Savings: ${future_value:,.2f}"
        
        elif calc_id == "currency_converter":
            amount = float(data.get("amount"))
            from_curr = float(data.get("from_rate", 1))
            to_curr = float(data.get("to_rate", 1))
            result = (amount / from_curr) * to_curr
            return f"Converted Amount: {result:,.2f}"
        
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
        
        elif calc_id == "area_trapezoid":
            base1 = float(data.get("base1"))
            base2 = float(data.get("base2"))
            height = float(data.get("height"))
            area = 0.5 * (base1 + base2) * height
            return f"Area: {area:.2f} square units"
        
        elif calc_id == "volume_cylinder":
            radius = float(data.get("radius"))
            height = float(data.get("height"))
            volume = math.pi * radius ** 2 * height
            return f"Volume: {volume:.2f} cubic units"
        
        elif calc_id == "volume_cube":
            side = float(data.get("side"))
            volume = side ** 3
            return f"Volume: {volume:.2f} cubic units"
        
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
        
        elif calc_id == "unit_length":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "meter": 1, "km": 1000, "cm": 0.01, "mm": 0.001,
                "mile": 1609.34, "yard": 0.9144, "foot": 0.3048, "inch": 0.0254
            }
            result = value * conversions.get(from_unit, 1) / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_weight":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "kg": 1, "gram": 0.001, "pound": 0.453592, "ounce": 0.0283495, "ton": 1000
            }
            result = value * conversions.get(from_unit, 1) / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_volume":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "liter": 1, "ml": 0.001, "gallon": 3.78541, "quart": 0.946353, "cup": 0.236588
            }
            result = value * conversions.get(from_unit, 1) / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_area":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "sq_meter": 1, "sq_km": 1000000, "sq_mile": 2589988, "acre": 4046.86, "hectare": 10000
            }
            result = value * conversions.get(from_unit, 1) / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_speed":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "mps": 1, "kmh": 0.277778, "mph": 0.44704, "knot": 0.514444
            }
            result = value * conversions.get(from_unit, 1) / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "grade":
            points = float(data.get("points"))
            total = float(data.get("total"))
            percentage = (points / total) * 100
            return f"Grade: {percentage:.2f}%"
        

        
        elif calc_id == "test_score":
            correct = float(data.get("correct"))
            total = float(data.get("total"))
            percentage = (correct / total) * 100
            return f"Test Score: {percentage:.2f}%"
        
        elif calc_id == "final_grade":
            current = float(data.get("current"))
            desired = float(data.get("desired"))
            weight = float(data.get("weight")) / 100
            needed = (desired - current * (1 - weight)) / weight
            return f"Grade Needed on Final: {needed:.2f}%"
        
        elif calc_id == "acceleration":
            v1 = float(data.get("v1"))
            v2 = float(data.get("v2"))
            time = float(data.get("time"))
            accel = (v2 - v1) / time
            return f"Acceleration: {accel:.2f} m/s²"
        
        elif calc_id == "potential_energy":
            mass = float(data.get("mass"))
            height = float(data.get("height"))
            g = 9.81
            pe = mass * g * height
            return f"Potential Energy: {pe:.2f} J"
        
        elif calc_id == "power_physics":
            work = float(data.get("work", 0))
            time = float(data.get("time", 0))
            force = float(data.get("force", 0))
            velocity = float(data.get("velocity", 0))
            if work > 0 and time > 0:
                power = work / time
            elif force > 0 and velocity > 0:
                power = force * velocity
            else:
                return "Please provide work & time or force & velocity"
            return f"Power: {power:.2f} W"
        
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
        
        elif calc_id == "fuel_cost":
            distance = float(data.get("distance"))
            mpg = float(data.get("mpg"))
            price = float(data.get("price"))
            gallons = distance / mpg
            cost = gallons * price
            return f"Fuel Needed: {gallons:.2f} gallons, Cost: ${cost:.2f}"
        
        elif calc_id == "car_loan":
            principal = float(data.get("principal"))
            rate = float(data.get("rate")) / 100 / 12
            months = float(data.get("months"))
            payment = principal * (rate * (1 + rate)**months) / ((1 + rate)**months - 1)
            return f"Monthly Payment: ${payment:,.2f}"
        
        elif calc_id == "recipe_scaler":
            original_servings = float(data.get("original"))
            new_servings = float(data.get("new"))
            factor = new_servings / original_servings
            return f"Scale Factor: {factor:.2f}x (multiply all ingredients by this)"
        
        elif calc_id == "alcohol_units":
            drinks = float(data.get("drinks"))
            abv = float(data.get("abv"))
            volume = float(data.get("volume"))
            units = (drinks * volume * abv) / 1000
            return f"Alcohol Units: {units:.2f}"
        
        elif calc_id == "pregnancy_due":
            lmp_str = data.get("lmp")
            if not lmp_str:
                return "Error: Please provide last menstrual period date"
            lmp = datetime.strptime(lmp_str, "%Y-%m-%d")
            due_date = lmp + timedelta(days=280)
            return f"Due Date: {due_date.strftime('%Y-%m-%d')}"
        
        elif calc_id == "ovulation":
            cycle = float(data.get("cycle", 28))
            ovulation_day = cycle - 14
            return f"Ovulation Day: Day {ovulation_day:.0f} of cycle"
        
        elif calc_id == "sleep_hours":
            bedtime = data.get("bedtime")
            wake_time = data.get("wake_time")
            if bedtime and wake_time:
                bed = datetime.strptime(bedtime, "%H:%M")
                wake = datetime.strptime(wake_time, "%H:%M")
                if wake < bed:
                    wake += timedelta(days=1)
                hours = (wake - bed).total_seconds() / 3600
                cycles = hours / 1.5
                return f"Sleep: {hours:.1f} hours ({cycles:.1f} cycles)"
            return "Please provide bedtime and wake time"
        
        elif calc_id == "protein_needs":
            weight = float(data.get("weight"))
            activity = data.get("activity", "moderate")
            multiplier = {"sedentary": 0.8, "moderate": 1.2, "active": 1.6}.get(activity, 1.2)
            protein = weight * multiplier
            return f"Daily Protein: {protein:.1f} grams"
        
        elif calc_id == "carbs_needs":
            calories = float(data.get("calories"))
            carbs = calories * 0.45 / 4
            return f"Daily Carbs: {carbs:.1f} grams"
        
        elif calc_id == "fiber_needs":
            calories = float(data.get("calories"))
            fiber = calories / 100
            return f"Daily Fiber: {fiber:.1f} grams"
        
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
        
        elif calc_id == "electricity_cost":
            power = float(data.get("power"))
            hours = float(data.get("hours"))
            rate = float(data.get("rate"))
            cost = (power / 1000) * hours * rate
            return f"Cost: ${cost:.2f}"
        
        elif calc_id == "work_days_old":
            start_str = data.get("start")
            end_str = data.get("end")
            if not start_str or not end_str:
                return "Error: Please provide both dates"
            start = datetime.strptime(start_str, "%Y-%m-%d")
            end = datetime.strptime(end_str, "%Y-%m-%d")
            days = 0
            current = start
            while current <= end:
                if current.weekday() < 5:
                    days += 1
                current += timedelta(days=1)
            return f"Work Days: {days}"
        
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
            if n < 0:
                return "Error: n must be non-negative"
            fib = [0, 1]
            for i in range(2, n + 1):
                fib.append(fib[i-1] + fib[i-2])
            return f"Fibonacci({n}): {fib[:n+1]}"
        
        elif calc_id == "random_number":
            min_val = int(float(data.get("min", 1)))
            max_val = int(float(data.get("max", 100)))
            import random
            result = random.randint(min_val, max_val)
            return f"Random Number: {result}"
        
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
            from collections import Counter
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
        
        elif calc_id == "acceleration":
            initial_velocity = float(data.get("initial_velocity", 0))
            final_velocity = float(data.get("final_velocity"))
            time = float(data.get("time"))
            acceleration = (final_velocity - initial_velocity) / time
            return f"Acceleration: {acceleration:.2f} m/s²"
        
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
        
        elif calc_id == "binary":
            number = int(float(data.get("number")))
            binary = bin(number)[2:]
            return f"Binary: {binary}"
        
        elif calc_id == "hex":
            number = int(float(data.get("number")))
            hexadecimal = hex(number)[2:].upper()
            return f"Hexadecimal: {hexadecimal}"
        
        elif calc_id == "octal":
            number = int(float(data.get("number")))
            octal = oct(number)[2:]
            return f"Octal: {octal}"
        
        elif calc_id == "prime_check":
            n = int(float(data.get("number")))
            if n < 2:
                return f"{n} is not a prime number"
            for i in range(2, int(n ** 0.5) + 1):
                if n % i == 0:
                    return f"{n} is not a prime number"
            return f"{n} is a prime number"
        
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
            import random
            result = random.randint(min_val, max_val)
            return f"Random Number: {result}"
        
        elif calc_id == "density":
            mass = float(data.get("mass"))
            volume = float(data.get("volume"))
            density = mass / volume
            return f"Density: {density:.2f} kg/m³"
        
        elif calc_id == "momentum":
            mass = float(data.get("mass"))
            velocity = float(data.get("velocity"))
            momentum = mass * velocity
            return f"Momentum: {momentum:.2f} kg⋅m/s"
        
        elif calc_id == "potential_energy":
            mass = float(data.get("mass"))
            height = float(data.get("height"))
            g = 9.8
            pe = mass * g * height
            return f"Potential Energy: {pe:.2f} J"
        
        elif calc_id == "power_physics":
            work = float(data.get("work"))
            time = float(data.get("time"))
            power = work / time
            return f"Power: {power:.2f} W"
        
        elif calc_id == "work":
            force = float(data.get("force"))
            distance = float(data.get("distance"))
            work = force * distance
            return f"Work: {work:.2f} J"
        
        elif calc_id == "pressure_physics":
            force = float(data.get("force"))
            area = float(data.get("area"))
            pressure = force / area
            return f"Pressure: {pressure:.2f} Pa"
        
        elif calc_id == "grade":
            score = float(data.get("score"))
            total = float(data.get("total"))
            percentage = (score / total) * 100
            return f"Grade: {percentage:.2f}%"
        
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
        
        elif calc_id == "cgpa":
            grades_str = data.get("grades", "")
            if not grades_str.strip():
                return "Error: Please provide GPAs separated by commas"
            
            try:
                grades = [float(g.strip()) for g in grades_str.split(",") if g.strip()]
                if not grades:
                    return "Error: Please provide at least one GPA"
                
                # Validate GPA range (typically 0.0 to 4.0)
                for gpa in grades:
                    if gpa < 0.0 or gpa > 4.0:
                        return f"Error: GPA {gpa} is out of range (0.0 - 4.0)"
                
                cgpa = sum(grades) / len(grades)
                return f"CGPA: {cgpa:.2f} (based on {len(grades)} courses)"
                
            except ValueError:
                return "Error: Please enter valid numbers separated by commas (e.g., 3.5, 3.8, 4.0)"
        
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
        
        elif calc_id == "countdown":
            date_str = data.get("date")
            if not date_str:
                return "Error: Please provide a target date"
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
            today = datetime.today()
            days = (target_date - today).days
            return f"Days Until Event: {days} days"
        
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
        
        elif calc_id == "electricity_cost":
            watts = float(data.get("watts"))
            hours = float(data.get("hours"))
            rate = float(data.get("rate"))
            kwh = (watts * hours) / 1000
            cost = kwh * rate
            return f"Electricity Cost: ${cost:.2f} ({kwh:.2f} kWh)"
        
        elif calc_id == "tile_needed":
            length = float(data.get("length"))
            width = float(data.get("width"))
            tile_size = float(data.get("tile_size"))
            area = length * width
            tiles = area / (tile_size ** 2)
            return f"Tiles Needed: {math.ceil(tiles)} tiles"
        
        elif calc_id == "flooring":
            length = float(data.get("length"))
            width = float(data.get("width"))
            area = length * width
            return f"Flooring Needed: {area:.2f} sq ft"
        
        elif calc_id == "fence":
            length = float(data.get("length"))
            width = float(data.get("width"))
            perimeter = 2 * (length + width)
            return f"Fence Length Needed: {perimeter:.2f} ft"
        
        elif calc_id == "concrete":
            length = float(data.get("length"))
            width = float(data.get("width"))
            depth = float(data.get("depth"))
            volume = length * width * depth
            cubic_yards = volume / 27
            return f"Concrete Needed: {cubic_yards:.2f} cubic yards"
        
        elif calc_id == "roofing":
            length = float(data.get("length"))
            width = float(data.get("width"))
            pitch = float(data.get("pitch", 0))
            area = length * width
            if pitch > 0:
                area *= (1 + (pitch / 12) ** 2) ** 0.5
            squares = area / 100
            return f"Roofing Needed: {squares:.2f} squares ({area:.2f} sq ft)"
        
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
        
        elif calc_id == "unit_length":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "meters": 1, "kilometers": 1000, "centimeters": 0.01,
                "millimeters": 0.001, "miles": 1609.34, "yards": 0.9144,
                "feet": 0.3048, "inches": 0.0254
            }
            meters = value * conversions.get(from_unit, 1)
            result = meters / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_weight":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "kilograms": 1, "grams": 0.001, "milligrams": 0.000001,
                "pounds": 0.453592, "ounces": 0.0283495, "tons": 1000
            }
            kg = value * conversions.get(from_unit, 1)
            result = kg / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_volume":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "liters": 1, "milliliters": 0.001, "gallons": 3.78541,
                "quarts": 0.946353, "pints": 0.473176, "cups": 0.236588,
                "fluid_ounces": 0.0295735, "cubic_meters": 1000
            }
            liters = value * conversions.get(from_unit, 1)
            result = liters / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_area":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "square_meters": 1, "square_kilometers": 1000000,
                "square_feet": 0.092903, "square_yards": 0.836127,
                "acres": 4046.86, "hectares": 10000
            }
            sq_meters = value * conversions.get(from_unit, 1)
            result = sq_meters / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_speed":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "meters_per_second": 1, "kilometers_per_hour": 0.277778,
                "miles_per_hour": 0.44704, "feet_per_second": 0.3048,
                "knots": 0.514444
            }
            mps = value * conversions.get(from_unit, 1)
            result = mps / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_time":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "seconds": 1, "minutes": 60, "hours": 3600,
                "days": 86400, "weeks": 604800, "years": 31536000
            }
            seconds = value * conversions.get(from_unit, 1)
            result = seconds / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_energy":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "joules": 1, "kilojoules": 1000, "calories": 4.184,
                "kilocalories": 4184, "watt_hours": 3600, "kilowatt_hours": 3600000
            }
            joules = value * conversions.get(from_unit, 1)
            result = joules / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_power":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "watts": 1, "kilowatts": 1000, "horsepower": 745.7,
                "btu_per_hour": 0.293071
            }
            watts = value * conversions.get(from_unit, 1)
            result = watts / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
        elif calc_id == "unit_pressure":
            value = float(data.get("value"))
            from_unit = data.get("from")
            to_unit = data.get("to")
            conversions = {
                "pascals": 1, "kilopascals": 1000, "bar": 100000,
                "psi": 6894.76, "atmospheres": 101325
            }
            pascals = value * conversions.get(from_unit, 1)
            result = pascals / conversions.get(to_unit, 1)
            return f"{value} {from_unit} = {result:.4f} {to_unit}"
        
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
        
        elif calc_id == "alcohol_units":
            volume = float(data.get("volume"))
            abv = float(data.get("abv"))
            units = (volume * abv) / 1000
            return f"Alcohol Units: {units:.2f} units"
        
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
        
        elif calc_id == "solar_panels":
            monthly_bill = float(data.get("monthly_bill"))
            rate = float(data.get("rate", 0.12))
            kwh_per_month = monthly_bill / rate
            kwh_per_day = kwh_per_month / 30
            panels = kwh_per_day / 1.5
            return f"Solar Panels Needed: {math.ceil(panels)} panels (250W each)"
        
        elif calc_id == "pregnancy_due":
            lmp_str = data.get("lmp")
            if not lmp_str:
                return "Error: Please provide last menstrual period date"
            lmp = datetime.strptime(lmp_str, "%Y-%m-%d")
            due_date = lmp + timedelta(days=280)
            return f"Due Date: {due_date.strftime('%B %d, %Y')}"
        
        elif calc_id == "ovulation":
            lmp_str = data.get("lmp")
            if not lmp_str:
                return "Error: Please provide last menstrual period date"
            lmp = datetime.strptime(lmp_str, "%Y-%m-%d")
            cycle_length = int(float(data.get("cycle_length", 28)))
            ovulation = lmp + timedelta(days=cycle_length - 14)
            return f"Ovulation Date: {ovulation.strftime('%B %d, %Y')}"
        
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
        
        elif calc_id == "tire_size":
            width = float(data.get("width"))
            aspect = float(data.get("aspect"))
            diameter = float(data.get("diameter"))
            sidewall = width * aspect / 100
            total_diameter = (diameter * 25.4) + (2 * sidewall)
            circumference = total_diameter * 3.14159
            return f"Tire Diameter: {total_diameter:.2f}mm, Circumference: {circumference:.2f}mm"
        
        elif calc_id == "lease_vs_buy":
            car_price = float(data.get("car_price"))
            lease_payment = float(data.get("lease_payment"))
            lease_months = float(data.get("lease_months"))
            loan_payment = float(data.get("loan_payment"))
            loan_months = float(data.get("loan_months"))
            lease_total = lease_payment * lease_months
            loan_total = loan_payment * loan_months
            savings = abs(lease_total - loan_total)
            better = "Leasing" if lease_total < loan_total else "Buying"
            return f"{better} is better. Lease: ${lease_total:,.2f}, Buy: ${loan_total:,.2f}, Savings: ${savings:,.2f}"
        
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
        

        elif calc_id == "fuel_economy":
            distance, error = get_float_value(data, "distance")
            if error: return error
            fuel, error = get_float_value(data, "fuel")
            if error: return error
            if distance <= 0 or fuel <= 0:
                return "Error: Distance and fuel must be positive"
            mpg = distance / fuel
            return f"Fuel Economy: {mpg:.2f} MPG"
        

        elif calc_id == "tax":
            amount, error = get_float_value(data, "amount")
            if error: return error
            rate, error = get_float_value(data, "rate")
            if error: return error
            if amount <= 0 or rate < 0:
                return "Error: Amount must be positive, rate cannot be negative"
            tax = amount * (rate / 100)
            total = amount + tax
            return f"Tax: ${tax:.2f}, Total: ${total:.2f}"
        
        elif calc_id == "grade":
            earned, error = get_float_value(data, "earned")
            if error: return error
            total, error = get_float_value(data, "total")
            if error: return error
            if total <= 0:
                return "Error: Total points must be positive"
            percentage = (earned / total) * 100
            letter = "A" if percentage >= 90 else "B" if percentage >= 80 else "C" if percentage >= 70 else "D" if percentage >= 60 else "F"
            return f"Grade: {percentage:.1f}% ({letter})"
        
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
        
        elif calc_id == "investment":
            initial, error = get_float_value(data, "initial")
            if error: return error
            monthly, error = get_float_value(data, "monthly")
            if error: return error
            annual_return, error = get_float_value(data, "return")
            if error: return error
            years, error = get_float_value(data, "years")
            if error: return error
            monthly_rate = annual_return / 100 / 12
            months = years * 12
            # Future value of initial investment
            fv_initial = initial * (1 + monthly_rate) ** months
            # Future value of monthly contributions
            if monthly_rate == 0:
                fv_monthly = monthly * months
            else:
                fv_monthly = monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
            total = fv_initial + fv_monthly
            return f"Investment Value: ${total:,.2f} after {years} years"
        
        elif calc_id == "body_fat":
            gender = data.get("gender")
            age, error = get_float_value(data, "age")
            if error: return error
            weight, error = get_float_value(data, "weight")
            if error: return error
            height, error = get_float_value(data, "height")
            if error: return error
            # Using BMI-based estimation (simplified)
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            if gender == "male":
                body_fat = (1.20 * bmi) + (0.23 * age) - 16.2
            else:
                body_fat = (1.20 * bmi) + (0.23 * age) - 5.4
            return f"Estimated Body Fat: {max(0, body_fat):.1f}%"
        
        elif calc_id == "ideal_weight":
            gender = data.get("gender")
            height, error = get_float_value(data, "height")
            if error: return error
            if height <= 0:
                return "Error: Height must be positive"
            # Using Devine formula
            if gender == "male":
                ideal = 50 + 2.3 * ((height - 152.4) / 2.54)
            else:
                ideal = 45.5 + 2.3 * ((height - 152.4) / 2.54)
            return f"Ideal Weight: {max(30, ideal):.1f} kg"
        
        elif calc_id == "pregnancy":
            lmp_str = data.get("lmp")
            if not lmp_str:
                return "Error: Please provide last menstrual period date"
            lmp = datetime.strptime(lmp_str, "%Y-%m-%d")
            due_date = lmp + timedelta(days=280)
            today = datetime.today()
            weeks = (today - lmp).days // 7
            return f"Due Date: {due_date.strftime('%Y-%m-%d')}, Current: {weeks} weeks"
        
        elif calc_id == "area_square":
            side, error = get_float_value(data, "side")
            if error: return error
            if side <= 0:
                return "Error: Side length must be positive"
            area = side ** 2
            return f"Area: {area:.2f} square units"
        
        elif calc_id == "volume_cube":
            side, error = get_float_value(data, "side")
            if error: return error
            if side <= 0:
                return "Error: Side length must be positive"
            volume = side ** 3
            return f"Volume: {volume:.2f} cubic units"
        
        elif calc_id == "volume_cylinder":
            radius, error = get_float_value(data, "radius")
            if error: return error
            height, error = get_float_value(data, "height")
            if error: return error
            if radius <= 0 or height <= 0:
                return "Error: Radius and height must be positive"
            volume = math.pi * radius ** 2 * height
            return f"Volume: {volume:.2f} cubic units"
        
        elif calc_id == "quadratic":
            a, error = get_float_value(data, "a")
            if error: return error
            b, error = get_float_value(data, "b")
            if error: return error
            c, error = get_float_value(data, "c")
            if error: return error
            if a == 0:
                return "Error: 'a' cannot be zero in quadratic equation"
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return "No real solutions (discriminant < 0)"
            elif discriminant == 0:
                x = -b / (2*a)
                return f"One solution: x = {x:.2f}"
            else:
                x1 = (-b + math.sqrt(discriminant)) / (2*a)
                x2 = (-b - math.sqrt(discriminant)) / (2*a)
                return f"Two solutions: x₁ = {x1:.2f}, x₂ = {x2:.2f}"
        
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

def save_feedback_to_db(name, email, subject, message, rating=None, feedback_type=None, wants_updates=False):
    """Save feedback to MySQL database or fallback to console logging"""
    try:
        connection = get_db_connection()
        if not connection:
            # Fallback to console logging for local development
            print(f"\n{'='*60}")
            print(f"📧 FEEDBACK (DB unavailable - logging to console)")
            print(f"FROM: {name} ({email})")
            print(f"SUBJECT: {subject}")
            print(f"RATING: {rating}/5 stars")
            print(f"TYPE: {feedback_type}")
            print(f"WANTS UPDATES: {wants_updates}")
            print(f"MESSAGE: {message}")
            print(f"{'='*60}")
            return True
        
        cursor = connection.cursor()
        
        query = """
            INSERT INTO feedback (name, email, subject, message, rating, feedback_type, wants_updates)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (name, email, subject, message, rating, feedback_type, wants_updates)
        cursor.execute(query, values)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        print(f"Feedback saved to database: {subject} from {name}")
        return True
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        # Fallback to console logging
        print(f"📧 FEEDBACK (DB error - logging to console): {subject} from {name}")
        return True
    except Exception as e:
        print(f"Failed to save feedback: {str(e)}")
        return False

def save_contact_to_db(name, email, subject, message):
    """Save contact message to MySQL database or fallback to console logging"""
    try:
        connection = get_db_connection()
        if not connection:
            # Fallback to console logging for local development
            print(f"\n{'='*60}")
            print(f"📞 CONTACT (DB unavailable - logging to console)")
            print(f"FROM: {name} ({email})")
            print(f"SUBJECT: {subject}")
            print(f"MESSAGE: {message}")
            print(f"{'='*60}")
            return True
        
        cursor = connection.cursor()
        
        query = """
            INSERT INTO contact (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
        """
        
        values = (name, email, subject, message)
        cursor.execute(query, values)
        connection.commit()
        
        cursor.close()
        connection.close()
        
        print(f"Contact message saved to database: {subject} from {name}")
        return True
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        # Fallback to console logging
        print(f"📞 CONTACT (DB error - logging to console): {subject} from {name}")
        return True
    except Exception as e:
        print(f"Failed to save contact: {str(e)}")
        return False
    
    # If Gmail fails, return False (no file fallback)
    print(f"❌ Failed to send email to {receiver_email}")
    print("📧 Configure Gmail SMTP to receive emails directly")
    return False

@app.route("/contact", methods=["POST"])
def contact_form():
    try:
        data = request.json
        name = data.get("name", "Anonymous")
        email = data.get("email", "No email provided")
        subject = data.get("subject", "General Inquiry")
        message = data.get("message", "")
        
        # Create email body
        email_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #667eea; text-align: center;">New Contact Form Submission</h2>
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
                    <p><strong>Subject:</strong> {subject}</p>
                </div>
                <div style="background: #fff; padding: 15px; border-left: 4px solid #667eea; margin: 20px 0;">
                    <h3>Message:</h3>
                    <p>{message}</p>
                </div>
                <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                <p style="text-align: center; color: #666; font-size: 12px;">
                    Sent from CalcMaster Pro Contact Form<br>
                    <a href="mailto:{email}">Reply to {name}</a>
                </p>
            </div>
        </body>
        </html>
        """
        
        # Save contact to database
        success = save_contact_to_db(name, email, subject, message)
        
        if success:
            return jsonify({"success": True, "message": "Message received! Thank you for contacting us."})
        else:
            return jsonify({"success": False, "message": "Failed to save message. Please try again."})
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route("/feedback", methods=["POST"])
def feedback_form():
    try:
        data = request.json
        name = data.get("name", "Anonymous")
        email = data.get("email", "No email provided")
        rating = data.get("rating", "Not provided")
        feedback_type = data.get("type", "General")
        message = data.get("message", "")
        updates = data.get("updates", False)
        
        # Create feedback text
        stars = "*" * int(rating) + "-" * (5 - int(rating))
        feedback_text = f"""Name: {name}
Email: {email}
Rating: {stars} ({rating}/5 stars)
Type: {feedback_type}
Wants Updates: {"Yes" if updates else "No"}
Message: {message}"""
        
        # Save feedback to database
        success = save_feedback_to_db(name, email, f"Feedback: {feedback_type}", message, rating, feedback_type, updates)
        
        if success:
            return jsonify({"success": True, "message": "Thank you for your feedback! We appreciate your input."})
        else:
            return jsonify({"success": False, "message": "Failed to save feedback. Please try again."})
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route("/feedback-view")
def view_feedback():
    """View all feedback submissions from database"""
    try:
        connection = get_db_connection()
        if not connection:
            return "Database connection failed"
        
        cursor = connection.cursor(dictionary=True)
        
        # Get all feedback
        cursor.execute("""
            SELECT * FROM feedback 
            ORDER BY created_at DESC
        """)
        feedback_data = cursor.fetchall()
        
        # Get all contact messages
        cursor.execute("""
            SELECT *, 'contact' as type FROM contact 
            ORDER BY created_at DESC
        """)
        contact_data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        # Combine and sort by date
        all_messages = []
        
        for item in feedback_data:
            stars = "★" * (item['rating'] or 0) + "☆" * (5 - (item['rating'] or 0))
            all_messages.append({
                'type': 'feedback',
                'name': item['name'],
                'email': item['email'],
                'subject': item['subject'],
                'message': item['message'],
                'rating': f"{stars} ({item['rating']}/5)" if item['rating'] else "No rating",
                'feedback_type': item['feedback_type'],
                'wants_updates': "Yes" if item['wants_updates'] else "No",
                'created_at': item['created_at']
            })
        
        for item in contact_data:
            all_messages.append({
                'type': 'contact',
                'name': item['name'],
                'email': item['email'],
                'subject': item['subject'],
                'message': item['message'],
                'created_at': item['created_at']
            })
        
        # Sort by date (newest first)
        all_messages.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Generate HTML
        messages_html = ""
        if not all_messages:
            messages_html = "<p>No feedback or messages received yet.</p>"
        else:
            for msg in all_messages:
                if msg['type'] == 'feedback':
                    messages_html += f"""
                    <div class="message feedback-msg">
                        <h4>⭐ Feedback: {msg['feedback_type']}</h4>
                        <p><strong>From:</strong> {msg['name']} ({msg['email']})</p>
                        <p><strong>Rating:</strong> {msg['rating']}</p>
                        <p><strong>Wants Updates:</strong> {msg['wants_updates']}</p>
                        <p><strong>Message:</strong> {msg['message']}</p>
                        <p><strong>Date:</strong> {msg['created_at']}</p>
                    </div>
                    """
                else:
                    messages_html += f"""
                    <div class="message contact-msg">
                        <h4>📞 Contact: {msg['subject']}</h4>
                        <p><strong>From:</strong> {msg['name']} ({msg['email']})</p>
                        <p><strong>Message:</strong> {msg['message']}</p>
                        <p><strong>Date:</strong> {msg['created_at']}</p>
                    </div>
                    """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>CalcMaster Pro - Feedback Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ text-align: center; color: #667eea; margin-bottom: 30px; }}
                .message {{ background: #f8f9fa; padding: 20px; margin: 15px 0; border-left: 4px solid #667eea; border-radius: 5px; }}
                .feedback-msg {{ border-left-color: #28a745; }}
                .contact-msg {{ border-left-color: #007bff; }}
                .back-btn {{ display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-bottom: 20px; }}
                .back-btn:hover {{ background: #5a6fd8; }}
                .stats {{ display: flex; gap: 20px; margin-bottom: 30px; }}
                .stat {{ background: #667eea; color: white; padding: 15px; border-radius: 8px; text-align: center; flex: 1; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 CalcMaster Pro Dashboard</h1>
                    <p>Feedback and Contact Messages</p>
                </div>
                <a href="/" class="back-btn">← Back to Calculator</a>
                
                <div class="stats">
                    <div class="stat">
                        <h3>{len([m for m in all_messages if m['type'] == 'feedback'])}</h3>
                        <p>Feedback Messages</p>
                    </div>
                    <div class="stat">
                        <h3>{len([m for m in all_messages if m['type'] == 'contact'])}</h3>
                        <p>Contact Messages</p>
                    </div>
                    <div class="stat">
                        <h3>{len(all_messages)}</h3>
                        <p>Total Messages</p>
                    </div>
                </div>
                
                <div class="messages">
                    {messages_html}
                </div>
            </div>
        </body>
        </html>
        """
        
    except mysql.connector.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error loading feedback: {str(e)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
