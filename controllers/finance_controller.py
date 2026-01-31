from flask import Blueprint, request, redirect, url_for
from models.food import Food
from models.repository import Repository

finance_bp = Blueprint('finance',__name__)
repo=Repository()

@finance_bp.route("/log_transaction", methods=["POST"])
def submit_transaction():
    name = request.form["expense-name"]
    amount = float(request.form["amount"])
    category = request.form["category"]
    date = request.form["date"]

    journal_day_id = repo.get_journal_id_by_date(date)

    if journal_day_id is None:
        journal_day_id = repo.add_journal_day(
            user_id=1,
            date=date,
            mood="",
            reflection=""
        )

    # ALWAYS add the transaction
    repo.add_transaction(journal_day_id, name, amount, category)

    return redirect(url_for('logbook.logbook_home'))
