class Food:
    def __init__(self, food_id: int, name: str, calories: int):
        self.food_id = food_id
        self.name = name
        self.calories = calories

    def __str__(self):
        return f"Food(food_id={self.food_id}, name={self.name}, calories={self.calories})"
