import os
from typing import List, Optional, Any, Dict
from datetime import date, time

from models.users import User
from models.journal_day import JournalDay
from models.food import Food
from models.transaction import Transaction
from models.exercise import Exercise

from sqlalchemy import create_engine, text

# Read the PostgreSQL connection URL from Render
db_url = os.getenv("DATABASE_URL")

# Create a global SQLAlchemy engine
engine = create_engine(db_url)




class Repository:

    def __init__(self):
        # No MySQL config, no pooling, no host/port/user/password
        # SQLAlchemy engine is already created globally at the top of the file
        pass

    #---------Connection Helpers--------------
    def _get_conn(self):
        # SQLAlchemy uses engine.connect() instead of MySQL pools
        return engine.connect()

    def ensure_table(self) -> None:
        # PostgreSQL-compatible DDL (AUTO_INCREMENT → SERIAL, VARCHAR stays fine)
        ddl_users = """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """

        ddl_journal_day = """
        CREATE TABLE IF NOT EXISTS journal_day(
            id SERIAL PRIMARY KEY,
            user_id INT REFERENCES users(id),
            date DATE NOT NULL,
            mood VARCHAR(255),
            reflection VARCHAR(255)
        );
        """

        ddl_song = """
        CREATE TABLE IF NOT EXISTS song(
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            artist VARCHAR(255) NOT NULL,
            genre VARCHAR(50) NOT NULL
        );
        """

        ddl_listening_session = """
        CREATE TABLE IF NOT EXISTS listening_session(
            id SERIAL PRIMARY KEY,
            journal_day_id INT REFERENCES journal_day(id),
            song_id INT REFERENCES song(id),
            played_at TIME NOT NULL
        );
        """

        ddl_transactions = """
        CREATE TABLE IF NOT EXISTS transactions(
            id SERIAL PRIMARY KEY,
            journal_day_id INT REFERENCES journal_day(id),
            name VARCHAR(50) NOT NULL,
            amount INT NOT NULL,
            category VARCHAR(50)
        );
        """

        ddl_food = """
        CREATE TABLE IF NOT EXISTS food(
            id SERIAL PRIMARY KEY,
            journal_day_id INT REFERENCES journal_day(id),
            name VARCHAR(50) NOT NULL,
            calories INT NOT NULL,
            meal_type VARCHAR(10)
        );
        """

        ddl_exercise = """
        CREATE TABLE IF NOT EXISTS exercise(
            id SERIAL PRIMARY KEY,
            journal_day_id INT REFERENCES journal_day(id),
            name VARCHAR(50) NOT NULL,
            duration INT NOT NULL,
            calories INT NOT NULL
        );
        """

        # Execute all DDL statements using SQLAlchemy
        with engine.begin() as conn:
            conn.execute(text(ddl_users))
            conn.execute(text(ddl_journal_day))
            conn.execute(text(ddl_song))
            conn.execute(text(ddl_listening_session))
            conn.execute(text(ddl_transactions))
            conn.execute(text(ddl_food))
            conn.execute(text(ddl_exercise))

    #------------- CRUD FOR USERS ----------------

    def add_user(self, first_name: str, last_name: str, email: str, password_hash: str) -> User:
        first_name = first_name.strip()
        last_name = last_name.strip()
        email = email.strip()

        insert_sql = """
            INSERT INTO users (first_name, last_name, email, password_hash)
            VALUES (:first_name, :last_name, :email, :password_hash)
            RETURNING id, created_at;
        """

        with engine.begin() as conn:
            result = conn.execute(
                text(insert_sql),
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password_hash": password_hash
                }
            )

            row = result.fetchone()
            user_id = row.id
            created_at = row.created_at

            return User(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=password_hash,
                created_at=created_at
            )

    #------------- CRUD FOR USERS ----------------

    def list_all_users(self) -> List[User]:
        sql = """
            SELECT id, first_name, last_name, email, password_hash, created_at
            FROM users
        """

        with engine.connect() as conn:
            result = conn.execute(text(sql))
            rows = result.fetchall()

            return [
                User(
                    user_id=row.id,
                    first_name=row.first_name,
                    last_name=row.last_name,
                    email=row.email,
                    password_hash=row.password_hash,
                    created_at=row.created_at
                )
                for row in rows
            ]


    def get_user_by_id(self, user_id: int) -> Optional[User]:
        sql = """
            SELECT id, first_name, last_name, email, password_hash, created_at
            FROM users
            WHERE id = :user_id
        """

        with engine.connect() as conn:
            result = conn.execute(text(sql), {"user_id": user_id})
            row = result.fetchone()

            if row is None:
                return None

            return User(
                user_id=row.id,
                first_name=row.first_name,
                last_name=row.last_name,
                email=row.email,
                password_hash=row.password_hash,
                created_at=row.created_at
            )


    def update_user_email(self, user_id: int, new_email: str) -> bool:
        sql = """
            UPDATE users
            SET email = :email
            WHERE id = :user_id
        """

        with engine.begin() as conn:
            result = conn.execute(
                text(sql),
                {"email": new_email, "user_id": user_id}
            )

            return result.rowcount > 0


    def delete_user(self, user_id: int) -> bool:
        sql = """
            DELETE FROM users
            WHERE id = :user_id
        """

        with engine.begin() as conn:
            result = conn.execute(text(sql), {"user_id": user_id})
            return result.rowcount > 0


    def get_user_by_email(self, email: str) -> Optional[User]:
        sql = """
            SELECT id, first_name, last_name, email, password_hash, created_at
            FROM users
            WHERE email = :email
        """

        with engine.connect() as conn:
            result = conn.execute(text(sql), {"email": email})
            row = result.fetchone()

            if row is None:
                return None

            return User(
                user_id=row.id,
                first_name=row.first_name,
                last_name=row.last_name,
                email=row.email,
                password_hash=row.password_hash,
                created_at=row.created_at
            )


    def get_user_data_week(self, user_id: int):
        sql = """
            SELECT id, user_id, date, mood, reflection
            FROM journal_day
            WHERE user_id = :user_id
            AND date >= CURRENT_DATE - INTERVAL '7 days'
            ORDER BY date DESC
        """

        with engine.connect() as conn:
            result = conn.execute(text(sql), {"user_id": user_id})
            rows = result.fetchall()

            if not rows:
                return []

            week = []
            for row in rows:
                week.append(JournalDay(
                    journal_day_id=row.id,
                    user_id=row.user_id,
                    date=row.date,
                    mood=row.mood,
                    reflection=row.reflection
                ))

            return week

    def get_user_data_daily(self, user_id: int):
        with engine.connect() as conn:

            # Get today's journal_day entry
            days_sql = """
                SELECT id, date, mood, reflection
                FROM journal_day
                WHERE user_id = :user_id
                AND date = CURRENT_DATE
                ORDER BY date DESC
            """

            days = conn.execute(text(days_sql), {"user_id": user_id}).fetchall()
            results = []

            for day in days:
                day_id = day.id

                food = conn.execute(
                    text("SELECT name, calories, meal_type FROM food WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                exercise = conn.execute(
                    text("SELECT name, duration, calories FROM exercise WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                transactions = conn.execute(
                    text("SELECT name, amount, category FROM transactions WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                results.append({
                    "journal_day": {
                        "id": day.id,
                        "date": day.date,
                        "mood": day.mood,
                        "reflection": day.reflection
                    },
                    "food": [dict(row) for row in food],
                    "exercise": [dict(row) for row in exercise],
                    "transactions": [dict(row) for row in transactions]
                })

            return results
        
    def get_user_data_weekly(self, user_id: int):
        with engine.connect() as conn:

            days_sql = """
                SELECT id, date, mood, reflection
                FROM journal_day
                WHERE user_id = :user_id
                AND date >= CURRENT_DATE - INTERVAL '7 days'
                ORDER BY date DESC
            """

            days = conn.execute(text(days_sql), {"user_id": user_id}).fetchall()
            results = []

            for day in days:
                day_id = day.id

                food = conn.execute(
                    text("SELECT name, calories, meal_type FROM food WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                exercise = conn.execute(
                    text("SELECT name, duration, calories FROM exercise WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                transactions = conn.execute(
                    text("SELECT name, amount, category FROM transactions WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                results.append({
                    "journal_day": {
                        "id": day.id,
                        "date": day.date,
                        "mood": day.mood,
                        "reflection": day.reflection
                    },
                    "food": [dict(row) for row in food],
                    "exercise": [dict(row) for row in exercise],
                    "transactions": [dict(row) for row in transactions]
                })

            return results
 
    def get_user_data_monthly(self, user_id: int):
        with engine.connect() as conn:

            # Get the last month of journal_day entries
            days_sql = """
                SELECT id, date, mood, reflection
                FROM journal_day
                WHERE user_id = :user_id
                AND date >= CURRENT_DATE - INTERVAL '1 month'
                ORDER BY date DESC
            """

            days = conn.execute(text(days_sql), {"user_id": user_id}).fetchall()
            results = []

            for day in days:
                day_id = day.id

                food = conn.execute(
                    text("SELECT name, calories, meal_type FROM food WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                exercise = conn.execute(
                    text("SELECT name, duration, calories FROM exercise WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                transactions = conn.execute(
                    text("SELECT name, amount, category FROM transactions WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                results.append({
                    "journal_day": {
                        "id": day.id,
                        "date": day.date,
                        "mood": day.mood,
                        "reflection": day.reflection
                    },
                    "food": [dict(row) for row in food],
                    "exercise": [dict(row) for row in exercise],
                    "transactions": [dict(row) for row in transactions]
                })

            return results

    def get_user_data_yearly(self, user_id: int):
        with engine.connect() as conn:

            # Get the last year of journal_day entries
            days_sql = """
                SELECT id, date, mood, reflection
                FROM journal_day
                WHERE user_id = :user_id
                AND date >= CURRENT_DATE - INTERVAL '1 year'
                ORDER BY date DESC
            """

            days = conn.execute(text(days_sql), {"user_id": user_id}).fetchall()
            results = []

            for day in days:
                day_id = day.id

                food = conn.execute(
                    text("SELECT name, calories, meal_type FROM food WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                exercise = conn.execute(
                    text("SELECT name, duration, calories FROM exercise WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                transactions = conn.execute(
                    text("SELECT name, amount, category FROM transactions WHERE journal_day_id = :id"),
                    {"id": day_id}
                ).fetchall()

                results.append({
                    "journal_day": {
                        "id": day.id,
                        "date": day.date,
                        "mood": day.mood,
                        "reflection": day.reflection
                    },
                    "food": [dict(row) for row in food],
                    "exercise": [dict(row) for row in exercise],
                    "transactions": [dict(row) for row in transactions]
                })

            return results
        
    #------------- CRUD FOR journal_day ----------------

    def add_journal_day(self, user_id: int, date: str, mood: str, reflection: str) -> JournalDay:
        sql = """
            INSERT INTO journal_day (user_id, date, mood, reflection)
            VALUES (:user_id, :date, :mood, :reflection)
            RETURNING id;
        """

        with engine.begin() as conn:
            result = conn.execute(
                text(sql),
                {"user_id": user_id, "date": date, "mood": mood, "reflection": reflection}
            )
            journal_day_id = result.scalar()
            return journal_day_id
        
    def get_journal_id_by_date(self, user_id: int, date: str) -> Optional[int]:
        sql = """
            SELECT id FROM journal_day
            WHERE date = :date AND user_id = :user_id
        """

        with engine.connect() as conn:
            row = conn.execute(text(sql), {"date": date, "user_id": user_id}).fetchone()
            return row.id if row else None


    #------------- CRUD FOR Food ----------------
            
    def add_food(self, journal_day_id: int, name: str, calories: int, meal_type: str) -> Food:
        sql = """
            INSERT INTO food (journal_day_id, name, calories, meal_type)
            VALUES (:journal_day_id, :name, :calories, :meal_type)
            RETURNING id;
        """

        with engine.begin() as conn:
            result = conn.execute(
                text(sql),
                {
                    "journal_day_id": journal_day_id,
                    "name": name,
                    "calories": calories,
                    "meal_type": meal_type
                }
            )
            food_id = result.scalar()
            return Food(food_id=food_id, journal_day_id=journal_day_id, name=name, calories=calories, meal_type=meal_type)

    def list_food_by_journal_day(self, journal_day_id: int) -> List[Food]:
        sql = """
            SELECT id, name, calories, meal_type
            FROM food
            WHERE journal_day_id = :journal_day_id
        """

        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"journal_day_id": journal_day_id}).fetchall()
            return [
                Food(food_id=row.id, journal_day_id=journal_day_id, name=row.name, calories=row.calories, meal_type=row.meal_type)
                for row in rows
            ]

    def list_food_by_week(self, user_id: int) -> List[Food]:
        sql = """
            SELECT f.id, f.journal_day_id, f.name, f.calories, f.meal_type
            FROM food f
            JOIN journal_day jd ON f.journal_day_id = jd.id
            WHERE jd.user_id = :user_id
            AND jd.date >= CURRENT_DATE - INTERVAL '7 days'
        """

        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"user_id": user_id}).fetchall()
            return [
                Food(food_id=row.id, journal_day_id=row.journal_day_id, name=row.name, calories=row.calories, meal_type=row.meal_type)
                for row in rows
            ]

            
    def delete_food(self, food_id: int) -> bool:
        sql = "DELETE FROM food WHERE id = :id"

        with engine.begin() as conn:
            result = conn.execute(text(sql), {"id": food_id})
            return result.rowcount > 0


    #------------- CRUD FOR Transaction ----------------
    def add_transaction(self, journal_day_id: int, name: str, amount: int, category: str) -> Transaction:
        sql = """
            INSERT INTO transactions (journal_day_id, name, amount, category)
            VALUES (:journal_day_id, :name, :amount, :category)
            RETURNING id;
        """

        with engine.begin() as conn:
            result = conn.execute(
                text(sql),
                {
                    "journal_day_id": journal_day_id,
                    "name": name,
                    "amount": amount,
                    "category": category
                }
            )
            transaction_id = result.scalar()
            return Transaction(transaction_id=transaction_id, journal_day_id=journal_day_id, name=name, amount=amount, category=category)

    def list_transactions_by_journal_day(self, journal_day_id: int) -> List[Transaction]:
        sql = """
            SELECT id, name, amount, category
            FROM transactions
            WHERE journal_day_id = :journal_day_id
        """

        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"journal_day_id": journal_day_id}).fetchall()
            return [
                Transaction(transaction_id=row.id, journal_day_id=journal_day_id, name=row.name, amount=row.amount, category=row.category)
                for row in rows
            ]

    def list_transactions_by_week(self, user_id: int) -> List[Transaction]:
        sql = """
            SELECT t.id, t.journal_day_id, t.name, t.amount, t.category
            FROM transactions t
            JOIN journal_day jd ON t.journal_day_id = jd.id
            WHERE jd.user_id = :user_id
            AND jd.date >= CURRENT_DATE - INTERVAL '7 days'
        """

        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"user_id": user_id}).fetchall()
            return [
                Transaction(transaction_id=row.id, journal_day_id=row.journal_day_id, name=row.name, amount=row.amount, category=row.category)
                for row in rows
            ]

    def delete_transaction(self, transaction_id: int) -> bool:
        sql = "DELETE FROM transactions WHERE id = :id"

        with engine.begin() as conn:
            result = conn.execute(text(sql), {"id": transaction_id})
            return result.rowcount > 0


    #------------- CRUD FOR Exercise ----------------
    def add_exercise(self, journal_day_id: int, name: str, duration: int, calories: int) -> Exercise:
        sql = """
            INSERT INTO exercise (journal_day_id, name, duration, calories)
            VALUES (:journal_day_id, :name, :duration, :calories)
            RETURNING id;
        """

        with engine.begin() as conn:
            result = conn.execute(
                text(sql),
                {
                    "journal_day_id": journal_day_id,
                    "name": name,
                    "duration": duration,
                    "calories": calories
                }
            )
            exercise_id = result.scalar()
            return Exercise(exercise_id=exercise_id, journal_day_id=journal_day_id, name=name, duration=duration, calories=calories)

    def list_exercises_by_journal_day(self, journal_day_id: int) -> List[Exercise]:
        sql = """
            SELECT id, name, duration, calories
            FROM exercise
            WHERE journal_day_id = :journal_day_id
        """

        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"journal_day_id": journal_day_id}).fetchall()
            return [
                Exercise(exercise_id=row.id, journal_day_id=journal_day_id, name=row.name, duration=row.duration, calories=row.calories)
                for row in rows
            ]

    def delete_exercise(self, exercise_id: int) -> bool:
        sql = "DELETE FROM exercise WHERE id = :id"

        with engine.begin() as conn:
            result = conn.execute(text(sql), {"id": exercise_id})
            return result.rowcount > 0

            
    def list_exercise_by_week(self, user_id: int) -> List[Exercise]:
        sql = """
            SELECT e.id, e.journal_day_id, e.name, e.duration, e.calories
            FROM exercise e
            JOIN journal_day jd ON e.journal_day_id = jd.id
            WHERE jd.user_id = :user_id
            AND jd.date >= CURRENT_DATE - INTERVAL '7 days'
        """

        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"user_id": user_id}).fetchall()
            return [
                Exercise(exercise_id=row.id, journal_day_id=row.journal_day_id, name=row.name, duration=row.duration, calories=row.calories)
                for row in rows
            ]

#------------- CRUD FOR Mood ----------------

    def add_mood(self, journal_day_id: int, user_id: int, mood: str, reflection: str) -> None:
        sql = """
            INSERT INTO journal_day (id, user_id, date, mood, reflection)
            VALUES (:id, :user_id, CURRENT_DATE, :mood, :reflection)
            ON CONFLICT (id)
            DO UPDATE SET mood = EXCLUDED.mood,
                          reflection = EXCLUDED.reflection;
        """

        with engine.begin() as conn:
            conn.execute(
                text(sql),
                {
                    "id": journal_day_id,
                    "user_id": user_id,
                    "mood": mood,
                    "reflection": reflection
                }
            )

        
    def list_mood_by_week(self, user_id: int) -> List[str]:
        sql = """
            SELECT mood
            FROM journal_day
            WHERE user_id = :user_id
            AND date >= CURRENT_DATE - INTERVAL '7 days'
        """

        with engine.connect() as conn:
            rows = conn.execute(text(sql), {"user_id": user_id}).fetchall()
            return [row.mood for row in rows]
