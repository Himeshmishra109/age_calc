from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, date, timedelta
import calendar

app = Flask(__name__, static_folder="static", template_folder="templates")


def compute_age(birth_date, today):
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day

    if days < 0:
        # borrow days from previous month
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
        months -= 1

    if months < 0:
        months += 12
        years -= 1

    return years, months, days


def next_birthday_info(birth_date, today):
    # next birthday year
    ny = today.year if (today.month, today.day) <= (birth_date.month, birth_date.day) else today.year + 1
    try:
        nb = date(ny, birth_date.month, birth_date.day)
    except ValueError:
        # Feb 29 handling -> treat as Feb 28 on non-leap years
        nb = date(ny, 2, 28)
    delta = nb - today
    return nb, delta.days


@app.route("/", methods=["GET", "POST"])
def index():
    context = {
        "age_result": None,
        "total_days": None,
        "next_birthday_days": None,
        "next_birthday_date": None,
        "birth_weekday": None,
        "error": None,
    }

    if request.method == "POST":
        dob = request.form.get("dob", "").strip()
        if not dob:
            context["error"] = "Please enter your date of birth."
            return render_template("index.html", **context)

        try:
            birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
        except ValueError:
            context["error"] = "Invalid date format. Use yyyy-mm-dd."
            return render_template("index.html", **context)

        today = date.today()
        if birth_date > today:
            context["error"] = "Date of birth cannot be in the future."
            return render_template("index.html", **context)

        years, months, days = compute_age(birth_date, today)
        total_days = (today - birth_date).days
        nb_date, nb_days = next_birthday_info(birth_date, today)
        weekday = calendar.day_name[birth_date.weekday()]

        context.update({
            "age_result": f"{years} years, {months} months, {days} days",
            "total_days": f"{total_days} days (~{total_days*24} hours)",
            "next_birthday_days": nb_days,
            "next_birthday_date": nb_date.isoformat(),
            "birth_weekday": weekday,
        })

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
