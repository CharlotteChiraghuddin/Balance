from flask import Blueprint, request, redirect, url_for
from models.food import Food
from models.repository import Repository

food_bp = Blueprint('food',__name__)
repo=Repository()

@food_bp.route("/log_food", methods=["POST"])
def submit_food():
    name=request.form["food-name"]
    calories=int(request.form["calories"])
    meal_type=request.form["meal-type"]
    date = request.form["date"] #needs to be converted to SQL date format

    journal_day_id = repo.get_journal_id_by_date(date)
    if journal_day_id is None:
        journal_day_id = repo.add_journal_day(
            user_id=1,
            date=date,
            mood="",
            reflection=""
        )
    repo.add_food(journal_day_id, name, calories, meal_type)

    return redirect(url_for('logbook.logbook_home')) #LATER ADD A FUNCTION TO REDIRECT TO TODAYS LOGS FOR FOOD.