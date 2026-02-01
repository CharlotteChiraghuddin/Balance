from flask import Blueprint, request, redirect, session, url_for
from models.food import Food
from models.repository import Repository
from datetime import date, datetime

mood_bp = Blueprint('mood',__name__)
repo=Repository()

@mood_bp.route("/log_mood", methods=["POST"])
def submit_mood():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))
    mood=request.form["mood"]
    reflection=request.form["reflection"]
    date= datetime.now().date().isoformat()
    journal_day_id = repo.get_journal_id_by_date(session.get('user_id'), date)
    if journal_day_id is None:
        journal_day_id = repo.add_journal_day(
            user_id=session.get('user_id'),
            date=date,
            mood=mood,
            reflection=reflection
        )
    repo.add_mood(journal_day_id, session.get('user_id'), mood, reflection)

    return redirect(url_for('logbook.logbook_home')) #LATER ADD A FUNCTION TO REDIRECT TO TODAYS LOGS FOR FOOD.