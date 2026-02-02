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
from insight_engine import analyze_exercise, analyze_finance, calculate_total_calories, analyze_mood, generate_calorie_insights, generate_exercise_insights, generate_finance_insights, generate_mood_insights,analyze_calories,generate_calorie_insights
from collections import defaultdict


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
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))
    
    full_data_week = repo.get_user_data_weekly(user_id)
    # Analyze exercise data for insights
    exercises = repo.list_exercise_by_week(user_id)
    exercise_totals = analyze_exercise(exercises)
    exercise_insights = generate_exercise_insights(exercise_totals)

    #Analyze calorie data for insights
    calories = repo.list_food_by_week(user_id)
    total_calories = analyze_calories(calories)
    calorie_insights = generate_calorie_insights(total_calories)

    #Analyze finance data for insights
    transactions = repo.list_transactions_by_week(user_id)
    finance_totals = analyze_finance(transactions)
    finance_insights = generate_finance_insights(finance_totals)
    #Analyze mood data for insights
    moods = repo.list_mood_by_week(user_id)
    mood_totals = analyze_mood(moods)
    mood_insights = generate_mood_insights(mood_totals)

    print(full_data_week)
    return render_template('index.html', exercise_insights = exercise_insights, finance_insights=finance_insights, mood_insights=mood_insights, calorie_insights=calorie_insights)

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

    full_data_day = repo.get_user_data_daily(user_id)
    full_data_week = repo.get_user_data_weekly(user_id)
    full_data_month = repo.get_user_data_monthly(user_id)
    full_data_year = repo.get_user_data_yearly(user_id)

    
    return render_template("insights.html", full_data_day=full_data_day, full_data_week=full_data_week, full_data_month=full_data_month, full_data_year=full_data_year)

if __name__=="__main__":
    app.run(debug=True)


