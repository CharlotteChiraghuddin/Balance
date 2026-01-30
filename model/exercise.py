class Exercise:
    def __init__(self, exercise_id: int, name: str, duration: int):
        self.exercise_id = exercise_id
        self.name = name
        self.duration = duration

    def __str__(self):
        return f"Exercise(exercise_id={self.exercise_id}, name={self.name}, duration={self.duration})"