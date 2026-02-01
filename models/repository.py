import mysql.connector
from mysql.connector import pooling, Error
import os
from typing import List, Optional, Any, Dict
from models.users import User
from models.journal_day import JournalDay
from models.food import Food
from models.transaction import Transaction
from models.exercise import Exercise
from datetime import date, time



class Repository:
    
    def __init__(
        self,
        host: str="127.0.0.1",
        port: int=3306,
        user: str="root",
        password: str= os.getenv("MYSQL_PASSWORD"),
        database: str="journal_db",
        use_pool: bool=True,
        pool_name: str ="journal_pool",
        pool_size: int=5,
        ensure_schema: bool = True,
    )-> None:
        self._db_config: Dict[str,Any] = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
        }
        self._pool = None

        if use_pool:
            self._pool=pooling.MySQLConnectionPool(
                pool_name=pool_name,
                pool_size=pool_size,
                **self._db_config
            )
        if ensure_schema:
            self.ensure_table()

    #---------Connection Helpers--------------
    def _get_conn(self):
        return self._pool.get_connection() if self._pool else mysql.connector.connect(**self._db_config)

    def ensure_table(self)-> None:
        ddl_users= """
        CREATE TABLE IF NOT EXISTS users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        ddl_journal_day="""
        CREATE TABLE IF NOT EXISTS journal_day(
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        date DATE NOT NULL,
        mood VARCHAR(255),
        reflection VARCHAR(255)
        )"""
        ddl_song="""
        CREATE TABLE IF NOT EXISTS song(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        artist VARCHAR(255) NOT NULL,
        genre VARCHAR(50) NOT NULL
        )"""
        ddl_listening_session="""
        CREATE TABLE IF NOT EXISTS listening_session(
        id INT AUTO_INCREMENT PRIMARY KEY,
        journal_day_id INT,
        song_id INT,
        FOREIGN KEY (journal_day_id) REFERENCES journal_day(id),
        FOREIGN KEY (song_id) REFERENCES song(id),
        played_at TIME NOT NULL)"""

        ddl_transactions="""
        CREATE TABLE IF NOT EXISTS transactions(
        id INT AUTO_INCREMENT PRIMARY KEY,
        journal_day_id INT,
        FOREIGN KEY (journal_day_id) REFERENCES journal_day(id),
        name VARCHAR(50) NOT NULL,
        amount INT NOT NULL,
        category VARCHAR(50)
        )"""
        ddl_food="""
        CREATE TABLE IF NOT EXISTS food(
        id INT AUTO_INCREMENT PRIMARY KEY,
        journal_day_id INT,
        FOREIGN KEY (journal_day_id) REFERENCES journal_day(id),
        name VARCHAR(50) NOT NULL,
        calories INT NOT NULL,
        meal_type VARCHAR(10)
        )"""

        ddl_exercise="""
        CREATE TABLE IF NOT EXISTS exercise(
        id INT AUTO_INCREMENT PRIMARY KEY,
        journal_day_id INT,
        FOREIGN KEY (journal_day_id) REFERENCES journal_day(id),
        name VARCHAR(50) NOT NULL,
        duration INT NOT NULL,
        calories INT NOT NULL
        )"""
        

        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(ddl_users)
                cur.execute(ddl_journal_day)
                cur.execute(ddl_song)
                cur.execute(ddl_listening_session)
                cur.execute(ddl_transactions)
                cur.execute(ddl_food)
                cur.execute(ddl_exercise)
                conn.commit()
        finally:
            conn.close()

    #------------- CRUD FOR USERS ----------------

    def add_user(self, first_name: str, last_name: str, email: str, password_hash: str) -> User:
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = email.strip()

        insert_sql = """
            INSERT INTO users (first_name, last_name, email, password_hash)
            VALUES (%s, %s, %s, %s)
        """

        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(insert_sql, (first_name, last_name, email, password_hash))
                conn.commit()
                user_id = cur.lastrowid

                # fetch created_at
                cur.execute("SELECT created_at FROM users WHERE id = %s", (user_id,))
                created_at = cur.fetchone()[0]

                return User(
                    user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password_hash=password_hash,
                    created_at=created_at
                )
        finally:
            conn.close()


    def list_all_users(self) -> List[User]:
        select_sql = "SELECT id, first_name, last_name, email, password_hash, created_at FROM users"
        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(select_sql)
                rows = cur.fetchall()
                return [User(user_id=row[0], first_name=row[1], last_name=row[2], email=row[3], password_hash=row[4], created_at=row[5]) for row in rows]
        finally:
            conn.close()
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        select_sql = "SELECT id, first_name, last_name, email, password_hash, created_at FROM users WHERE id = %s"
        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(select_sql, (user_id,))
                row = cur.fetchone()
                if row:
                    return User(user_id=row[0], first_name=row[1], last_name=row[2], email=row[3], password_hash=row[4], created_at=row[5])
                return None
        finally:
            conn.close()
        
    def update_user_email(self, user_id: int, new_email: str) -> bool:
        update_sql = "UPDATE users SET email = %s WHERE id = %s"
        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(update_sql, (new_email, user_id))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()
    def delete_user(self, user_id: int) -> bool:
        delete_sql = "DELETE FROM users WHERE id = %s"
        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(delete_sql, (user_id,))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()
    def get_user_by_email(self, email: str) -> User | None:
        sql = """
            SELECT id, first_name, last_name, email, password_hash, created_at
            FROM users
            WHERE email = %s
        """

        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(sql, (email,))
                row = cur.fetchone()  # ⭐ THIS IS REQUIRED

                if row is None:
                    return None

                return User(
                    user_id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    email=row[3],
                    password_hash=row[4],
                    created_at=row[5]
                )
        finally:
            conn.close()

    def get_user_data_today(self, user_id: int):
        select_sql = """
            SELECT * FROM journal_day
            WHERE user_id = %s AND date = CURDATE()
        """
        conn = self._get_conn()
        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(select_sql, (user_id,))
                row = cur.fetchone()

                if row is None:
                    return None

                return JournalDay(
                    journal_day_id=row[0],
                    user_id=row[1],
                    date=row[2],
                    mood=row[3],
                    reflection=row[4]
                )
        finally:
            conn.close()
    def get_user_data(self, user_id: int):
        conn = self._get_conn()
        try:
            with conn.cursor(dictionary=True) as cur:

                # Get the journal_day id(s) for this user
                cur.execute("""
                    SELECT id, date, mood, reflection
                    FROM journal_day
                    WHERE user_id = %s
                    ORDER BY date DESC
                """, (user_id,))
                days = cur.fetchall()

                results = []

                for day in days:
                    day_id = day["id"]

                    # Food entries
                    cur.execute("""
                        SELECT name, calories, meal_type
                        FROM food
                        WHERE journal_day_id = %s
                    """, (day_id,))
                    food = cur.fetchall()

                    # Exercise entries
                    cur.execute("""
                        SELECT name, duration, calories
                        FROM exercise
                        WHERE journal_day_id = %s
                    """, (day_id,))
                    exercise = cur.fetchall()

                    # Transaction entries
                    cur.execute("""
                        SELECT name, amount, category
                        FROM transactions
                        WHERE journal_day_id = %s
                    """, (day_id,))
                    transactions = cur.fetchall()

                    results.append({
                        "journal_day": day,
                        "food": food,
                        "exercise": exercise,
                        "transactions": transactions
                    })

                return results

        finally:
            conn.close()
    #------------- CRUD FOR journal_day ----------------

    def add_journal_day(self, user_id: int, date: str, mood: str, reflection: str) -> JournalDay:
        insert_sql = """
            INSERT INTO journal_day (user_id, date, mood, reflection)
            VALUES (%s, %s, %s, %s)
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(insert_sql, (user_id, date, mood, reflection))
                conn.commit()
                journal_day_id = cur.lastrowid
                return journal_day_id

        finally:
            conn.close()

    def get_journal_id_by_date(self, user_id: int, date: str) -> Optional[int]:
        select_sql = """
            SELECT id FROM journal_day WHERE date = %s AND user_id = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(select_sql, (date, user_id))
                row = cur.fetchone()

                if row:
                    return row[0]   # journal_day_id
                else:
                    return None
        finally:
            conn.close()

    #------------- CRUD FOR Food ----------------
            
    def add_food(self, journal_day_id: int, name: str, calories: int, meal_type: str) -> Food:
        insert_sql = """
            INSERT INTO food (journal_day_id, name, calories, meal_type)
            VALUES (%s, %s, %s, %s)
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(insert_sql, (journal_day_id, name, calories, meal_type))
                conn.commit()
                food_id = cur.lastrowid
                return Food(food_id=food_id, journal_day_id=journal_day_id, name=name, calories=calories, meal_type=meal_type)
        finally:
            conn.close()

    def list_food_by_journal_day(self, journal_day_id: int) -> List[Food]:
        select_sql = """
            SELECT id, name, calories, meal_type FROM food WHERE journal_day_id = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(select_sql, (journal_day_id,))
                rows = cur.fetchall()
                return [Food(food_id=row[0], journal_day_id=journal_day_id, name=row[1], calories=row[2], meal_type=row[3]) for row in rows]
        finally:
            conn.close()

    def delete_food(self, food_id: int) -> bool:
        delete_sql = """
            DELETE FROM food WHERE id = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(delete_sql, (food_id,))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()

    #------------- CRUD FOR Transaction ----------------
    def add_transaction(self, journal_day_id: int, name: str, amount: int, category: str) -> Transaction:
        insert_sql = """
            INSERT INTO transactions (journal_day_id, name, amount, category)
            VALUES (%s, %s, %s, %s)
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(insert_sql, (journal_day_id, name, amount, category))
                conn.commit()
                transaction_id = cur.lastrowid
                return Transaction(transaction_id=transaction_id, journal_day_id=journal_day_id, name=name, amount=amount, category=category)
        finally:
            conn.close()

    def list_transactions_by_journal_day(self, journal_day_id: int) -> List[Transaction]:
        select_sql = """
            SELECT id, name, amount, category FROM transactions WHERE journal_day_id = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(select_sql, (journal_day_id,))
                rows = cur.fetchall()
                return [Transaction(transaction_id=row[0], journal_day_id=journal_day_id, name=row[1], amount=row[2], category=row[3]) for row in rows]
        finally:
            conn.close()

    def delete_transaction(self, transaction_id: int) -> bool:
        delete_sql = """
            DELETE FROM transactions WHERE id = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(delete_sql, (transaction_id,))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()

    #------------- CRUD FOR Exercise ----------------
    def add_exercise(self, journal_day_id: int, name: str, duration: int, calories: int) -> Exercise:
        insert_sql = """
            INSERT INTO exercise (journal_day_id, name, duration, calories)
            VALUES (%s, %s, %s, %s)
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(insert_sql, (journal_day_id, name, duration, calories))
                conn.commit()
                exercise_id = cur.lastrowid
                return Exercise(exercise_id=exercise_id, journal_day_id=journal_day_id, name=name, duration=duration, calories=calories)
        finally:
            conn.close()

    def list_exercises_by_journal_day(self, journal_day_id: int) -> List[Exercise]:
        select_sql = """
            SELECT id, name, duration, calories FROM exercise WHERE journal_day_id = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(select_sql, (journal_day_id,))
                rows = cur.fetchall()
                return [Exercise(exercise_id=row[0], journal_day_id=journal_day_id, name=row[1], duration=row[2], calories=row[3]) for row in rows]
        finally:
            conn.close()

    def delete_exercise(self, exercise_id: int) -> bool:
        delete_sql = """
            DELETE FROM exercise WHERE id = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(delete_sql, (exercise_id,))
                conn.commit()
                return cur.rowcount > 0
        finally:
            conn.close()
#------------- CRUD FOR Mood ----------------

    def add_mood(self, journal_day_id: int, user_id: int, mood: str, reflection: str) -> None:
        insert_sql = """
            INSERT INTO journal_day (id, user_id, date, mood, reflection)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE mood = %s, reflection = %s
        """

        conn = self._get_conn()

        try:
            with conn.cursor(buffered=True) as cur:
                cur.execute(
                    insert_sql,
                    (
                        journal_day_id,
                        user_id,
                        date.today(),
                        mood,
                        reflection,
                        mood,
                        reflection
                    )
                )
                conn.commit()
        finally:
            conn.close()