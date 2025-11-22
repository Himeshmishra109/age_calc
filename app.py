from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    age_result = None
    if request.method == "POST":
        dob = request.form["dob"]
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()

        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if months < 0:
            years -= 1
            months += 12

        if days < 0:
            months -= 1
            prev_month_days = (datetime(today.year, today.month, 1) - 
                               datetime(today.year, today.month - 1, 1)).days
            days += prev_month_days

        age_result = f"Your Age: {years} Years, {months} Months, {days} Days"
    return render_template("index.html", age_result=age_result)

if __name__ == "__main__":
    app.run()
