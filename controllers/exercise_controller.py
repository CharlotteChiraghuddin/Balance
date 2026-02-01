from flask import Blueprint, request, redirect, session, url_for
from models.food import Food
from models.repository import Repository

exercise_bp = Blueprint('exercise',__name__)
repo=Repository()

@exercise_bp.route("/log_exercise", methods=["POST"])
def submit_exercise():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))
    name = request.form["exercise-name"]
    duration = int(request.form["duration"])
    calories_burned = int(request.form["calories"])
    date = request.form["date"]

    journal_day_id = repo.get_journal_id_by_date(session.get('user_id'), date)

    if journal_day_id is None:
        journal_day_id = repo.add_journal_day(
            user_id=session.get('user_id'),
            date=date,
            mood="",
            reflection=""
        )

    # ALWAYS add the exercise
    repo.add_exercise(journal_day_id, name, duration, calories_burned)

    return redirect(url_for('logbook.logbook_home'))
