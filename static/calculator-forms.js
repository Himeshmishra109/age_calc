// Shared form generation logic for all 108 calculators
function generateFormHTML(calcId) {
    let html = '';
    
    // ==================== DATE & TIME CALCULATORS ====================
    if (calcId === 'age') {
            html += `
                <div class="form-group">
                    <label>Date of Birth:</label>
                    <input type="date" id="dob" required>
                </div>
            `;
        } else if (calcId === 'days_between') {
            html += `
                <div class="form-group">
                    <label>Start Date:</label>
                    <input type="date" id="date1" required>
                </div>
                <div class="form-group">
                    <label>End Date:</label>
                    <input type="date" id="date2" required>
                </div>
            `;
        } else if (calcId === 'bmi') {
            html += `
                <div class="form-group">
                    <label>Weight (kg):</label>
                    <input type="number" id="weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Height (cm):</label>
                    <input type="number" id="height" step="0.1" required>
                </div>
            `;
        } else if (calcId === 'simple_interest') {
            html += `
                <div class="form-group">
                    <label>Principal Amount ($):</label>
                    <input type="number" id="principal" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Interest Rate (%):</label>
                    <input type="number" id="rate" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Time (years):</label>
                    <input type="number" id="time" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'tip_calculator') {
            html += `
                <div class="form-group">
                    <label>Bill Amount ($):</label>
                    <input type="number" id="bill" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Tip Percentage (%):</label>
                    <input type="number" id="tip" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'area_circle') {
            html += `
                <div class="form-group">
                    <label>Radius:</label>
                    <input type="number" id="radius" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'percentage') {
            html += `
                <div class="form-group">
                    <label>Value:</label>
                    <input type="number" id="value" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Percentage:</label>
                    <input type="number" id="percent" step="0.01" required>
                </div>
            `;
        } 
        
            else if (calcId === 'area-converter') {
            html += `
                <div class="form-group">
                <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="fromUnit" required>
                <option value="sqm">Square Meter (m²)</option>
                <option value="sqcm">Square Centimeter (cm²)</option>
                <option value="sqkm">Square Kilometer (km²)</option>
                <option value="sqft">Square Feet (ft²)</option>
                <option value="sqin">Square Inch (in²)</option>
                <option value="sqyd">Square Yard (yd²)</option>
                <option value="acre">Acre</option>
                <option value="hectare">Hectare</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="toUnit" required>
                <option value="sqm">Square Meter (m²)</option>
                <option value="sqcm">Square Centimeter (cm²)</option>
                <option value="sqkm">Square Kilometer (km²)</option>
                <option value="sqft">Square Feet (ft²)</option>
                <option value="sqin">Square Inch (in²)</option>
                <option value="sqyd">Square Yard (yd²)</option>
                <option value="acre">Acre</option>
                <option value="hectare">Hectare</option>
            </select>
        </div>
    `;
}    
        else if (calcId === 'factorial') {
            html += `
                <div class="form-group">
                    <label>Number:</label>
                    <input type="number" id="n" min="0" max="170" required>
                </div>
            `;
        } else if (calcId === 'speed') {
            html += `
                <div class="form-group">
                    <label>Distance:</label>
                    <input type="number" id="distance" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Time:</label>
                    <input type="number" id="time" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'unit_temperature') {
            html += `
                <div class="form-group">
                    <label>Temperature:</label>
                    <input type="number" id="temp" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>From:</label>
                    <select id="from" required>
                        <option value="celsius">Celsius</option>
                        <option value="fahrenheit">Fahrenheit</option>
                        <option value="kelvin">Kelvin</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>To:</label>
                    <select id="to" required>
                        <option value="celsius">Celsius</option>
                        <option value="fahrenheit">Fahrenheit</option>
                        <option value="kelvin">Kelvin</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'compound_interest') {
            html += `
                <div class="form-group">
                    <label>Principal Amount ($):</label>
                    <input type="number" id="principal" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Interest Rate (%):</label>
                    <input type="number" id="rate" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Time (years):</label>
                    <input type="number" id="time" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Compounds per year:</label>
                    <input type="number" id="compounds" value="12" required>
                </div>
            `;
        } else if (calcId === 'loan_payment') {
            html += `
                <div class="form-group">
                    <label>Loan Amount ($):</label>
                    <input type="number" id="principal" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Annual Interest Rate (%):</label>
                    <input type="number" id="rate" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Loan Term (months):</label>
                    <input type="number" id="months" required>
                </div>
            `;
        } else if (calcId === 'area_rectangle') {
            html += `
                <div class="form-group">
                    <label>Length:</label>
                    <input type="number" id="length" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Width:</label>
                    <input type="number" id="width" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'area_triangle') {
            html += `
                <div class="form-group">
                    <label>Base:</label>
                    <input type="number" id="base" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Height:</label>
                    <input type="number" id="height" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'volume_sphere') {
            html += `
                <div class="form-group">
                    <label>Radius:</label>
                    <input type="number" id="radius" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'pythagorean') {
            html += `
                <div class="form-group">
                    <label>Side A (leave empty to calculate):</label>
                    <input type="number" id="a" step="0.01">
                </div>
                <div class="form-group">
                    <label>Side B (leave empty to calculate):</label>
                    <input type="number" id="b" step="0.01">
                </div>
                <div class="form-group">
                    <label>Hypotenuse C (leave empty to calculate):</label>
                    <input type="number" id="c" step="0.01">
                </div>
            `;
        } else if (calcId === 'bmr') {
            html += `
                <div class="form-group">
                    <label>Weight (kg):</label>
                    <input type="number" id="weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Height (cm):</label>
                    <input type="number" id="height" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Age:</label>
                    <input type="number" id="age" required>
                </div>
                <div class="form-group">
                    <label>Gender:</label>
                    <select id="gender" required>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'gpa') {
            html += `
                <div class="form-group">
                    <label>Total Grade Points:</label>
                    <input type="number" id="points" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Total Credit Hours:</label>
                    <input type="number" id="credits" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'force') {
            html += `
                <div class="form-group">
                    <label>Mass (kg):</label>
                    <input type="number" id="mass" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Acceleration (m/s²):</label>
                    <input type="number" id="acceleration" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'kinetic_energy') {
            html += `
                <div class="form-group">
                    <label>Mass (kg):</label>
                    <input type="number" id="mass" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Velocity (m/s):</label>
                    <input type="number" id="velocity" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'gcd') {
            html += `
                <div class="form-group">
                    <label>Number A:</label>
                    <input type="number" id="a" required>
                </div>
                <div class="form-group">
                    <label>Number B:</label>
                    <input type="number" id="b" required>
                </div>
            `;
        } else if (calcId === 'lcm') {
            html += `
                <div class="form-group">
                    <label>Number A:</label>
                    <input type="number" id="a" required>
                </div>
                <div class="form-group">
                    <label>Number B:</label>
                    <input type="number" id="b" required>
                </div>
            `;
        } else if (calcId === 'mean') {
            html += `
                <div class="form-group">
                    <label>Numbers (comma-separated):</label>
                    <input type="text" id="numbers" required>
                </div>
            `;
        } else if (calcId === 'fuel_efficiency') {
            html += `
                <div class="form-group">
                    <label>Distance (miles):</label>
                    <input type="number" id="distance" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Fuel Used (gallons):</label>
                    <input type="number" id="fuel" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'binary') {
            html += `
                <div class="form-group">
                    <label>Decimal Number:</label>
                    <input type="number" id="number" required>
                </div>
            `;
        } else if (calcId === 'hex') {
            html += `
                <div class="form-group">
                    <label>Decimal Number:</label>
                    <input type="number" id="number" required>
                </div>
            `;
        } else if (calcId === 'prime_check') {
            html += `
                <div class="form-group">
                    <label>Number:</label>
                    <input type="number" id="number" required>
                </div>
            `;
        } else if (calcId === 'fibonacci') {
            html += `
                <div class="form-group">
                    <label>Number of Terms:</label>
                    <input type="number" id="n" min="1" max="50" required>
                </div>
            `;
        } else if (calcId === 'random_number') {
            html += `
                <div class="form-group">
                    <label>Minimum:</label>
                    <input type="number" id="min" value="1" required>
                </div>
                <div class="form-group">
                    <label>Maximum:</label>
                    <input type="number" id="max" value="100" required>
                </div>
            `;
        } else if (calcId === 'date_add') {
            html += `
                <div class="form-group">
                    <label>Start Date:</label>
                    <input type="date" id="date" required>
                </div>
                <div class="form-group">
                    <label>Days to Add:</label>
                    <input type="number" id="days" required>
                </div>
            `;
        } else if (calcId === 'weekday') {
            html += `
                <div class="form-group">
                    <label>Date:</label>
                    <input type="date" id="date" required>
                </div>
            `;
        } else if (calcId === 'leap_year') {
            html += `
                <div class="form-group">
                    <label>Year:</label>
                    <input type="number" id="year" required>
                </div>
            `;
        } else if (calcId === 'median') {
            html += `
                <div class="form-group">
                    <label>Numbers (comma-separated):</label>
                    <input type="text" id="numbers" required>
                </div>
            `;
        } else if (calcId === 'mode') {
            html += `
                <div class="form-group">
                    <label>Numbers (comma-separated):</label>
                    <input type="text" id="numbers" required>
                </div>
            `;
        } else if (calcId === 'standard_deviation') {
            html += `
                <div class="form-group">
                    <label>Numbers (comma-separated):</label>
                    <input type="text" id="numbers" required>
                </div>
            `;
        } else if (calcId === 'variance') {
            html += `
                <div class="form-group">
                    <label>Numbers (comma-separated):</label>
                    <input type="text" id="numbers" required>
                </div>
            `;
        } else if (calcId === 'volume_cube') {
            html += `
                <div class="form-group">
                    <label>Side Length:</label>
                    <input type="number" id="side" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'volume_cylinder') {
            html += `
                <div class="form-group">
                    <label>Radius:</label>
                    <input type="number" id="radius" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Height:</label>
                    <input type="number" id="height" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'area_trapezoid') {
            html += `
                <div class="form-group">
                    <label>Base 1:</label>
                    <input type="number" id="base1" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Base 2:</label>
                    <input type="number" id="base2" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Height:</label>
                    <input type="number" id="height" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'quadratic') {
            html += `
                <div class="form-group">
                    <label>Coefficient a:</label>
                    <input type="number" id="a" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Coefficient b:</label>
                    <input type="number" id="b" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Coefficient c:</label>
                    <input type="number" id="c" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'permutation') {
            html += `
                <div class="form-group">
                    <label>Total Items (n):</label>
                    <input type="number" id="n" required>
                </div>
                <div class="form-group">
                    <label>Items to Choose (r):</label>
                    <input type="number" id="r" required>
                </div>
            `;
        } else if (calcId === 'combination') {
            html += `
                <div class="form-group">
                    <label>Total Items (n):</label>
                    <input type="number" id="n" required>
                </div>
                <div class="form-group">
                    <label>Items to Choose (r):</label>
                    <input type="number" id="r" required>
                </div>
            `;
        } else if (calcId === 'distance') {
            html += `
                <div class="form-group">
                    <label>Point 1 - X coordinate:</label>
                    <input type="number" id="x1" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Point 1 - Y coordinate:</label>
                    <input type="number" id="y1" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Point 2 - X coordinate:</label>
                    <input type="number" id="x2" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Point 2 - Y coordinate:</label>
                    <input type="number" id="y2" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'slope') {
            html += `
                <div class="form-group">
                    <label>Point 1 - X coordinate:</label>
                    <input type="number" id="x1" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Point 1 - Y coordinate:</label>
                    <input type="number" id="y1" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Point 2 - X coordinate:</label>
                    <input type="number" id="x2" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Point 2 - Y coordinate:</label>
                    <input type="number" id="y2" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'percentage_change') {
            html += `
                <div class="form-group">
                    <label>Old Value:</label>
                    <input type="number" id="old" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>New Value:</label>
                    <input type="number" id="new" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'percentage_of') {
            html += `
                <div class="form-group">
                    <label>Value:</label>
                    <input type="number" id="value" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Percentage:</label>
                    <input type="number" id="percent" step="0.01" required>
                </div>
            `;
        }  else if (calcId === 'investment_return') {
            html += `
                <div class="form-group">
                    <label>Principal ($):</label>
                    <input type="number" id="principal" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Annual Return Rate (%):</label>
                    <input type="number" id="rate" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Time (years):</label>
                    <input type="number" id="time" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'acceleration') {
            html += `
                <div class="form-group">
                    <label>Initial Velocity (m/s):</label>
                    <input type="number" id="initial_velocity" step="0.01" value="0" required>
                </div>
                <div class="form-group">
                    <label>Final Velocity (m/s):</label>
                    <input type="number" id="final_velocity" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Time (seconds):</label>
                    <input type="number" id="time" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'age_difference') {
            html += `
                <div class="form-group">
                    <label>First Date:</label>
                    <input type="date" id="date1" required>
                </div>
                <div class="form-group">
                    <label>Second Date:</label>
                    <input type="date" id="date2" required>
                </div>
            `;
        } else if (calcId === 'octal') {
            html += `
                <div class="form-group">
                    <label>Decimal Number:</label>
                    <input type="number" id="number" required>
                </div>
            `;
        } else if (calcId === 'density') {
            html += `
                <div class="form-group">
                    <label>Mass (kg):</label>
                    <input type="number" id="mass" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Volume (m³):</label>
                    <input type="number" id="volume" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'momentum') {
            html += `
                <div class="form-group">
                    <label>Mass (kg):</label>
                    <input type="number" id="mass" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Velocity (m/s):</label>
                    <input type="number" id="velocity" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'potential_energy') {
            html += `
                <div class="form-group">
                    <label>Mass (kg):</label>
                    <input type="number" id="mass" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Height (m):</label>
                    <input type="number" id="height" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'power_physics') {
            html += `
                <div class="form-group">
                    <label>Work (J):</label>
                    <input type="number" id="work" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Time (s):</label>
                    <input type="number" id="time" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'work') {
            html += `
                <div class="form-group">
                    <label>Force (N):</label>
                    <input type="number" id="force" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Distance (m):</label>
                    <input type="number" id="distance" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'pressure_physics') {
            html += `
                <div class="form-group">
                    <label>Force (N):</label>
                    <input type="number" id="force" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Area (m²):</label>
                    <input type="number" id="area" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'grade') {
            html += `
                <div class="form-group">
                    <label>Score Earned:</label>
                    <input type="number" id="score" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Total Points:</label>
                    <input type="number" id="total" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'test_score') {
            html += `
                <div class="form-group">
                    <label>Correct Answers:</label>
                    <input type="number" id="correct" required>
                </div>
                <div class="form-group">
                    <label>Total Questions:</label>
                    <input type="number" id="total" required>
                </div>
            `;
        } else if (calcId === 'final_grade') {
            html += `
                <div class="form-group">
                    <label>Current Grade (%):</label>
                    <input type="number" id="current_grade" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Desired Grade (%):</label>
                    <input type="number" id="desired_grade" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Final Exam Weight (%):</label>
                    <input type="number" id="final_weight" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'cgpa') {
            html += `
                <div class="form-group">
                    <label>GPAs (comma-separated):</label>
                    <input type="text" id="grades" placeholder="3.5, 3.8, 4.0" required>
                </div>
            `;
        } else if (calcId === 'protein_needs') {
            html += `
                <div class="form-group">
                    <label>Weight (kg):</label>
                    <input type="number" id="weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Activity Level:</label>
                    <select id="activity" required>
                        <option value="sedentary">Sedentary</option>
                        <option value="moderate" selected>Moderate</option>
                        <option value="active">Active</option>
                        <option value="athlete">Athlete</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'carbs_needs') {
            html += `
                <div class="form-group">
                    <label>Weight (kg):</label>
                    <input type="number" id="weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Activity Level:</label>
                    <select id="activity" required>
                        <option value="sedentary">Sedentary</option>
                        <option value="moderate" selected>Moderate</option>
                        <option value="active">Active</option>
                        <option value="athlete">Athlete</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'fiber_needs') {
            html += `
                <div class="form-group">
                    <label>Age:</label>
                    <input type="number" id="age" required>
                </div>
                <div class="form-group">
                    <label>Gender:</label>
                    <select id="gender" required>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>
            `;
        } 
        
        else if (calcId === 'carbon_footprint') {
    html += `
        <div class="form-group">
            <label>Electricity Usage (kWh/year):</label>
            <input type="number" id="electricity" step="0.01" placeholder="e.g., 1200" required>
        </div>

        <div class="form-group">
            <label>Natural Gas Usage (Therms/year):</label>
            <input type="number" id="gas" step="0.01" placeholder="e.g., 450" required>
        </div>

        <div class="form-group">
            <label>Car Travel (Miles/year):</label>
            <input type="number" id="car_miles" step="0.01" placeholder="e.g., 8000" required>
        </div>

        <div class="form-group">
            <label>Number of Flights per Year:</label>
            <input type="number" id="flights" step="1" placeholder="e.g., 3" required>
        </div>
    `;
}

        else if (calcId === 'correlation') {
    html += `
        <div class="form-group">
            <label>Enter X Values (comma-separated):</label>
            <input type="text" id="x_values" placeholder="Example: 2, 4, 6, 8, 10" required>
        </div>

        <div class="form-group">
            <label>Enter Y Values (comma-separated):</label>
            <input type="text" id="y_values" placeholder="Example: 3, 5, 7, 9, 11" required>
        </div>

        <p class="note">⚠ X and Y must have the same number of values.</p>
    `;
}

        else if (calcId === 'unit_energy') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter energy amount" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="joules">Joules (J)</option>
                <option value="kilojoules">Kilojoules (kJ)</option>
                <option value="calories">Calories (cal)</option>
                <option value="kilocalories">Kilocalories (kcal)</option>
                <option value="watt_hours">Watt-hours (Wh)</option>
                <option value="kilowatt_hours">Kilowatt-hours (kWh)</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="joules">Joules (J)</option>
                <option value="kilojoules">Kilojoules (kJ)</option>
                <option value="calories">Calories (cal)</option>
                <option value="kilocalories">Kilocalories (kcal)</option>
                <option value="watt_hours">Watt-hours (Wh)</option>
                <option value="kilowatt_hours">Kilowatt-hours (kWh)</option>
            </select>
        </div>
    `;
}

else if (calcId === 'lease_vs_buy') {
    html += `
        <div class="form-group">
            <label>Monthly Lease Payment ($):</label>
            <input type="number" id="lease_payment" step="0.01" placeholder="e.g., 250" required>
        </div>

        <div class="form-group">
            <label>Lease Term (Months):</label>
            <input type="number" id="lease_months" placeholder="e.g., 36" required>
        </div>

        <div class="form-group">
            <label>Monthly Loan Payment ($):</label>
            <input type="number" id="loan_payment" step="0.01" placeholder="e.g., 350" required>
        </div>

        <div class="form-group">
            <label>Loan Term (Months):</label>
            <input type="number" id="loan_months" placeholder="e.g., 48" required>
        </div>
    `;
}

else if (calcId === 'unit_length') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter length" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="meters">Meters (m)</option>
                <option value="kilometers">Kilometers (km)</option>
                <option value="centimeters">Centimeters (cm)</option>
                <option value="millimeters">Millimeters (mm)</option>
                <option value="miles">Miles (mi)</option>
                <option value="yards">Yards (yd)</option>
                <option value="feet">Feet (ft)</option>
                <option value="inches">Inches (in)</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="meters">Meters (m)</option>
                <option value="kilometers">Kilometers (km)</option>
                <option value="centimeters">Centimeters (cm)</option>
                <option value="millimeters">Millimeters (mm)</option>
                <option value="miles">Miles (mi)</option>
                <option value="yards">Yards (yd)</option>
                <option value="feet">Feet (ft)</option>
                <option value="inches">Inches (in)</option>
            </select>
        </div>
    `;
}
        
