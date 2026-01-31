class Transaction:
    def __init__(self, transaction_id, journal_day_id, name, amount, category):
        self.transaction_id = transaction_id
        self.journal_day_id = journal_day_id
        self.name = name
        self.amount = amount
        self.category = category


    def __str__(self):
        return f"Transaction(transaction_id={self.transaction_id}, amount={self.amount}, date={self.date}, name={self.name}, category={self.category})"