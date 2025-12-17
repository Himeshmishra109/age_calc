from flask import Flask, render_template, request, jsonify, Response, send_from_directory, url_for, redirect
from datetime import datetime, timedelta
import math
import random
import json
import os
from collections import Counter

app = Flask(__name__)

# Load calculators list from JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data", "calculators.json")

with open(DATA_FILE, "r", encoding="utf-8") as file:
    CALCULATORS = json.load(file)

def get_calculator_content(calc_id):
    """Get specific content for each calculator"""
    content_map = {
        # Date & Time Calculators
        "age": {
            "description": "Calculate your exact age in years, months, and days from your birth date.",
            "usage": [
                "Enter your birth date in the date field",
                "Click 'Calculate' to get your exact age",
                "View results in years, months, and days",
                "Perfect for official documents and birthday planning"
            ],
            "formula": "Age = Current Date - Birth Date (accounting for leap years and varying month lengths)",
            "examples": ["Born on January 15, 1990 → Age: 35 years, 0 months, 1 day (as of Jan 16, 2025)"],
            "use_cases": ["Official documents", "Birthday planning", "Age verification", "Personal records"],
            "key_features": [
                "Precise calculation including leap years",
                "Results in years, months, and days format",
                "Instant calculation from any birth date",
                "Perfect for legal and official documentation",
                "Works with any date from 1900 onwards"
            ]
        },
        "days_between": {
            "description": "Calculate the exact number of days between two dates.",
            "usage": [
                "Enter the first date",
                "Enter the second date", 
                "Click 'Calculate' to get the difference",
                "Result shows total days between dates"
            ],
            "formula": "Days = |Date2 - Date1|",
            "examples": ["Jan 1, 2025 to Jan 31, 2025 = 30 days"],
            "use_cases": ["Project planning", "Event countdown", "Duration calculation", "Timeline planning"],
            "key_features": [
                "Handles any date range from past to future",
                "Accounts for leap years automatically",
                "Instant calculation with exact day count",
                "Perfect for project timeline planning",
                "Works with dates from 1900 to 2100"
            ]
        },
        "date_add": {
            "description": "Add or subtract days from any date to find a future or past date.",
            "usage": [
                "Enter the starting date",
                "Enter number of days to add (positive) or subtract (negative)",
                "Click 'Calculate' to get the result date"
            ],
            "formula": "Result Date = Starting Date ± Number of Days",
            "examples": ["Jan 1, 2025 + 30 days = Jan 31, 2025"],
            "use_cases": ["Due date calculation", "Deadline planning", "Schedule management", "Event planning"]
        },
        "weekday": {
            "description": "Find out what day of the week any date falls on.",
            "usage": [
                "Enter any date",
                "Click 'Calculate' to find the weekday",
                "Result shows the day name (Monday, Tuesday, etc.)"
            ],
            "formula": "Uses calendar algorithms to determine weekday",
            "examples": ["January 1, 2025 falls on a Wednesday"],
            "use_cases": ["Historical research", "Event planning", "Schedule verification", "Calendar reference"]
        },
        "leap_year": {
            "description": "Check if any year is a leap year with 366 days instead of 365.",
            "usage": [
                "Enter the year you want to check",
                "Click 'Calculate' to see if it's a leap year"
            ],
            "formula": "Leap if: (year % 4 == 0 AND year % 100 != 0) OR (year % 400 == 0)",
            "examples": ["2024 is a leap year", "2023 is not a leap year"],
            "use_cases": ["Calendar planning", "Date calculations", "Historical research", "Programming"]
        },
        
        # Health Calculators
        "bmi": {
            "description": "Calculate your Body Mass Index to assess if your weight is in a healthy range.",
            "usage": [
                "Enter your weight in kilograms",
                "Enter your height in centimeters", 
                "Click 'Calculate' to get your BMI and category"
            ],
            "formula": "BMI = Weight (kg) / Height (m)²",
            "examples": ["70kg, 175cm → BMI: 22.9 (Normal weight)"],
            "use_cases": ["Health assessment", "Fitness tracking", "Medical consultations", "Weight management"],
            "categories": {
                "Underweight": "BMI less than 18.5",
                "Normal weight": "BMI 18.5-24.9", 
                "Overweight": "BMI 25-29.9",
                "Obese": "BMI 30 or greater"
            },
            "key_features": [
                "WHO standard BMI calculation formula",
                "Automatic health category classification",
                "Supports metric measurements (kg/cm)",
                "Instant health risk assessment",
                "Medical-grade accuracy for consultations"
            ]
        },
        "bmr": {
            "description": "Calculate your Basal Metabolic Rate - calories your body burns at rest.",
            "usage": [
                "Enter your weight in kilograms",
                "Enter your height in centimeters",
                "Enter your age in years",
                "Select your gender",
                "Get your daily calorie needs at rest"
            ],
            "formula": "Men: BMR = 88.362 + (13.397 × weight) + (4.799 × height) - (5.677 × age)\nWomen: BMR = 447.593 + (9.247 × weight) + (3.098 × height) - (4.330 × age)",
            "examples": ["Male, 30 years, 70kg, 175cm → BMR: ~1,680 calories/day"],
            "use_cases": ["Diet planning", "Weight management", "Fitness goals", "Nutrition planning"],
            "key_features": [
                "Uses Harris-Benedict equation (gold standard)",
                "Gender-specific calculation formulas",
                "Foundation for all diet and fitness planning",
                "Accurate baseline calorie requirements",
                "Essential for weight management programs"
            ]
        },
        "calories_burned": {
            "description": "Estimate calories burned during physical activities based on weight and duration.",
            "usage": [
                "Enter your weight in kilograms",
                "Enter exercise duration in minutes",
                "Select activity intensity level",
                "Get estimated calories burned"
            ],
            "formula": "Calories = MET value × weight (kg) × duration (hours)",
            "examples": ["70kg person, 30 min moderate exercise → ~175 calories"],
            "use_cases": ["Fitness tracking", "Weight loss planning", "Exercise monitoring", "Health goals"]
        },
        
        # Finance Calculators  
        "simple_interest": {
            "description": "Calculate simple interest on loans, investments, or savings accounts.",
            "usage": [
                "Enter the principal amount",
                "Enter the annual interest rate (%)",
                "Enter the time period in years",
                "Get interest earned and total amount"
            ],
            "formula": "Simple Interest = (Principal × Rate × Time) / 100\nTotal = Principal + Interest",
            "examples": ["$1,000 at 5% for 2 years → Interest: $100, Total: $1,100"],
            "use_cases": ["Loan calculations", "Investment planning", "Savings growth", "Financial planning"],
            "key_features": [
                "Standard banking industry formula",
                "Shows both interest earned and total amount",
                "Supports any currency and time period",
                "Perfect for loan and investment comparisons",
                "Instant calculation with detailed breakdown"
            ]
        },
        "compound_interest": {
            "description": "Calculate compound interest where interest earns interest over time.",
            "usage": [
                "Enter the principal amount",
                "Enter annual interest rate (%)",
                "Enter time period in years", 
                "Enter compounding frequency",
                "See how your money grows exponentially"
            ],
            "formula": "A = P(1 + r/n)^(nt)\nWhere: A=final amount, P=principal, r=rate, n=compounds per year, t=time",
            "examples": ["$1,000 at 5% compounded annually for 10 years → $1,628.89"],
            "use_cases": ["Investment growth", "Retirement planning", "Savings accounts", "Long-term financial goals"]
        },
        "loan_payment": {
            "description": "Calculate monthly payments for loans including mortgages, car loans, and personal loans.",
            "usage": [
                "Enter the loan amount (principal)",
                "Enter annual interest rate (%)",
                "Enter loan term in months",
                "Get your monthly payment amount"
            ],
            "formula": "PMT = P × [r(1+r)^n] / [(1+r)^n - 1]\nWhere: P=principal, r=monthly rate, n=number of payments",
            "examples": ["$20,000 loan at 6% for 5 years → $386.66/month"],
            "use_cases": ["Mortgage planning", "Car loans", "Personal loans", "Budget planning"],
            "key_features": [
                "Standard banking amortization formula",
                "Works for any loan type and term",
                "Precise monthly payment calculation",
                "Essential for budget and financial planning",
                "Handles various interest rates and terms"
            ]
        },
        "mortgage": {
            "description": "Calculate mortgage payments including principal, interest, and loan details.",
            "usage": [
                "Enter home price",
                "Enter down payment amount",
                "Enter interest rate (%)",
                "Enter loan term in years",
                "Get monthly mortgage payment"
            ],
            "formula": "Monthly Payment = Loan Amount × [r(1+r)^n] / [(1+r)^n - 1]",
            "examples": ["$300,000 home, $60,000 down, 4% for 30 years → $1,146/month"],
            "use_cases": ["Home buying", "Refinancing", "Budget planning", "Real estate investment"]
        },
        
        # Math Calculators
        "percentage": {
            "description": "Calculate what percentage one number is of another, or find a percentage of a number.",
            "usage": [
                "Enter the number you want to find percentage of",
                "Enter the percentage value",
                "Get the calculated result"
            ],
            "formula": "Percentage of Number = (Number × Percentage) / 100",
            "examples": ["25% of 200 = 50", "What % is 30 of 120? = 25%"],
            "use_cases": ["Discounts", "Tax calculations", "Grade calculations", "Statistics"],
            "key_features": [
                "Handles both percentage calculation types",
                "Works with decimals and whole numbers",
                "Essential for shopping and finance",
                "Instant calculation with precise results",
                "Perfect for discount and tax calculations"
            ]
        },
        "area_circle": {
            "description": "Calculate the area of a circle using its radius for geometry and construction projects.",
            "usage": [
                "Enter the radius of the circle",
                "Click 'Calculate' to get the area",
                "Result is shown in square units"
            ],
            "formula": "Area = π × r² (where r is the radius)\nπ (pi) ≈ 3.14159",
            "examples": ["Circle with radius 5 units → Area: 78.54 square units"],
            "use_cases": ["Geometry problems", "Construction projects", "Land measurement", "Engineering"],
            "key_features": [
                "Uses precise π value (3.14159) for accuracy",
                "Works with any unit of measurement",
                "Essential for construction and engineering",
                "Instant calculation with high precision",
                "Perfect for circular area planning"
            ]
        },
        "area_rectangle": {
            "description": "Calculate the area of a rectangle by multiplying length and width.",
            "usage": [
                "Enter the length of the rectangle",
                "Enter the width of the rectangle",
                "Get the total area in square units"
            ],
            "formula": "Area = Length × Width",
            "examples": ["Rectangle 10×5 units → Area: 50 square units"],
            "use_cases": ["Room measurements", "Flooring calculations", "Land area", "Construction planning"]
        },
        "pythagorean": {
            "description": "Calculate missing sides of right triangles using the Pythagorean theorem.",
            "usage": [
                "Enter any two known sides of a right triangle",
                "Leave the unknown side blank",
                "Calculate the missing side length"
            ],
            "formula": "a² + b² = c² (where c is the hypotenuse)",
            "examples": ["Sides 3 and 4 → Hypotenuse: 5"],
            "use_cases": ["Construction", "Engineering", "Navigation", "Geometry problems"],
            "key_features": [
                "Fundamental theorem for right triangles",
                "Works with any two known sides",
                "Essential for construction and engineering",
                "Validates right triangle relationships",
                "High precision for professional use"
            ]
        },
        
        # Physics Calculators
        "speed": {
            "description": "Calculate speed, distance, or time using the fundamental physics relationship.",
            "usage": [
                "Enter any two values (speed, distance, time)",
                "Calculate the missing third value",
                "Results in appropriate units"
            ],
            "formula": "Speed = Distance / Time",
            "examples": ["100 km in 2 hours → Speed: 50 km/h"],
            "use_cases": ["Travel planning", "Physics problems", "Sports analysis", "Transportation"]
        },
        "force": {
            "description": "Calculate force using Newton's second law of motion (F = ma).",
            "usage": [
                "Enter mass in kilograms",
                "Enter acceleration in m/s²",
                "Calculate force in Newtons"
            ],
            "formula": "Force = Mass × Acceleration (F = ma)",
            "examples": ["10 kg mass with 2 m/s² acceleration → Force: 20 N"],
            "use_cases": ["Physics problems", "Engineering", "Mechanics", "Scientific calculations"]
        },
        
        # Unit Conversion Calculators
        "unit_temperature": {
            "description": "Convert temperatures between Celsius, Fahrenheit, and Kelvin scales.",
            "usage": [
                "Enter the temperature value",
                "Select the source unit (°C, °F, or K)",
                "Select the target unit",
                "Get instant conversion results"
            ],
            "formula": "°F = (°C × 9/5) + 32\n°C = (°F - 32) × 5/9\nK = °C + 273.15",
            "examples": ["25°C = 77°F = 298.15K"],
            "use_cases": ["Weather conversion", "Cooking recipes", "Scientific calculations", "Travel planning"]
        },
        "unit_length": {
            "description": "Convert between different units of length and distance measurements.",
            "usage": [
                "Enter the length value",
                "Select source unit (meters, feet, inches, etc.)",
                "Select target unit",
                "Get precise conversion"
            ],
            "formula": "Converts through metric base units for accuracy",
            "examples": ["1 meter = 3.28 feet = 39.37 inches"],
            "use_cases": ["Construction", "Engineering", "Travel", "International trade"]
        },
        "unit_weight": {
            "description": "Convert weight and mass between different measurement systems.",
            "usage": [
                "Enter the weight value",
                "Select source unit (kg, lbs, oz, etc.)",
                "Select target unit",
                "Get accurate conversion"
            ],
            "formula": "Uses standard conversion factors: 1 kg = 2.20462 lbs",
            "examples": ["70 kg = 154.32 lbs = 2,469 oz"],
            "use_cases": ["Health tracking", "Shipping", "Cooking", "International commerce"]
        },
        
        # Education Calculators
        "gpa": {
            "description": "Calculate your Grade Point Average from letter grades.",
            "usage": [
                "Enter your letter grades separated by commas",
                "Supports grades: A, A-, B+, B, B-, C+, C, C-, D+, D, F",
                "Get your calculated GPA on 4.0 scale"
            ],
            "formula": "GPA = Sum of Grade Points / Number of Grades\nA=4.0, A-=3.7, B+=3.3, B=3.0, etc.",
            "examples": ["Grades A, B+, A-, B → GPA: 3.5"],
            "use_cases": ["Academic planning", "College applications", "Scholarship requirements", "Academic progress tracking"]
        },
        "grade": {
            "description": "Calculate percentage grades and letter grades from points earned.",
            "usage": [
                "Enter points earned",
                "Enter total possible points",
                "Get percentage and letter grade"
            ],
            "formula": "Percentage = (Points Earned / Total Points) × 100",
            "examples": ["85 out of 100 points → 85% (B)"],
            "use_cases": ["Test grading", "Assignment evaluation", "Course grades", "Academic assessment"]
        },
        
        # Home & DIY Calculators
        "paint_needed": {
            "description": "Calculate how much paint you need for your painting project.",
            "usage": [
                "Enter room dimensions or wall area",
                "Account for doors and windows",
                "Get paint quantity needed in gallons/liters"
            ],
            "formula": "Paint Needed = (Total Wall Area - Openings) / Coverage per Gallon",
            "examples": ["12×10 room with 8ft ceiling → ~1.5 gallons"],
            "use_cases": ["Home renovation", "Interior painting", "Exterior painting", "Cost estimation"]
        },
        "flooring": {
            "description": "Calculate flooring materials needed for your space.",
            "usage": [
                "Enter room length and width",
                "Add waste factor percentage",
                "Get total square footage needed"
            ],
            "formula": "Total Needed = Room Area × (1 + Waste Factor)",
            "examples": ["12×15 room with 10% waste → 198 sq ft"],
            "use_cases": ["Home renovation", "Flooring installation", "Material ordering", "Cost planning"]
        },
        
        # Automotive Calculators
        "fuel_efficiency": {
            "description": "Calculate your vehicle's fuel efficiency in MPG or KPL.",
            "usage": [
                "Enter distance traveled",
                "Enter fuel consumed",
                "Select units (miles/km, gallons/liters)",
                "Get fuel efficiency rating"
            ],
            "formula": "MPG = Miles Driven / Gallons Used\nKPL = Kilometers Driven / Liters Used",
            "examples": ["300 miles on 12 gallons → 25 MPG"],
            "use_cases": ["Fuel economy tracking", "Vehicle comparison", "Trip planning", "Environmental impact"]
        },
        "fuel_cost": {
            "description": "Calculate the cost of fuel for your trip or commute.",
            "usage": [
                "Enter trip distance",
                "Enter vehicle's fuel efficiency",
                "Enter current fuel price",
                "Get total fuel cost"
            ],
            "formula": "Fuel Cost = (Distance / MPG) × Price per Gallon",
            "examples": ["500 mile trip, 25 MPG, $3.50/gal → $70"],
            "use_cases": ["Trip budgeting", "Commute costs", "Travel planning", "Vehicle expenses"]
        },
        
        # Statistics Calculators
        "mean": {
            "description": "Calculate the arithmetic mean (average) of a set of numbers.",
            "usage": [
                "Enter numbers separated by commas",
                "Click calculate to get the mean",
                "Result shows the average value"
            ],
            "formula": "Mean = Sum of all values / Number of values",
            "examples": ["Numbers: 2, 4, 6, 8, 10 → Mean: 6"],
            "use_cases": ["Data analysis", "Statistics", "Research", "Academic work"]
        },
        "median": {
            "description": "Find the median (middle value) of a dataset.",
            "usage": [
                "Enter numbers separated by commas",
                "Numbers will be automatically sorted",
                "Get the middle value (median)"
            ],
            "formula": "Median = Middle value when numbers are arranged in order",
            "examples": ["Numbers: 1, 3, 5, 7, 9 → Median: 5"],
            "use_cases": ["Statistical analysis", "Data interpretation", "Research", "Quality control"]
        },
        
        # More Math Calculators
        "factorial": {
            "description": "Calculate the factorial of a number (n!).",
            "usage": [
                "Enter a positive integer",
                "Click calculate to get n!",
                "Result shows the factorial value"
            ],
            "formula": "n! = n × (n-1) × (n-2) × ... × 2 × 1",
            "examples": ["5! = 5 × 4 × 3 × 2 × 1 = 120"],
            "use_cases": ["Probability calculations", "Combinatorics", "Mathematics", "Statistics"]
        },
        "percentage_change": {
            "description": "Calculate the percentage increase or decrease between two values.",
            "usage": [
                "Enter the original (old) value",
                "Enter the new value",
                "Get percentage change (+ for increase, - for decrease)"
            ],
            "formula": "Percentage Change = ((New Value - Old Value) / Old Value) × 100",
            "examples": ["From 50 to 75 → +50% increase"],
            "use_cases": ["Financial analysis", "Performance tracking", "Growth calculations", "Data comparison"]
        },
        
        # More Finance Calculators
        "discount": {
            "description": "Calculate discounted prices and savings amount.",
            "usage": [
                "Enter the original price",
                "Enter the discount percentage",
                "Get final price and amount saved"
            ],
            "formula": "Final Price = Original Price × (1 - Discount%/100)\nSavings = Original Price - Final Price",
            "examples": ["$100 item with 25% discount → $75 final price, $25 saved"],
            "use_cases": ["Shopping", "Sales calculations", "Budgeting", "Retail pricing"]
        },
        "tip_calculator": {
            "description": "Calculate tip amount and total bill including tip.",
            "usage": [
                "Enter the bill amount",
                "Enter tip percentage",
                "Get tip amount and total to pay"
            ],
            "formula": "Tip = Bill Amount × (Tip % / 100)\nTotal = Bill Amount + Tip",
            "examples": ["$50 bill with 18% tip → $9 tip, $59 total"],
            "use_cases": ["Restaurant dining", "Service tipping", "Bill splitting", "Hospitality"]
        },
        
        # Additional comprehensive calculator content
        "area_triangle": {
            "description": "Calculate the area of a triangle using base and height measurements.",
            "usage": [
                "Enter the base length of the triangle",
                "Enter the height (perpendicular distance from base to opposite vertex)",
                "Click calculate to get the area in square units"
            ],
            "formula": "Area = (Base × Height) / 2",
            "examples": ["Triangle with base 10 units and height 8 units → Area: 40 square units"],
            "use_cases": ["Geometry homework", "Construction planning", "Land surveying", "Architectural design", "Engineering calculations"]
        },
        
        "area_rectangle": {
            "description": "Calculate the area of a rectangle by multiplying its length and width.",
            "usage": [
                "Enter the length of the rectangle",
                "Enter the width of the rectangle", 
                "Get the total area in square units"
            ],
            "formula": "Area = Length × Width",
            "examples": ["Rectangle 12×8 meters → Area: 96 square meters"],
            "use_cases": ["Room measurements", "Flooring calculations", "Garden planning", "Construction projects", "Real estate"]
        },
        
        "volume_sphere": {
            "description": "Calculate the volume of a sphere using its radius.",
            "usage": [
                "Enter the radius of the sphere",
                "Click calculate to get volume in cubic units",
                "Perfect for spherical objects and containers"
            ],
            "formula": "Volume = (4/3) × π × r³ where r is the radius",
            "examples": ["Sphere with radius 5 cm → Volume: 523.6 cubic cm"],
            "use_cases": ["Engineering design", "Manufacturing", "Scientific calculations", "Storage planning", "3D modeling"]
        },
        
        "volume_cylinder": {
            "description": "Calculate the volume of a cylinder using radius and height.",
            "usage": [
                "Enter the radius of the circular base",
                "Enter the height of the cylinder",
                "Get volume in cubic units"
            ],
            "formula": "Volume = π × r² × h where r is radius and h is height",
            "examples": ["Cylinder: radius 3 cm, height 10 cm → Volume: 282.7 cubic cm"],
            "use_cases": ["Tank capacity", "Pipe volume", "Container design", "Engineering", "Manufacturing"]
        },
        
        "compound_interest": {
            "description": "Calculate compound interest where interest earns interest over time, showing the power of compounding.",
            "usage": [
                "Enter the principal (initial) amount",
                "Enter annual interest rate as percentage",
                "Enter time period in years",
                "Enter compounding frequency (monthly, quarterly, annually)",
                "See how your investment grows exponentially"
            ],
            "formula": "A = P(1 + r/n)^(nt) where A=final amount, P=principal, r=annual rate, n=compounds per year, t=time in years",
            "examples": ["$5,000 at 6% compounded monthly for 10 years → $9,110.59 (total gain: $4,110.59)"],
            "use_cases": ["Investment planning", "Retirement savings", "Education funds", "Long-term financial goals", "Wealth building"],
            "key_features": [
                "Shows the power of compounding over time",
                "Supports multiple compounding frequencies",
                "Displays both final amount and interest earned",
                "Essential for long-term investment planning",
                "Demonstrates exponential growth potential"
            ]
        },
        
        "mortgage": {
            "description": "Calculate monthly mortgage payments for home loans including principal and interest.",
            "usage": [
                "Enter the home purchase price",
                "Enter your down payment amount",
                "Enter the annual interest rate",
                "Enter loan term in years (typically 15 or 30)",
                "Get your monthly payment amount"
            ],
            "formula": "Monthly Payment = [P × r(1+r)^n] / [(1+r)^n - 1] where P=loan amount, r=monthly rate, n=total payments",
            "examples": ["$400,000 home, $80,000 down, 5% rate, 30 years → $1,718/month"],
            "use_cases": ["Home buying", "Refinancing decisions", "Budget planning", "Real estate investment", "Affordability analysis"],
            "key_features": [
                "Standard mortgage industry calculations",
                "Accounts for down payment automatically",
                "Works with any loan term and interest rate",
                "Essential for home buying decisions",
                "Helps determine affordability limits"
            ]
        },
        
        "retirement": {
            "description": "Calculate how much you need to save monthly to reach your retirement goals.",
            "usage": [
                "Enter your current age",
                "Enter desired retirement age", 
                "Enter monthly savings amount",
                "Enter expected annual return rate",
                "See your projected retirement savings"
            ],
            "formula": "Future Value = Monthly Payment × [((1 + r)^n - 1) / r] where r=monthly rate, n=number of payments",
            "examples": ["Age 25, retire at 65, save $500/month at 7% return → $1.37 million at retirement"],
            "use_cases": ["Retirement planning", "Financial goal setting", "Investment strategy", "Long-term savings", "Financial independence"]
        },
        
        "investment_return": {
            "description": "Calculate the future value of your investments based on initial amount and growth rate.",
            "usage": [
                "Enter your initial investment amount",
                "Enter expected annual return rate",
                "Enter investment time period in years",
                "See projected future value and total returns"
            ],
            "formula": "Future Value = Initial Investment × (1 + Annual Rate)^Years",
            "examples": ["$10,000 invested at 8% annual return for 20 years → $46,610 (gain: $36,610)"],
            "use_cases": ["Investment planning", "Portfolio analysis", "Financial forecasting", "Wealth building", "Goal setting"]
        },
        
        "savings_goal": {
            "description": "Calculate how much you need to save monthly to reach a specific financial goal.",
            "usage": [
                "Enter your savings goal amount",
                "Enter expected interest rate (if any)",
                "Enter time frame in months",
                "Get required monthly savings amount"
            ],
            "formula": "Monthly Savings = Goal Amount × r / [(1 + r)^n - 1] where r=monthly rate, n=months",
            "examples": ["Save $20,000 in 3 years at 4% interest → $509/month needed"],
            "use_cases": ["Emergency fund", "Vacation planning", "Major purchases", "Education savings", "Financial goals"]
        },
        
        "ideal_weight": {
            "description": "Calculate your ideal body weight based on height and gender using medical formulas.",
            "usage": [
                "Enter your height in centimeters",
                "Select your gender",
                "Get ideal weight range in kg and pounds"
            ],
            "formula": "Men: 50 + 2.3 × (height in inches - 60), Women: 45.5 + 2.3 × (height in inches - 60)",
            "examples": ["Male, 175cm height → Ideal weight: ~70kg (154 lbs)"],
            "use_cases": ["Health assessment", "Weight management", "Fitness goals", "Medical reference", "Wellness planning"]
        },
        
        "water_intake": {
            "description": "Calculate your daily water intake needs based on body weight and activity level.",
            "usage": [
                "Enter your body weight in kilograms",
                "Enter daily exercise duration in hours",
                "Get recommended daily water intake in liters and ounces"
            ],
            "formula": "Base Water = Weight × 0.033 liters, Additional = Exercise Hours × 0.5 liters",
            "examples": ["70kg person with 1 hour exercise → 2.8 liters (95 oz) daily"],
            "use_cases": ["Health maintenance", "Fitness planning", "Athletic training", "Wellness tracking", "Hydration goals"]
        },
        
        "heart_rate": {
            "description": "Calculate your maximum heart rate and target heart rate zones for exercise.",
            "usage": [
                "Enter your age in years",
                "Get maximum heart rate and training zones",
                "Use for cardio exercise planning"
            ],
            "formula": "Max HR = 220 - Age, Target Zone = 50-85% of Max HR",
            "examples": ["Age 30 → Max HR: 190 bpm, Target Zone: 95-162 bpm"],
            "use_cases": ["Cardio training", "Fitness monitoring", "Exercise planning", "Health tracking", "Athletic performance"]
        },
        
        "protein_needs": {
            "description": "Calculate your daily protein requirements based on weight and activity level.",
            "usage": [
                "Enter your body weight in kilograms",
                "Select your activity level (sedentary to athlete)",
                "Get daily protein needs in grams"
            ],
            "formula": "Protein = Weight × Activity Multiplier (0.8-2.0g per kg)",
            "examples": ["70kg moderately active person → 84g protein daily"],
            "use_cases": ["Nutrition planning", "Fitness goals", "Muscle building", "Diet planning", "Health optimization"]
        },
        
        "calories_burned": {
            "description": "Estimate calories burned during various physical activities and exercises.",
            "usage": [
                "Enter your body weight in kilograms",
                "Enter exercise duration in minutes",
                "Select activity intensity level",
                "Get estimated calories burned"
            ],
            "formula": "Calories = MET Value × Weight (kg) × Duration (hours)",
            "examples": ["70kg person, 45 min moderate cycling → ~315 calories burned"],
            "use_cases": ["Weight loss planning", "Fitness tracking", "Exercise monitoring", "Diet balancing", "Health goals"]
        },
        
        "quadratic": {
            "description": "Solve quadratic equations of the form ax² + bx + c = 0 using the quadratic formula.",
            "usage": [
                "Enter coefficient 'a' (cannot be zero)",
                "Enter coefficient 'b'",
                "Enter coefficient 'c'",
                "Get both solutions (real or complex)"
            ],
            "formula": "x = [-b ± √(b² - 4ac)] / 2a",
            "examples": ["2x² + 5x - 3 = 0 → x = 0.5 or x = -3"],
            "use_cases": ["Algebra homework", "Engineering calculations", "Physics problems", "Mathematical modeling", "Academic research"]
        },
        
        "distance": {
            "description": "Calculate the distance between two points in a coordinate plane.",
            "usage": [
                "Enter coordinates of first point (x1, y1)",
                "Enter coordinates of second point (x2, y2)",
                "Get the straight-line distance between points"
            ],
            "formula": "Distance = √[(x2-x1)² + (y2-y1)²]",
            "examples": ["Point (0,0) to (3,4) → Distance: 5 units"],
            "use_cases": ["Geometry problems", "Navigation", "Engineering", "Computer graphics", "Surveying"]
        },
        
        "slope": {
            "description": "Calculate the slope of a line passing through two points.",
            "usage": [
                "Enter coordinates of first point (x1, y1)",
                "Enter coordinates of second point (x2, y2)",
                "Get the slope (rise over run)"
            ],
            "formula": "Slope = (y2 - y1) / (x2 - x1)",
            "examples": ["Points (1,2) and (3,8) → Slope: 3"],
            "use_cases": ["Algebra problems", "Engineering", "Architecture", "Road construction", "Mathematical analysis"]
        },
        
        "gcd": {
            "description": "Find the Greatest Common Divisor (GCD) of two integers.",
            "usage": [
                "Enter the first integer",
                "Enter the second integer",
                "Get the largest number that divides both"
            ],
            "formula": "Uses Euclidean algorithm for efficient calculation",
            "examples": ["GCD of 48 and 18 → 6"],
            "use_cases": ["Number theory", "Fraction simplification", "Programming", "Mathematical proofs", "Cryptography"]
        },
        
        "lcm": {
            "description": "Find the Least Common Multiple (LCM) of two integers.",
            "usage": [
                "Enter the first integer",
                "Enter the second integer", 
                "Get the smallest positive number divisible by both"
            ],
            "formula": "LCM = |a × b| / GCD(a,b)",
            "examples": ["LCM of 12 and 18 → 36"],
            "use_cases": ["Fraction operations", "Scheduling problems", "Number theory", "Mathematical calculations", "Programming"]
        },
        
        "binary": {
            "description": "Convert decimal numbers to binary (base-2) representation.",
            "usage": [
                "Enter a decimal number (positive integer)",
                "Get the binary equivalent",
                "Useful for computer science and programming"
            ],
            "formula": "Repeatedly divide by 2 and collect remainders",
            "examples": ["Decimal 25 → Binary: 11001"],
            "use_cases": ["Computer science", "Programming", "Digital electronics", "Data representation", "Binary arithmetic"]
        },
        
        "hex": {
            "description": "Convert decimal numbers to hexadecimal (base-16) representation.",
            "usage": [
                "Enter a decimal number",
                "Get hexadecimal equivalent",
                "Uses digits 0-9 and letters A-F"
            ],
            "formula": "Repeatedly divide by 16 and collect remainders",
            "examples": ["Decimal 255 → Hexadecimal: FF"],
            "use_cases": ["Programming", "Web development", "Color codes", "Memory addresses", "Computer systems"]
        },
        
        "prime_check": {
            "description": "Check if a number is prime (only divisible by 1 and itself).",
            "usage": [
                "Enter any positive integer",
                "Get result: prime or not prime",
                "Includes explanation for composite numbers"
            ],
            "formula": "Tests divisibility up to √n for efficiency",
            "examples": ["17 is prime", "15 is not prime (divisible by 3 and 5)"],
            "use_cases": ["Number theory", "Cryptography", "Mathematical research", "Programming", "Security algorithms"]
        },
        
        "roman_numeral": {
            "description": "Convert numbers between decimal and Roman numeral systems.",
            "usage": [
                "Enter a number between 1 and 3999",
                "Get Roman numeral equivalent",
                "Uses standard Roman numeral rules"
            ],
            "formula": "Uses place values: M=1000, D=500, C=100, L=50, X=10, V=5, I=1",
            "examples": ["1994 → MCMXCIV", "2023 → MMXXIII"],
            "use_cases": ["Historical dates", "Clock faces", "Book chapters", "Movie sequels", "Formal documents"]
        },
        
        # More Date & Time Calculators
        "next_birthday": {
            "description": "Calculate how many days until your next birthday celebration.",
            "usage": [
                "Enter your birth date (month and day)",
                "Get exact days remaining until next birthday",
                "Perfect for birthday planning and countdowns"
            ],
            "formula": "Days = Next Birthday Date - Current Date",
            "examples": ["Born July 15th, today is March 10th → 127 days until next birthday"],
            "use_cases": ["Birthday planning", "Event countdowns", "Party preparation", "Gift shopping reminders", "Age milestones"]
        },
        
        "work_days": {
            "description": "Calculate the number of working days (excluding weekends) between two dates.",
            "usage": [
                "Enter start date",
                "Enter end date",
                "Get total weekdays (Monday-Friday) between dates"
            ],
            "formula": "Counts only Monday through Friday, excludes Saturday and Sunday",
            "examples": ["Jan 1 to Jan 31, 2025 → 23 working days"],
            "use_cases": ["Project planning", "Payroll calculations", "Business scheduling", "Deadline planning", "Work time tracking"]
        },
        
        "countdown": {
            "description": "Count down days, hours, and minutes to any future event or deadline.",
            "usage": [
                "Enter target date and time",
                "Get countdown in days, hours, minutes",
                "Perfect for event planning and deadlines"
            ],
            "formula": "Time Remaining = Target DateTime - Current DateTime",
            "examples": ["New Year 2026 → 341 days, 15 hours, 23 minutes remaining"],
            "use_cases": ["Event planning", "Project deadlines", "Holiday countdowns", "Launch dates", "Important milestones"]
        },
        
        # More Unit Conversion Calculators
        "unit_volume": {
            "description": "Convert between different volume measurements including liters, gallons, cups, and more.",
            "usage": [
                "Enter volume value",
                "Select source unit (liters, gallons, cups, etc.)",
                "Select target unit",
                "Get precise conversion"
            ],
            "formula": "Converts through liter base unit: 1 gallon = 3.78541 liters",
            "examples": ["5 gallons = 18.93 liters = 20 quarts"],
            "use_cases": ["Cooking recipes", "Fuel calculations", "Chemical mixing", "Container sizing", "International trade"]
        },
        
        "unit_speed": {
            "description": "Convert speed between different units like mph, km/h, m/s, and knots.",
            "usage": [
                "Enter speed value",
                "Select source unit (mph, km/h, m/s, knots)",
                "Select target unit",
                "Get accurate speed conversion"
            ],
            "formula": "Base conversion: 1 m/s = 3.6 km/h = 2.237 mph",
            "examples": ["60 mph = 96.56 km/h = 26.82 m/s"],
            "use_cases": ["Travel planning", "Vehicle specifications", "Weather data", "Sports analysis", "Aviation"]
        },
        
        # More Physics Calculators
        "acceleration": {
            "description": "Calculate acceleration from velocity change and time, or find missing values.",
            "usage": [
                "Enter initial velocity (m/s)",
                "Enter final velocity (m/s)",
                "Enter time period (seconds)",
                "Get acceleration in m/s²"
            ],
            "formula": "Acceleration = (Final Velocity - Initial Velocity) / Time",
            "examples": ["Car accelerates from 0 to 30 m/s in 10 seconds → 3 m/s² acceleration"],
            "use_cases": ["Physics problems", "Vehicle performance", "Engineering design", "Motion analysis", "Safety calculations"]
        },
        
        "kinetic_energy": {
            "description": "Calculate the kinetic energy of moving objects based on mass and velocity.",
            "usage": [
                "Enter object mass in kilograms",
                "Enter velocity in meters per second",
                "Get kinetic energy in Joules"
            ],
            "formula": "KE = ½ × mass × velocity²",
            "examples": ["2kg object moving at 10 m/s → KE = 100 Joules"],
            "use_cases": ["Physics calculations", "Engineering design", "Safety analysis", "Energy studies", "Collision analysis"]
        },
        
        "potential_energy": {
            "description": "Calculate gravitational potential energy based on mass, height, and gravity.",
            "usage": [
                "Enter object mass in kilograms",
                "Enter height in meters",
                "Get potential energy in Joules"
            ],
            "formula": "PE = mass × gravity × height (g = 9.81 m/s²)",
            "examples": ["5kg object at 10m height → PE = 490.5 Joules"],
            "use_cases": ["Physics problems", "Engineering calculations", "Energy analysis", "Safety planning", "Mechanical design"]
        },
        
        "momentum": {
            "description": "Calculate momentum of moving objects using mass and velocity.",
            "usage": [
                "Enter object mass in kilograms",
                "Enter velocity in m/s",
                "Get momentum in kg⋅m/s"
            ],
            "formula": "Momentum = mass × velocity",
            "examples": ["10kg object at 5 m/s → Momentum = 50 kg⋅m/s"],
            "use_cases": ["Physics problems", "Collision analysis", "Sports science", "Engineering", "Motion studies"]
        },
        
        # More Education Calculators
        "cgpa": {
            "description": "Calculate Cumulative Grade Point Average from multiple semester GPAs.",
            "usage": [
                "Enter GPA values for each semester",
                "Separate multiple GPAs with commas",
                "Get overall CGPA on 4.0 scale"
            ],
            "formula": "CGPA = Sum of all GPAs / Number of semesters",
            "examples": ["Semester GPAs: 3.5, 3.8, 3.2, 3.9 → CGPA: 3.6"],
            "use_cases": ["Academic tracking", "College applications", "Scholarship eligibility", "Graduate school", "Academic planning"]
        },
        
        "test_score": {
            "description": "Calculate test score percentage from correct answers and total questions.",
            "usage": [
                "Enter number of correct answers",
                "Enter total number of questions",
                "Get percentage score and letter grade"
            ],
            "formula": "Score = (Correct Answers / Total Questions) × 100",
            "examples": ["85 correct out of 100 questions → 85% (B grade)"],
            "use_cases": ["Test grading", "Quiz scoring", "Exam evaluation", "Academic assessment", "Performance tracking"]
        },
        
        "final_grade": {
            "description": "Calculate what grade you need on the final exam to achieve your desired course grade.",
            "usage": [
                "Enter your current grade percentage",
                "Enter desired final grade",
                "Enter final exam weight percentage",
                "Get required final exam score"
            ],
            "formula": "Required = (Desired - Current × (100 - Weight)) / Weight",
            "examples": ["Current: 78%, Want: 85%, Final worth 30% → Need 101.3% (not achievable)"],
            "use_cases": ["Academic planning", "Grade management", "Study prioritization", "Course strategy", "Goal setting"]
        },
        
        # More Home & DIY Calculators
        "concrete": {
            "description": "Calculate how much concrete you need for your construction project.",
            "usage": [
                "Enter length, width, and thickness",
                "Get concrete volume in cubic yards/meters",
                "Includes waste factor recommendations"
            ],
            "formula": "Volume = Length × Width × Thickness, add 10% waste factor",
            "examples": ["10×12 ft slab, 4 inches thick → 1.48 cubic yards needed"],
            "use_cases": ["Foundation work", "Driveways", "Sidewalks", "Patios", "Construction projects"]
        },
        
        "tile_needed": {
            "description": "Calculate how many tiles you need for flooring or wall projects.",
            "usage": [
                "Enter room dimensions",
                "Enter tile size",
                "Add waste percentage",
                "Get total tiles needed"
            ],
            "formula": "Tiles = (Room Area / Tile Area) × (1 + Waste Factor)",
            "examples": ["12×10 room with 12×12 inch tiles + 10% waste → 110 tiles"],
            "use_cases": ["Bathroom renovation", "Kitchen backsplash", "Floor tiling", "Wall decoration", "Home improvement"]
        },
        
        # More Statistics Calculators
        "standard_deviation": {
            "description": "Calculate standard deviation to measure data spread and variability.",
            "usage": [
                "Enter data values separated by commas",
                "Get standard deviation and variance",
                "Shows population and sample calculations"
            ],
            "formula": "σ = √[Σ(x - μ)² / N] for population",
            "examples": ["Data: 2, 4, 6, 8, 10 → Standard Deviation: 2.83"],
            "use_cases": ["Data analysis", "Quality control", "Research", "Statistics", "Performance measurement"]
        },
        
        "variance": {
            "description": "Calculate variance to measure how spread out data points are from the mean.",
            "usage": [
                "Enter numerical data separated by commas",
                "Get variance value",
                "Choose population or sample variance"
            ],
            "formula": "Variance = Σ(x - mean)² / N",
            "examples": ["Data: 1, 3, 5, 7, 9 → Variance: 8"],
            "use_cases": ["Statistical analysis", "Data science", "Quality control", "Research", "Risk assessment"]
        },
        
        # More Automotive Calculators
        "car_loan": {
            "description": "Calculate monthly payments for auto loans including interest and principal.",
            "usage": [
                "Enter car price",
                "Enter down payment",
                "Enter interest rate and loan term",
                "Get monthly payment amount"
            ],
            "formula": "Payment = [P × r(1+r)^n] / [(1+r)^n - 1]",
            "examples": ["$25,000 car, $5,000 down, 6% for 5 years → $386.66/month"],
            "use_cases": ["Car buying", "Budget planning", "Loan comparison", "Financial planning", "Auto financing"]
        },
        
        "tire_size": {
            "description": "Calculate tire dimensions and specifications from tire size codes.",
            "usage": [
                "Enter tire size code (e.g., 225/60R16)",
                "Get width, sidewall height, diameter",
                "Compare different tire sizes"
            ],
            "formula": "Sidewall Height = Width × Aspect Ratio / 100",
            "examples": ["225/60R16 → Width: 225mm, Sidewall: 135mm, Wheel: 16 inches"],
            "use_cases": ["Tire shopping", "Vehicle modification", "Performance tuning", "Replacement planning", "Size comparison"]
        },
        
        # REMAINING DATE & TIME CALCULATORS
        "age_difference": {
            "description": "Calculate the age difference between two people or the time span between two dates.",
            "usage": [
                "Enter the first person's birth date",
                "Enter the second person's birth date",
                "Get the age difference in years, months, and days"
            ],
            "formula": "Age Difference = |Date1 - Date2| calculated in years, months, and days",
            "examples": ["Person A born Jan 15, 1990 and Person B born Mar 22, 1985 → 4 years, 10 months, 7 days difference"],
            "use_cases": ["Relationship planning", "Sibling age gaps", "Historical comparisons", "Legal age requirements", "Family planning"]
        },
        
        "time_zone": {
            "description": "Convert time between different time zones around the world.",
            "usage": [
                "Enter the time in the source time zone",
                "Select source time zone offset",
                "Select target time zone offset",
                "Get converted time"
            ],
            "formula": "New Time = Original Time + (Target Offset - Source Offset)",
            "examples": ["2:00 PM EST (UTC-5) → 8:00 PM GMT (UTC+0)"],
            "use_cases": ["International meetings", "Travel planning", "Global business", "Online events", "Communication scheduling"]
        },
        
        # REMAINING HEALTH CALCULATORS
        "alcohol_units": {
            "description": "Calculate alcohol units in drinks to monitor safe consumption levels.",
            "usage": [
                "Enter drink volume in milliliters",
                "Enter alcohol by volume (ABV) percentage",
                "Get total alcohol units consumed"
            ],
            "formula": "Alcohol Units = (Volume in ml × ABV%) / 1000",
            "examples": ["500ml beer at 5% ABV → 2.5 alcohol units"],
            "use_cases": ["Health monitoring", "Safe drinking guidelines", "Medical consultations", "Designated driver planning", "Alcohol awareness"]
        },
        
        "body_fat": {
            "description": "Estimate body fat percentage using height, weight, and waist measurements.",
            "usage": [
                "Enter your height in centimeters",
                "Enter your weight in kilograms",
                "Enter waist circumference",
                "Select gender for accurate calculation"
            ],
            "formula": "Men: 64 - (20 × height/waist), Women: 76 - (20 × height/waist)",
            "examples": ["Male: 180cm height, 85cm waist → ~26% body fat"],
            "use_cases": ["Fitness tracking", "Health assessment", "Weight loss monitoring", "Athletic performance", "Medical evaluation"]
        },
        
        "carbs_needs": {
            "description": "Calculate daily carbohydrate requirements based on weight and activity level.",
            "usage": [
                "Enter your body weight in kilograms",
                "Select your activity level",
                "Get recommended daily carb intake in grams"
            ],
            "formula": "Carbs = Weight × Activity Multiplier (3-10g per kg)",
            "examples": ["70kg moderately active person → 350g carbs daily"],
            "use_cases": ["Athletic nutrition", "Diet planning", "Diabetes management", "Weight management", "Performance optimization"]
        },
        
        "fiber_needs": {
            "description": "Calculate daily fiber requirements based on age and gender for optimal digestive health.",
            "usage": [
                "Enter your age in years",
                "Select your gender",
                "Get recommended daily fiber intake"
            ],
            "formula": "Men <50: 38g, Men 50+: 30g, Women <50: 25g, Women 50+: 21g",
            "examples": ["35-year-old male → 38g fiber daily"],
            "use_cases": ["Digestive health", "Diet planning", "Nutrition counseling", "Health optimization", "Medical dietary requirements"]
        },
        
        "sleep_hours": {
            "description": "Calculate sleep duration and sleep cycles based on bedtime and wake time.",
            "usage": [
                "Enter your bedtime (24-hour format)",
                "Enter your wake time",
                "Get total sleep hours and number of sleep cycles"
            ],
            "formula": "Sleep Duration = Wake Time - Bedtime, Sleep Cycles = Duration / 1.5 hours",
            "examples": ["Bedtime 10:30 PM, Wake 6:30 AM → 8 hours sleep, 5.3 cycles"],
            "use_cases": ["Sleep optimization", "Health tracking", "Circadian rhythm management", "Performance improvement", "Wellness planning"]
        },
        
        # REMAINING FINANCE CALCULATORS
        "currency_converter": {
            "description": "Convert amounts between different currencies using current exchange rates.",
            "usage": [
                "Enter the amount to convert",
                "Enter source currency exchange rate",
                "Enter target currency exchange rate",
                "Get converted amount"
            ],
            "formula": "Converted Amount = (Amount / Source Rate) × Target Rate",
            "examples": ["$100 USD to EUR (rate 0.85) → €85"],
            "use_cases": ["International travel", "Online shopping", "Business transactions", "Investment planning", "Currency trading"]
        },
        
        "lease_vs_buy": {
            "description": "Compare the financial benefits of leasing versus buying a vehicle.",
            "usage": [
                "Enter vehicle purchase price",
                "Enter lease terms and monthly payment",
                "Enter loan terms and interest rate",
                "Compare total costs over time"
            ],
            "formula": "Total Cost = Down Payment + (Monthly Payment × Term) + Fees",
            "examples": ["$30,000 car: Buy $450/month vs Lease $350/month → Analysis shows best option"],
            "use_cases": ["Car shopping", "Financial planning", "Budget optimization", "Vehicle decisions", "Cost analysis"]
        },
        
        # REMAINING MATH CALCULATORS
        "area_trapezoid": {
            "description": "Calculate the area of a trapezoid using parallel sides and height.",
            "usage": [
                "Enter length of first parallel side (base1)",
                "Enter length of second parallel side (base2)",
                "Enter height (perpendicular distance between bases)",
                "Get area in square units"
            ],
            "formula": "Area = ½ × (base1 + base2) × height",
            "examples": ["Trapezoid: base1=8, base2=12, height=5 → Area: 50 square units"],
            "use_cases": ["Geometry problems", "Land surveying", "Construction planning", "Engineering design", "Architecture"]
        },
        
        "volume_cube": {
            "description": "Calculate the volume of a cube using the length of one side.",
            "usage": [
                "Enter the length of one side of the cube",
                "Get volume in cubic units",
                "Perfect for cubic containers and storage"
            ],
            "formula": "Volume = side³ (side × side × side)",
            "examples": ["Cube with 4-unit sides → Volume: 64 cubic units"],
            "use_cases": ["Storage calculations", "Packaging design", "Construction", "3D modeling", "Container sizing"]
        },
        
        "combination": {
            "description": "Calculate combinations (nCr) - number of ways to choose r items from n items without regard to order.",
            "usage": [
                "Enter total number of items (n)",
                "Enter number of items to choose (r)",
                "Get number of possible combinations"
            ],
            "formula": "C(n,r) = n! / (r! × (n-r)!)",
            "examples": ["Choose 3 items from 10 → C(10,3) = 120 combinations"],
            "use_cases": ["Probability calculations", "Statistics", "Lottery analysis", "Game theory", "Research design"]
        },
        
        "permutation": {
            "description": "Calculate permutations (nPr) - number of ways to arrange r items from n items where order matters.",
            "usage": [
                "Enter total number of items (n)",
                "Enter number of items to arrange (r)",
                "Get number of possible arrangements"
            ],
            "formula": "P(n,r) = n! / (n-r)!",
            "examples": ["Arrange 3 items from 10 → P(10,3) = 720 permutations"],
            "use_cases": ["Probability theory", "Combinatorics", "Password combinations", "Scheduling", "Competition rankings"]
        },
        
        "fibonacci": {
            "description": "Generate the Fibonacci sequence up to n terms where each number is the sum of the two preceding ones.",
            "usage": [
                "Enter the number of terms to generate",
                "Get the complete Fibonacci sequence",
                "Sequence starts with 0, 1, 1, 2, 3, 5..."
            ],
            "formula": "F(n) = F(n-1) + F(n-2), starting with F(0)=0, F(1)=1",
            "examples": ["First 8 terms → 0, 1, 1, 2, 3, 5, 8, 13"],
            "use_cases": ["Mathematical education", "Algorithm studies", "Pattern recognition", "Nature studies", "Programming practice"]
        },
        
        "random_number": {
            "description": "Generate random numbers within a specified range for various applications.",
            "usage": [
                "Enter minimum value",
                "Enter maximum value",
                "Click generate to get a random number",
                "Perfect for games, sampling, and simulations"
            ],
            "formula": "Random integer between min and max (inclusive)",
            "examples": ["Range 1-100 → Random number: 47"],
            "use_cases": ["Games and contests", "Statistical sampling", "Password generation", "Decision making", "Simulations"]
        },
        
        "octal": {
            "description": "Convert decimal numbers to octal (base-8) number system.",
            "usage": [
                "Enter a decimal number",
                "Get octal equivalent using digits 0-7",
                "Useful for computer science applications"
            ],
            "formula": "Repeatedly divide by 8 and collect remainders",
            "examples": ["Decimal 64 → Octal: 100"],
            "use_cases": ["Computer programming", "Digital systems", "File permissions", "Number system education", "Data representation"]
        },
        
        "mode": {
            "description": "Find the mode (most frequently occurring value) in a dataset.",
            "usage": [
                "Enter numbers separated by commas",
                "Get the most frequent value(s)",
                "Shows frequency count for each value"
            ],
            "formula": "Mode = value(s) that appear most frequently in the dataset",
            "examples": ["Data: 1,2,2,3,3,3,4 → Mode: 3 (appears 3 times)"],
            "use_cases": ["Statistical analysis", "Data interpretation", "Quality control", "Survey analysis", "Research studies"]
        },
        
        "correlation": {
            "description": "Calculate correlation coefficient to measure the strength of relationship between two datasets.",
            "usage": [
                "Enter first dataset (x values)",
                "Enter second dataset (y values)",
                "Get correlation coefficient (-1 to +1)"
            ],
            "formula": "r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)²Σ(yi - ȳ)²]",
            "examples": ["Strong positive correlation: r = 0.85"],
            "use_cases": ["Data analysis", "Research studies", "Business intelligence", "Scientific research", "Predictive modeling"]
        },
        
        # REMAINING PHYSICS CALCULATORS
        "density": {
            "description": "Calculate density of materials and objects using mass and volume measurements.",
            "usage": [
                "Enter mass in kilograms",
                "Enter volume in cubic meters",
                "Get density in kg/m³"
            ],
            "formula": "Density = Mass / Volume",
            "examples": ["2kg object with 0.5m³ volume → Density: 4 kg/m³"],
            "use_cases": ["Material science", "Engineering design", "Quality control", "Physics problems", "Manufacturing"]
        },
        
        "power_physics": {
            "description": "Calculate power in physics - the rate of energy transfer or work done per unit time.",
            "usage": [
                "Enter work done in Joules",
                "Enter time taken in seconds",
                "Get power output in Watts"
            ],
            "formula": "Power = Work / Time = Energy / Time",
            "examples": ["1000 Joules of work in 10 seconds → Power: 100 Watts"],
            "use_cases": ["Electrical engineering", "Mechanical systems", "Energy efficiency", "Motor specifications", "Physics calculations"]
        },
        
        "pressure_physics": {
            "description": "Calculate pressure exerted by force over an area.",
            "usage": [
                "Enter applied force in Newtons",
                "Enter contact area in square meters",
                "Get pressure in Pascals"
            ],
            "formula": "Pressure = Force / Area",
            "examples": ["100N force over 0.1m² area → Pressure: 1000 Pa"],
            "use_cases": ["Engineering design", "Hydraulic systems", "Material testing", "Safety calculations", "Physics problems"]
        },
        
        "work": {
            "description": "Calculate work done when a force moves an object through a distance.",
            "usage": [
                "Enter applied force in Newtons",
                "Enter distance moved in meters",
                "Enter angle between force and motion",
                "Get work done in Joules"
            ],
            "formula": "Work = Force × Distance × cos(angle)",
            "examples": ["50N force moving object 10m → Work: 500 Joules"],
            "use_cases": ["Physics problems", "Engineering calculations", "Energy analysis", "Mechanical systems", "Efficiency studies"]
        },
        
        # REMAINING UNIT CONVERSION CALCULATORS
        "area-converter": {
            "description": "Convert between different area measurements including square meters, feet, acres, and hectares.",
            "usage": [
                "Enter area value",
                "Select source unit (sq m, sq ft, acres, etc.)",
                "Select target unit",
                "Get precise area conversion"
            ],
            "formula": "Converts through square meter base: 1 acre = 4,047 sq meters",
            "examples": ["1 acre = 4,047 sq meters = 43,560 sq feet"],
            "use_cases": ["Real estate", "Land surveying", "Construction planning", "Agriculture", "Property management"]
        },
        
        "unit_energy": {
            "description": "Convert between different energy units including Joules, calories, kWh, and BTU.",
            "usage": [
                "Enter energy value",
                "Select source unit (Joules, calories, kWh, BTU)",
                "Select target unit",
                "Get energy conversion"
            ],
            "formula": "Base conversion: 1 kWh = 3.6 million Joules = 860 kcal",
            "examples": ["1 kWh = 3,600,000 Joules = 3,412 BTU"],
            "use_cases": ["Energy billing", "Engineering calculations", "Nutrition analysis", "HVAC systems", "Scientific research"]
        },
        
        "unit_power": {
            "description": "Convert between different power units including Watts, horsepower, and BTU/hour.",
            "usage": [
                "Enter power value",
                "Select source unit (Watts, HP, BTU/hr)",
                "Select target unit",
                "Get power conversion"
            ],
            "formula": "Base conversion: 1 HP = 746 Watts = 2,545 BTU/hr",
            "examples": ["100 HP = 74,600 Watts = 254,500 BTU/hr"],
            "use_cases": ["Motor specifications", "HVAC sizing", "Vehicle performance", "Industrial equipment", "Energy systems"]
        },
        
        "unit_pressure": {
            "description": "Convert between different pressure units including Pascals, PSI, bar, and atmospheres.",
            "usage": [
                "Enter pressure value",
                "Select source unit (Pa, PSI, bar, atm)",
                "Select target unit",
                "Get pressure conversion"
            ],
            "formula": "Base conversion: 1 atm = 101,325 Pa = 14.7 PSI = 1.01 bar",
            "examples": ["30 PSI = 206,843 Pa = 2.07 bar"],
            "use_cases": ["Tire pressure", "Hydraulic systems", "Weather data", "Engineering design", "Scientific measurements"]
        },
        
        "unit_time": {
            "description": "Convert between different time units from seconds to years.",
            "usage": [
                "Enter time value",
                "Select source unit (seconds, minutes, hours, days, weeks, years)",
                "Select target unit",
                "Get time conversion"
            ],
            "formula": "Base conversions: 1 day = 24 hours = 1,440 minutes = 86,400 seconds",
            "examples": ["1 week = 7 days = 168 hours = 604,800 seconds"],
            "use_cases": ["Project planning", "Scientific calculations", "Time management", "Data analysis", "International coordination"]
        },
        
        # REMAINING HOME & DIY CALCULATORS
        "electricity_cost": {
            "description": "Calculate electricity costs based on power consumption and utility rates.",
            "usage": [
                "Enter appliance power rating in Watts",
                "Enter hours of daily usage",
                "Enter electricity rate per kWh",
                "Get daily, monthly, and yearly costs"
            ],
            "formula": "Cost = (Power in kW × Hours × Rate per kWh) × Days",
            "examples": ["1500W heater, 8 hrs/day, $0.12/kWh → $1.44/day, $43.20/month"],
            "use_cases": ["Energy budgeting", "Appliance comparison", "Home efficiency", "Cost analysis", "Utility planning"]
        },
        
        "fence": {
            "description": "Calculate fencing materials needed for property boundaries and enclosures.",
            "usage": [
                "Enter perimeter length or property dimensions",
                "Enter fence height",
                "Select fence type and post spacing",
                "Get materials list and costs"
            ],
            "formula": "Materials = Perimeter / Post Spacing + Gates + Hardware",
            "examples": ["100ft perimeter, 6ft height, 8ft spacing → 13 posts, 100ft fencing"],
            "use_cases": ["Property fencing", "Garden enclosures", "Pet containment", "Privacy barriers", "Security fencing"]
        },
        
        "roofing": {
            "description": "Calculate roofing materials needed including shingles, underlayment, and accessories.",
            "usage": [
                "Enter roof dimensions and pitch",
                "Select roofing material type",
                "Add waste factor for cuts and overlaps",
                "Get complete materials list"
            ],
            "formula": "Area = Length × Width × Pitch Factor, Materials = Area × Coverage Rate",
            "examples": ["30×40 ft roof, 6/12 pitch → 1,342 sq ft area, 14 squares of shingles"],
            "use_cases": ["Roof replacement", "New construction", "Repair projects", "Cost estimation", "Contractor planning"]
        },
        
        "solar_panels": {
            "description": "Calculate solar panel requirements and energy production for your home.",
            "usage": [
                "Enter monthly electricity usage in kWh",
                "Enter available roof area",
                "Enter local sun hours per day",
                "Get panel count and system size"
            ],
            "formula": "System Size = Monthly Usage × 12 / (Sun Hours × 365 × Panel Efficiency)",
            "examples": ["1000 kWh/month, 5 sun hours → 20kW system, ~67 panels"],
            "use_cases": ["Solar installation", "Energy independence", "Cost savings", "Environmental impact", "Home improvement"]
        },
        
        # REMAINING COOKING CALCULATORS
        "cooking_time": {
            "description": "Adjust cooking times and temperatures for different portion sizes and oven types.",
            "usage": [
                "Enter original recipe cooking time",
                "Enter original and new portion sizes",
                "Select oven type adjustments",
                "Get adjusted cooking time and temperature"
            ],
            "formula": "New Time = Original Time × (New Size / Original Size)^0.67",
            "examples": ["Recipe for 4 people, 30 min → Recipe for 8 people, ~38 min"],
            "use_cases": ["Recipe scaling", "Meal planning", "Catering", "Baking adjustments", "Kitchen efficiency"]
        },
        
        "recipe_scaler": {
            "description": "Scale recipe ingredients up or down for different serving sizes.",
            "usage": [
                "Enter original recipe serving size",
                "Enter desired serving size",
                "Input ingredient quantities",
                "Get scaled ingredient amounts"
            ],
            "formula": "New Amount = Original Amount × (New Servings / Original Servings)",
            "examples": ["Recipe for 4 → Recipe for 10: 2 cups flour becomes 5 cups flour"],
            "use_cases": ["Meal planning", "Party cooking", "Batch cooking", "Restaurant portions", "Food service"]
        },
        
        "oven_temp": {
            "description": "Convert oven temperatures between Celsius, Fahrenheit, and gas mark settings.",
            "usage": [
                "Enter temperature value",
                "Select source unit (°C, °F, Gas Mark)",
                "Select target unit",
                "Get converted oven temperature"
            ],
            "formula": "°F = (°C × 9/5) + 32, Gas Mark approximations included",
            "examples": ["180°C = 356°F = Gas Mark 4"],
            "use_cases": ["International recipes", "Oven calibration", "Baking conversions", "Cooking guides", "Recipe adaptation"]
        },
        
        # REMAINING ENVIRONMENT CALCULATORS
        "carbon_footprint": {
            "description": "Calculate your carbon footprint from transportation, energy use, and lifestyle choices.",
            "usage": [
                "Enter transportation details (car, flights, etc.)",
                "Enter home energy consumption",
                "Enter lifestyle factors",
                "Get total CO2 emissions per year"
            ],
            "formula": "CO2 = Σ(Activity × Emission Factor) for all activities",
            "examples": ["10,000 miles driving + 2 flights + home energy → 12 tons CO2/year"],
            "use_cases": ["Environmental awareness", "Sustainability planning", "Carbon offsetting", "Lifestyle changes", "Corporate reporting"]
        },
        
        "recycling": {
            "description": "Calculate environmental impact and CO2 savings from recycling different materials.",
            "usage": [
                "Enter amounts of paper, plastic, glass, metal recycled",
                "Select time period (monthly, yearly)",
                "Get CO2 savings and environmental impact"
            ],
            "formula": "CO2 Saved = Σ(Material Weight × CO2 Factor per material)",
            "examples": ["10kg paper + 5kg plastic monthly → 45kg CO2 saved per year"],
            "use_cases": ["Environmental tracking", "Sustainability goals", "Waste management", "Corporate reporting", "Educational purposes"]
        },
        
        "tree_offset": {
            "description": "Calculate how many trees needed to offset your carbon emissions.",
            "usage": [
                "Enter annual CO2 emissions in tons",
                "Select tree type and growth conditions",
                "Get number of trees needed for offset"
            ],
            "formula": "Trees Needed = CO2 Emissions / Average CO2 Absorption per Tree",
            "examples": ["15 tons CO2 annually → Need to plant ~750 trees"],
            "use_cases": ["Carbon offsetting", "Reforestation planning", "Environmental projects", "Sustainability goals", "Climate action"]
        }
    }
    
    # Only return content for calculators that have specific content defined
    # This prevents auto-generated content that triggers AdSense violations
    return content_map.get(calc_id, None)