else if (calcId === 'unit_weight') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter weight" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="kilograms">Kilograms (kg)</option>
                <option value="grams">Grams (g)</option>
                <option value="milligrams">Milligrams (mg)</option>
                <option value="pounds">Pounds (lb)</option>
                <option value="ounces">Ounces (oz)</option>
                <option value="tons">Tons (t)</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="kilograms">Kilograms (kg)</option>
                <option value="grams">Grams (g)</option>
                <option value="milligrams">Milligrams (mg)</option>
                <option value="pounds">Pounds (lb)</option>
                <option value="ounces">Ounces (oz)</option>
                <option value="tons">Tons (t)</option>
            </select>
        </div>
    `;
}


else if (calcId === 'unit_volume') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter volume" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="liters">Liters (L)</option>
                <option value="milliliters">Milliliters (mL)</option>
                <option value="gallons">Gallons (gal)</option>
                <option value="quarts">Quarts (qt)</option>
                <option value="pints">Pints (pt)</option>
                <option value="cups">Cups</option>
                <option value="fluid_ounces">Fluid Ounces (fl oz)</option>
                <option value="cubic_meters">Cubic Meters (m³)</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="liters">Liters (L)</option>
                <option value="milliliters">Milliliters (mL)</option>
                <option value="gallons">Gallons (gal)</option>
                <option value="quarts">Quarts (qt)</option>
                <option value="pints">Pints (pt)</option>
                <option value="cups">Cups</option>
                <option value="fluid_ounces">Fluid Ounces (fl oz)</option>
                <option value="cubic_meters">Cubic Meters (m³)</option>
            </select>
        </div>
    `;
}

