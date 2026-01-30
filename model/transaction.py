class Transaction:
    def __init__(self, transaction_id: int, amount: float, date: str, description: str):
        self.transaction_id = transaction_id
        self.amount = amount
        self.date = date
        self.description = description

    def __str__(self):
        return f"Transaction(transaction_id={self.transaction_id}, amount={self.amount}, date={self.date}, description={self.description})"