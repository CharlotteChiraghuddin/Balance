class JournalDay:
    def __init__(self, day_id: int, date: str, content: str):
        self.day_id = day_id
        self.date = date
        self.content = content

    def __str__(self):
        return f"JournalDay(day_id={self.day_id}, date={self.date}, content={self.content})"