else if (calcId === 'tree_offset') {
    html += `
        <div class="form-group">
            <label>Enter CO₂ Emissions (kg per year):</label>
            <input type="number" id="co2" step="0.01" placeholder="e.g., 1200" required>
        </div>
        <p class="note">🌱 Approx. 1 tree offsets ~21.77 kg CO₂ per year.</p>
    `;
}


else if (calcId === 'tire_size') {
    html += `
        <div class="form-group">
            <label>Tire Width (mm):</label>
            <input type="number" id="width" step="0.01" placeholder="e.g., 205" required>
        </div>

        <div class="form-group">
            <label>Aspect Ratio (%):</label>
            <input type="number" id="aspect" step="0.01" placeholder="e.g., 55" required>
        </div>

        <div class="form-group">
            <label>Rim Diameter (inches):</label>
            <input type="number" id="diameter" step="0.01" placeholder="e.g., 16" required>
        </div>

        <p class="note">📌 Formula uses: total diameter = rim diameter × 25.4 + 2 × sidewall height.</p>
    `;
}


else if (calcId === 'time_zone') {
    html += `
        <div class="form-group">
            <label>Select Time:</label>
            <input type="time" id="time" required>
        </div>

        <div class="form-group">
            <label>From Time Zone (UTC Offset):</label>
            <select id="from_offset" required>
                <option value="-12">UTC -12</option>
                <option value="-11">UTC -11</option>
                <option value="-10">UTC -10</option>
                <option value="-9">UTC -9</option>
                <option value="-8">UTC -8</option>
                <option value="-7">UTC -7</option>
                <option value="-6">UTC -6</option>
                <option value="-5">UTC -5</option>
                <option value="-4">UTC -4</option>
                <option value="-3">UTC -3</option>
                <option value="-2">UTC -2</option>
                <option value="-1">UTC -1</option>
                <option value="0" selected>UTC 0</option>
                <option value="1">UTC +1</option>
                <option value="2">UTC +2</option>
                <option value="3">UTC +3</option>
                <option value="3.5">UTC +3:30</option>
                <option value="4">UTC +4</option>
                <option value="4.5">UTC +4:30</option>
                <option value="5">UTC +5</option>
                <option value="5.5">UTC +5:30 (India)</option>
                <option value="6">UTC +6</option>
                <option value="7">UTC +7</option>
                <option value="8">UTC +8</option>
                <option value="9">UTC +9</option>
                <option value="9.5">UTC +9:30</option>
                <option value="10">UTC +10</option>
                <option value="11">UTC +11</option>
                <option value="12">UTC +12</option>
                <option value="13">UTC +13</option>
                <option value="14">UTC +14</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Time Zone (UTC Offset):</label>
            <select id="to_offset" required>
                <option value="-12">UTC -12</option>
                <option value="-11">UTC -11</option>
                <option value="-10">UTC -10</option>
                <option value="-9">UTC -9</option>
                <option value="-8">UTC -8</option>
                <option value="-7">UTC -7</option>
                <option value="-6">UTC -6</option>
                <option value="-5">UTC -5</option>
                <option value="-4">UTC -4</option>
                <option value="-3">UTC -3</option>
                <option value="-2">UTC -2</option>
                <option value="-1">UTC -1</option>
                <option value="0" selected>UTC 0</option>
                <option value="1">UTC +1</option>
                <option value="2">UTC +2</option>
                <option value="3">UTC +3</option>
                <option value="3.5">UTC +3:30</option>
                <option value="4">UTC +4</option>
                <option value="4.5">UTC +4:30</option>
                <option value="5">UTC +5</option>
                <option value="5.5">UTC +5:30 (India)</option>
                <option value="6">UTC +6</option>
                <option value="7">UTC +7</option>
                <option value="8">UTC +8</option>
                <option value="9">UTC +9</option>
                <option value="9.5">UTC +9:30</option>
                <option value="10">UTC +10</option>
                <option value="11">UTC +11</option>
                <option value="12">UTC +12</option>
                <option value="13">UTC +13</option>
                <option value="14">UTC +14</option>
            </select>
        </div>
    `;
}

