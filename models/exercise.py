class Exercise:
    def __init__(self, exercise_id: int, journal_day_id: int, name: str, calories: int, duration: int):
        self.exercise_id = exercise_id
        self.journal_day_id = journal_day_id
        self.name = name
        self.calories = calories
        self.duration = duration

    def __str__(self):
        return f"Exercise(exercise_id={self.exercise_id}, name={self.name}, duration={self.duration})"