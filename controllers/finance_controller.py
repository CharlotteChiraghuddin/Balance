from flask import Blueprint, request, redirect, session, url_for
from models.food import Food
from models.repository import Repository

finance_bp = Blueprint('finance',__name__)
repo=Repository()

@finance_bp.route("/log_transaction", methods=["POST"])
def submit_transaction():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))
    name = request.form["expense-name"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    journal_day_id = repo.get_journal_id_by_date(session.get('user_id'), date)

    if journal_day_id is None:
        journal_day_id = repo.add_journal_day(
            user_id=session.get('user_id'),
            date=date,
            mood="",
            reflection=""
        )

    # ALWAYS add the transaction
    repo.add_transaction(journal_day_id, name, amount, category)

    return redirect(url_for('logbook.logbook_home'))
