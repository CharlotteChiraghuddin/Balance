import flask
from flask import Flask, render_template
from model.repository import Repository
import os



app=flask.Flask(__name__)

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
    return render_template('insights.html')

@app.route('/logbook')
def logbook():
    return render_template('logbook.html')

@app.route('/logbook/food')
def log_food():
    return render_template('log_food.html')

@app.route('/logbook/exercise')
def log_exercise():
    return render_template('log_exercise.html')

@app.route('/logbook/mood')
def log_mood():
    return render_template('log_mood.html')

@app.route('/logbook/finances')
def log_finances():
    return render_template('log_finances.html')

if __name__=="__main__":
    app.run(debug=True)


