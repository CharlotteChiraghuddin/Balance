class User:
    def __init__(self, first_name, last_name, email, password_hash=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
    def __str__(self):
        return f"Users(first_name={self.first_name}, last_name={self.last_name}, email={self.email})"