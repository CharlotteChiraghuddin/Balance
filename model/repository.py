import mysql.connector
from mysql.connector import pooling, Error
import os
from typing import List, Optional, Any, Dict


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
        email VARCHAR(255) NOT NULL
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

        conn = self._get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(ddl_users)
                cur.execute(ddl_journal_day)
                cur.execute(ddl_song)
                cur.execute(ddl_listening_session)
                cur.execute(ddl_transactions)
                conn.commit()
        finally:
            conn.close()

