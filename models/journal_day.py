class JournalDay:
    def __init__(self, journal_day_id: int, user_id: int, date: str, mood: str, reflection: str):
        self.journal_day_id = journal_day_id
        self.user_id = user_id
        self.date = date
        self.mood = mood
        self.reflection = reflection
    def __str__(self):
        return f"JournalDay(day_id={self.journal_day_id}, date={self.date}, mood={self.mood}, reflection={self.reflection})"