# Serve static sitemap and robots BEFORE any other routes
@app.route('/sitemap.xml')
def sitemap():
    """Generate dynamic sitemap based on calculator list"""

    pages = []

    # Base domain of your deployed site
    base_url = "https://clackmasterpro.online"

    # Add homepage
    pages.append({
        "loc": base_url,
        "lastmod": datetime.now().strftime("%Y-%m-%d")
    })

    # Add static pages
    static_pages = ["/guides", "/about", "/contact", "/privacy-policy", "/terms-and-conditions"]
    for page in static_pages:
        pages.append({
            "loc": f"{base_url}{page}",
            "lastmod": datetime.now().strftime("%Y-%m-%d")
        })

    # Add calculator URLs only for those with comprehensive content
    for calc in CALCULATORS:
        slug = calc.get("slug") or calc.get("id")
        content = get_calculator_content(calc['id'])
        if slug and content:  # Only include calculators with specific content
            pages.append({
                "loc": f"{base_url}/calculator/{slug}",
                "lastmod": datetime.now().strftime("%Y-%m-%d")
            })

    # Generate XML content
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for page in pages:
        xml.append("<url>")
        xml.append(f"<loc>{page['loc']}</loc>")
        xml.append(f"<lastmod>{page['lastmod']}</lastmod>")
        xml.append("<changefreq>weekly</changefreq>")
        xml.append("<priority>0.80</priority>")
        xml.append("</url>")

    xml.append("</urlset>")
    sitemap_xml = "\n".join(xml)

    return Response(sitemap_xml, mimetype="application/xml")


