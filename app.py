import flask
from flask import Flask, render_template
from models.repository import Repository
import os
from controllers.logbook import logbook_bp
from controllers.food_controller import food_bp
from controllers.exercise_controller import exercise_bp
from controllers.finance_controller import finance_bp
from controllers.auth_controller import auth_bp

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

if __name__=="__main__":
    app.run(debug=True)


