class Food:
    def __init__(self, food_id, journal_day_id, name, calories, meal_type):
        self.food_id = food_id
        self.journal_day_id = journal_day_id
        self.name = name
        self.calories = calories
        self.meal_type = meal_type


    def __str__(self):
        return f"Food(food_id={self.food_id}, name={self.name}, calories={self.calories})"
