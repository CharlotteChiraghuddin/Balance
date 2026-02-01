from sqlite3 import Date
import flask
from flask import Flask, render_template, session, redirect, url_for
from models.repository import Repository
import os
from controllers.logbook import logbook_bp
from controllers.food_controller import food_bp
from controllers.exercise_controller import exercise_bp
from controllers.finance_controller import finance_bp
from controllers.auth_controller import auth_bp
from controllers.mood_controller import mood_bp
from datetime import datetime, date
app=flask.Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = os.environ.get("SECRET_KEY", "dev-key")

repo=Repository(
    host="127.0.0.1",
    port=3306,
    user="root",
    password=os.getenv("MYSQL_PASSWORD"),
    database="journal_db",
    use_pool=True,
    pool_name="journal_pool",
    pool_size=5,
    ensure_schema=True
    )

app.register_blueprint(logbook_bp)
app.register_blueprint(food_bp)
app.register_blueprint(exercise_bp)
app.register_blueprint(finance_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(mood_bp)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/calendar")
def calendar():
    return render_template('calendar.html')

@app.route("/music")
def music():
    return render_template('music.html')

@app.route("/insights")
def insights():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    # Get last 7 days of JournalDay objects
    week_days = repo.get_user_data_week(user_id)

    # Get full detailed data (food, exercise, transactions)
    full_data = repo.get_user_data_weekly(user_id)

    # --- TODAY'S DATA ---
    today = week_days[0] if week_days else None
    mood = today.mood if today else None

    # --- TODAY'S CALORIES ---
    if full_data:
        today_food = full_data[0]["food"]
        today_exercise = full_data[0]["exercise"]

        calories = sum(f["calories"] for f in today_food)
        exercise_calories = sum(e["calories"] for e in today_exercise)
    else:
        calories = 0
        exercise_calories = 0

    return render_template(
        "insights.html",
        Date=datetime.now().date(),
        mood=mood,
        calories=calories,
        exercise_calories=exercise_calories,
        full_data=full_data,
        today_data=today
    )

if __name__=="__main__":
    app.run(debug=True)