@app.route('/robots.txt')
def robots():
    return send_from_directory(app.root_path, 'robots.txt', mimetype='text/plain')

@app.route('/ads.txt')
def ads():
    return send_from_directory(app.root_path, 'ads.txt', mimetype='text/plain')
    #Temporarily disabled until AdSense approval

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
        
        # Education Calculators
        elif calc_id == "gpa":
            grades_str = data.get("grades", "")
            if not grades_str:
                return "Error: Please provide grades"
            grades = [g.strip().upper() for g in grades_str.split(",")]
            grade_points = {"A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
                           "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "F": 0.0}
            total = 0
            count = 0
            for grade in grades:
                if grade in grade_points:
                    total += grade_points[grade]
                    count += 1
            if count == 0:
                return "Error: No valid grades found"
            gpa = total / count
            return f"GPA: {gpa:.2f} (based on {count} grades)"
        
        elif calc_id == "cgpa":
            gpas_str = data.get("gpas", "")
            if not gpas_str:
                return "Error: Please provide GPAs"
            try:
                gpas = [float(g.strip()) for g in gpas_str.split(",")]
                cgpa = sum(gpas) / len(gpas)
                return f"CGPA: {cgpa:.2f} (average of {len(gpas)} semesters)"
            except ValueError:
                return "Error: Please provide valid numeric GPAs"
        
        elif calc_id == "grade":
            earned = float(data.get("earned"))
            total = float(data.get("total"))
            if total <= 0:
                return "Error: Total points must be greater than 0"
            percentage = (earned / total) * 100
            if percentage >= 90:
                letter = "A"
            elif percentage >= 80:
                letter = "B"
            elif percentage >= 70:
                letter = "C"
            elif percentage >= 60:
                letter = "D"
            else:
                letter = "F"
            return f"Grade: {percentage:.1f}% ({letter})"
        
        elif calc_id == "test_score":
            correct = int(float(data.get("correct")))
            total = int(float(data.get("total")))
            if total <= 0:
                return "Error: Total questions must be greater than 0"
            percentage = (correct / total) * 100
            return f"Score: {correct}/{total} = {percentage:.1f}%"
        
        elif calc_id == "final_grade":
            current = float(data.get("current"))
            desired = float(data.get("desired"))
            weight = float(data.get("weight"))
            if weight <= 0 or weight > 100:
                return "Error: Final exam weight must be between 0 and 100"
            needed = (desired - current * (100 - weight) / 100) / (weight / 100)
            if needed > 100:
                return f"Grade Needed: {needed:.1f}% (Not achievable - you need more than 100%)"
            elif needed < 0:
                return f"Grade Needed: 0% (You already have the desired grade!)"
            else:
                return f"Grade Needed on Final: {needed:.1f}%"
        
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
    # Only show calculators that have comprehensive content defined
    featured_calculators = []
    for calc in CALCULATORS:
        content = get_calculator_content(calc['id'])
        if content:  # Only include calculators with specific content
            featured_calculators.append(calc)
    
    return render_template("index.html", calculators=featured_calculators)

@app.route("/calculator/<slug>")
def calculator_page(slug):
    """Individual SEO-friendly page for each calculator
    Supports both slug (e.g., 'age-calculator') and id (e.g., 'age') for backward compatibility
    """
    # Find calculator by slug first, then by id for backward compatibility
    calc = next((c for c in CALCULATORS if c.get('slug') == slug or c.get('id') == slug), None)
    if not calc:
        return render_template("404.html"), 404
    
    # Redirect to canonical URL if accessed via non-canonical slug
    canonical_slug = calc.get('slug') or calc.get('id')
    if slug != canonical_slug:
        return redirect(url_for('calculator_page', slug=canonical_slug), 301)
    
    # Get specific content for this calculator
    calc_content = get_calculator_content(calc['id'])
    
    # If no content defined, return 404 to avoid thin content pages
    if not calc_content:
        return render_template("404.html"), 404
    
    # Only show calculators with content in related section
    related_calculators = []
    for c in CALCULATORS:
        if c.get('category') == calc.get('category') and c.get('id') != calc.get('id'):
            if get_calculator_content(c['id']):  # Only include if has content
                related_calculators.append(c)
    
    return render_template("calculator_page.html", calculator=calc, all_calculators=related_calculators, content=calc_content)

@app.route("/calculate", methods=["POST"])
def calculate_route():
    data = request.json
    calc_id = data.get("calc_id")
    result = calculate(calc_id, data.get("data", {}))
    return jsonify({"result": result})

@app.route("/guides")
def guides():
    # Add content for each calculator - only show calculators with defined content
    calculators_with_content = []
    for calc in CALCULATORS:
        content = get_calculator_content(calc['id'])
        if content:  # Only include calculators with specific content
            calc_with_content = calc.copy()
            calc_with_content['content'] = content
            calculators_with_content.append(calc_with_content)
    
    return render_template("guides.html", calculators=calculators_with_content)

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
