# controllers/logbook.py

from flask import Blueprint, render_template

logbook_bp = Blueprint("logbook", __name__)

@logbook_bp.route("/logbook")
def logbook_home():
    return render_template("logbook.html")

@logbook_bp.route("/logbook/food")
def logbook_food():
    return render_template("log_food.html")

@logbook_bp.route("/logbook/exercise")
def logbook_exercise():
    return render_template("log_exercise.html")

@logbook_bp.route("/logbook/mood")
def logbook_mood():
    return render_template("log_mood.html")

@logbook_bp.route("/logbook/finances")
def logbook_finances():
    return render_template("log_finances.html")
