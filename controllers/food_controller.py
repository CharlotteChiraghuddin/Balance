from flask import Blueprint, render_template, request, redirect, session, url_for
from models.food import Food
from models.repository import Repository

food_bp = Blueprint('food',__name__)
repo=Repository()

@food_bp.route("/log_food", methods=["POST"])
def submit_food():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))
    name=request.form["food-name"]
    calories=int(request.form["calories"])
    meal_type=request.form["meal-type"]
    date = request.form["date"] #needs to be converted to SQL date format

    journal_day_id = repo.get_journal_id_by_date(session.get('user_id'), date)
    if journal_day_id is None:
        journal_day_id = repo.add_journal_day(
            user_id=session.get('user_id'),
            date=date,
            mood="",
            reflection=""
        )
    repo.add_food(journal_day_id, name, calories, meal_type)

    return redirect(url_for('logbook.logbook_home')) #LATER ADD A FUNCTION TO REDIRECT TO TODAYS LOGS FOR FOOD.

#@food_bp.route("/view_food")
#def view_food():
 #   user_id = session.get("user_id")
  #  foods_daily = repo.get_user_data_daily(user_id)
   # food_weekly = repo.get_user_data_weekly(user_id)
    #food_monthly = repo.get_user_data_monthly(user_id)
    #foods_yearly = repo.get_user_data_yearly(user_id)
    #print("DAILY:", foods_daily)
    #print("WEEKLY:", food_weekly)
    #print("MONTHLY:", food_monthly)
    #print("YEARLY:", foods_yearly)
    #return render_template("view_food.html", foods_daily=foods_daily, food_weekly=food_weekly, food_monthly=food_monthly, foods_yearly=foods_yearly)