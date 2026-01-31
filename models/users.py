class User:
    def __init__(self, user_id, first_name, last_name, email, password_hash, created_at=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash
        self.created_at = created_at

    def __str__(self):
        return f"User(id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}, email={self.email})"