else if (calcId === 'unit_time') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter time value" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="seconds">Seconds (s)</option>
                <option value="minutes">Minutes (min)</option>
                <option value="hours">Hours (hr)</option>
                <option value="days">Days</option>
                <option value="weeks">Weeks</option>
                <option value="years">Years</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="seconds">Seconds (s)</option>
                <option value="minutes">Minutes (min)</option>
                <option value="hours">Hours (hr)</option>
                <option value="days">Days</option>
                <option value="weeks">Weeks</option>
                <option value="years">Years</option>
            </select>
        </div>
    `;
}


else if (calcId === 'unit_speed') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter speed value" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="meters_per_second">Meters per Second (m/s)</option>
                <option value="kilometers_per_hour">Kilometers per Hour (km/h)</option>
                <option value="miles_per_hour">Miles per Hour (mph)</option>
                <option value="feet_per_second">Feet per Second (ft/s)</option>
                <option value="knots">Knots (nautical mph)</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="meters_per_second">Meters per Second (m/s)</option>
                <option value="kilometers_per_hour">Kilometers per Hour (km/h)</option>
                <option value="miles_per_hour">Miles per Hour (mph)</option>
                <option value="feet_per_second">Feet per Second (ft/s)</option>
                <option value="knots">Knots (nautical mph)</option>
            </select>
        </div>
    `;
}


else if (calcId === 'solar_panels') {
    html += `
        <div class="form-group">
            <label>Monthly Electricity Bill ($):</label>
            <input type="number" id="monthly_bill" step="0.01" placeholder="e.g., 120" required>
        </div>

        <div class="form-group">
            <label>Electricity Rate ($ per kWh):</label>
            <input type="number" id="rate" step="0.001" placeholder="Default: 0.12">
        </div>

        <p class="note">⚡ Assumption: Each solar panel generates approx. 1.5 kWh/day.</p>
    `;
}


else if (calcId === 'unit_power') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter power value" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="watts">Watts (W)</option>
                <option value="kilowatts">Kilowatts (kW)</option>
                <option value="horsepower">Horsepower (HP)</option>
                <option value="btu_per_hour">BTU/hour (BTU/hr)</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="watts">Watts (W)</option>
                <option value="kilowatts">Kilowatts (kW)</option>
                <option value="horsepower">Horsepower (HP)</option>
                <option value="btu_per_hour">BTU/hour (BTU/hr)</option>
            </select>
        </div>
    `;
}


else if (calcId === 'unit_pressure') {
    html += `
        <div class="form-group">
            <label>Enter Value:</label>
            <input type="number" id="value" step="0.01" placeholder="Enter pressure value" required>
        </div>

        <div class="form-group">
            <label>From Unit:</label>
            <select id="from" required>
                <option value="pascals">Pascals (Pa)</option>
                <option value="kilopascals">Kilopascals (kPa)</option>
                <option value="bar">Bar</option>
                <option value="psi">PSI (Pound per Square Inch)</option>
                <option value="atmospheres">Atmospheres (atm)</option>
            </select>
        </div>

        <div class="form-group">
            <label>To Unit:</label>
            <select id="to" required>
                <option value="pascals">Pascals (Pa)</option>
                <option value="kilopascals">Kilopascals (kPa)</option>
                <option value="bar">Bar</option>
                <option value="psi">PSI (Pound per Square Inch)</option>
                <option value="atmospheres">Atmospheres (atm)</option>
            </select>
        </div>
    `;
}


else if (calcId === 'recycling') {
    html += `
        <div class="form-group">
            <label>Paper Recycled (kg/year):</label>
            <input type="number" id="paper" step="0.01" placeholder="e.g., 20">
        </div>

        <div class="form-group">
            <label>Plastic Recycled (kg/year):</label>
            <input type="number" id="plastic" step="0.01" placeholder="e.g., 15">
        </div>

        <div class="form-group">
            <label>Glass Recycled (kg/year):</label>
            <input type="number" id="glass" step="0.01" placeholder="e.g., 10">
        </div>

        <div class="form-group">
            <label>Metal Recycled (kg/year):</label>
            <input type="number" id="metal" step="0.01" placeholder="e.g., 8">
        </div>

        <p class="note">♻ Recycling reduces CO₂ emissions and conserves energy.</p>
    `;
}


        else if (calcId === 'sleep_hours') {
            html += `
                <div class="form-group">
                    <label>Bedtime:</label>
                    <input type="time" id="bedtime" required>
                </div>
                <div class="form-group">
                    <label>Wake Time:</label>
                    <input type="time" id="waketime" required>
                </div>
            `;
        } else if (calcId === 'next_birthday') {
            html += `
                <div class="form-group">
                    <label>Date of Birth:</label>
                    <input type="date" id="dob" required>
                </div>
            `;
        } else if (calcId === 'countdown') {
            html += `
                <div class="form-group">
                    <label>Target Date:</label>
                    <input type="date" id="date" required>
                </div>
            `;
        } else if (calcId === 'work_days') {
            html += `
                <div class="form-group">
                    <label>Start Date:</label>
                    <input type="date" id="date1" required>
                </div>
                <div class="form-group">
                    <label>End Date:</label>
                    <input type="date" id="date2" required>
                </div>
            `;
        } else if (calcId === 'car_loan') {
            html += `
                <div class="form-group">
                    <label>Loan Amount ($):</label>
                    <input type="number" id="principal" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Interest Rate (%):</label>
                    <input type="number" id="rate" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Loan Term (months):</label>
                    <input type="number" id="months" required>
                </div>
            `;
        } else if (calcId === 'fuel_cost') {
            html += `
                <div class="form-group">
                    <label>Distance (miles):</label>
                    <input type="number" id="distance" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>MPG:</label>
                    <input type="number" id="mpg" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Price per Gallon ($):</label>
                    <input type="number" id="price" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'electricity_cost') {
            html += `
                <div class="form-group">
                    <label>Power (Watts):</label>
                    <input type="number" id="watts" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Hours Used:</label>
                    <input type="number" id="hours" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Rate ($/kWh):</label>
                    <input type="number" id="rate" step="0.01" value="0.12" required>
                </div>
            `;
        } else if (calcId === 'tile_needed') {
            html += `
                <div class="form-group">
                    <label>Room Length (ft):</label>
                    <input type="number" id="length" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Room Width (ft):</label>
                    <input type="number" id="width" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Tile Size (ft):</label>
                    <input type="number" id="tile_size" step="0.01" value="1" required>
                </div>
            `;
        } else if (calcId === 'flooring') {
            html += `
                <div class="form-group">
                    <label>Length (ft):</label>
                    <input type="number" id="length" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Width (ft):</label>
                    <input type="number" id="width" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'fence') {
            html += `
                <div class="form-group">
                    <label>Length (ft):</label>
                    <input type="number" id="length" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Width (ft):</label>
                    <input type="number" id="width" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'concrete') {
            html += `
                <div class="form-group">
                    <label>Length (ft):</label>
                    <input type="number" id="length" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Width (ft):</label>
                    <input type="number" id="width" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Depth (inches):</label>
                    <input type="number" id="depth" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'roofing') {
            html += `
                <div class="form-group">
                    <label>Length (ft):</label>
                    <input type="number" id="length" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Width (ft):</label>
                    <input type="number" id="width" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Roof Pitch (optional):</label>
                    <input type="number" id="pitch" step="0.01" value="0">
                </div>
            `;
        } else if (calcId === 'recipe_scaler') {
            html += `
                <div class="form-group">
                    <label>Original Servings:</label>
                    <input type="number" id="original_servings" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Desired Servings:</label>
                    <input type="number" id="desired_servings" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'oven_temp') {
            html += `
                <div class="form-group">
                    <label>Temperature:</label>
                    <input type="number" id="temp" step="1" required>
                </div>
                <div class="form-group">
                    <label>From:</label>
                    <select id="from" required>
                        <option value="fahrenheit">Fahrenheit</option>
                        <option value="celsius">Celsius</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>To:</label>
                    <select id="to" required>
                        <option value="fahrenheit">Fahrenheit</option>
                        <option value="celsius">Celsius</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'cooking_time') {
            html += `
                <div class="form-group">
                    <label>Weight (lbs or kg):</label>
                    <input type="number" id="weight" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Minutes per Unit:</label>
                    <input type="number" id="time_per_unit" step="1" value="20" required>
                </div>
            `;
        } else if (calcId === 'paint_needed') {
            html += `
                <div class="form-group">
                    <label>Length (feet):</label>
                    <input type="number" id="length" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Width (feet):</label>
                    <input type="number" id="width" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Height (feet, optional):</label>
                    <input type="number" id="height" step="0.01">
                </div>
                <div class="form-group">
                    <label>Number of Coats:</label>
                    <input type="number" id="coats" value="1" required>
                </div>
                <div class="form-group">
                    <label>Coverage per gallon (sq ft):</label>
                    <input type="number" id="coverage" value="350" required>
                </div>
            `;
        } else if (calcId === 'savings_goal') {
            html += `
                <div class="form-group">
                    <label>Savings Goal ($):</label>
                    <input type="number" id="goal" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Interest Rate (%):</label>
                    <input type="number" id="rate" step="0.01" value="0">
                </div>
                <div class="form-group">
                    <label>Time (months):</label>
                    <input type="number" id="months" required>
                </div>
            `;
        }  else if (calcId === 'currency_converter') {
            html += `
                <div class="form-group">
                    <label>Amount:</label>
                    <input type="number" id="amount" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>From Rate (to USD):</label>
                    <input type="number" id="from_rate" step="0.0001" value="1" required>
                </div>
                <div class="form-group">
                    <label>To Rate (from USD):</label>
                    <input type="number" id="to_rate" step="0.0001" value="1" required>
                </div>
            `;
        } else if (calcId === 'roman_numeral') {
            html += `
                <div class="form-group">
                    <label>Number (1-3999):</label>
                    <input type="number" id="number" min="1" max="3999" required>
                </div>
            `;
        } else if (calcId === 'alcohol_units') {
            html += `
                <div class="form-group">
                    <label>Volume (ml):</label>
                    <input type="number" id="volume" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>ABV (%):</label>
                    <input type="number" id="abv" step="0.1" required>
                </div>
            `;
        } else if (calcId === 'body_fat') {
            html += `
                <div class="form-group">
                    <label>Weight (kg):</label>
                    <input type="number" id="weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Waist (cm):</label>
                    <input type="number" id="waist" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Height (cm):</label>
                    <input type="number" id="height" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Gender:</label>
                    <select id="gender" required>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'ideal_weight') {
            html += `
                <div class="form-group">
                    <label>Height (cm):</label>
                    <input type="number" id="height" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Gender:</label>
                    <select id="gender" required>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'calories_burned') {
            html += `
                <div class="form-group">
                    <label>Weight (kg):</label>
                    <input type="number" id="weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Duration (minutes):</label>
                    <input type="number" id="duration" step="1" required>
                </div>
                <div class="form-group">
                    <label>Activity Level:</label>
                    <select id="activity" required>
                        <option value="light">Light</option>
                        <option value="moderate" selected>Moderate</option>
                        <option value="vigorous">Vigorous</option>
                    </select>
                </div>
            `;
        } else if (calcId === 'water_intake') {
            html += `
                <div class="form-group">
                    <label>Weight (kg):</label>
                    <input type="number" id="weight" step="0.1" required>
                </div>
                <div class="form-group">
                    <label>Activity Hours:</label>
                    <input type="number" id="activity" step="0.1" value="0">
                </div>
            `;
        } else if (calcId === 'heart_rate') {
            html += `
                <div class="form-group">
                    <label>Age:</label>
                    <input type="number" id="age" required>
                </div>
            `;
        } else if (calcId === 'mortgage') {
            html += `
                <div class="form-group">
                    <label>Home Price ($):</label>
                    <input type="number" id="price" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Down Payment ($):</label>
                    <input type="number" id="down" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Interest Rate (%):</label>
                    <input type="number" id="rate" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Loan Term (years):</label>
                    <input type="number" id="years" required>
                </div>
            `;

        } else if (calcId === 'fuel_economy') {
            html += `
                <div class="form-group">
                    <label>Distance (miles):</label>
                    <input type="number" id="distance" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Fuel Used (gallons):</label>
                    <input type="number" id="fuel" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'discount') {
            html += `
                <div class="form-group">
                    <label>Original Price ($):</label>
                    <input type="number" id="price" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Discount (%):</label>
                    <input type="number" id="discount" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'tax') {
            html += `
                <div class="form-group">
                    <label>Amount ($):</label>
                    <input type="number" id="amount" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Tax Rate (%):</label>
                    <input type="number" id="rate" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'grade') {
            html += `
                <div class="form-group">
                    <label>Points Earned:</label>
                    <input type="number" id="earned" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Total Points:</label>
                    <input type="number" id="total" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'retirement') {
            html += `
                <div class="form-group">
                    <label>Current Age:</label>
                    <input type="number" id="age" required>
                </div>
                <div class="form-group">
                    <label>Retirement Age:</label>
                    <input type="number" id="retire_age" required>
                </div>
                <div class="form-group">
                    <label>Monthly Savings ($):</label>
                    <input type="number" id="monthly" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Annual Return (%):</label>
                    <input type="number" id="return" step="0.01" value="7" required>
                </div>
            `;
        } else if (calcId === 'investment') {
            html += `
                <div class="form-group">
                    <label>Initial Investment ($):</label>
                    <input type="number" id="initial" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Monthly Contribution ($):</label>
                    <input type="number" id="monthly" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Annual Return (%):</label>
                    <input type="number" id="return" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Years:</label>
                    <input type="number" id="years" required>
                </div>
            `;
        } else if (calcId === 'ideal_weight') {
            html += `
                <div class="form-group">
                    <label>Gender:</label>
                    <select id="gender" required>
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Height (cm):</label>
                    <input type="number" id="height" step="0.1" required>
                </div>
            `;
        } else if (calcId === 'pregnancy') {
            html += `
                <div class="form-group">
                    <label>Last Menstrual Period:</label>
                    <input type="date" id="lmp" required>
                </div>
            `;
        } else if (calcId === 'area_square') {
            html += `
                <div class="form-group">
                    <label>Side Length:</label>
                    <input type="number" id="side" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'volume_cube') {
            html += `
                <div class="form-group">
                    <label>Side Length:</label>
                    <input type="number" id="side" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'volume_cylinder') {
            html += `
                <div class="form-group">
                    <label>Radius:</label>
                    <input type="number" id="radius" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>Height:</label>
                    <input type="number" id="height" step="0.01" required>
                </div>
            `;
        } else if (calcId === 'quadratic') {
            html += `
                <div class="form-group">
                    <label>a (coefficient of x²):</label>
                    <input type="number" id="a" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>b (coefficient of x):</label>
                    <input type="number" id="b" step="0.01" required>
                </div>
                <div class="form-group">
                    <label>c (constant):</label>
                    <input type="number" id="c" step="0.01" required>
                </div>
            `;
        } else {
            html += `
                <div class="form-group">
                    <div style="text-align:center; padding:40px; background:linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); border-radius:15px; border:2px dashed #667eea;">
                        <h3 style="color:#667eea; margin-bottom:15px;">🚧 Calculator Coming Soon!</h3>
                        <p style="color:#666; margin-bottom:20px;">This calculator is being developed and will be available soon.</p>
                        <p style="color:#888; font-size:0.9em;">We're constantly adding new calculators to serve you better!</p>
                    </div>
                </div>
            `;
  
            ``;
        }

    return html;
}
