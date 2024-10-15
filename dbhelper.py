import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()

            # Creating 'users' table (already present)
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL)''')

            # Creating 'your_table_name' table (or replace it with the actual name)
            cursor.execute('''CREATE TABLE IF NOT EXISTS your_table_name (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                column1 TEXT,
                                column2 TEXT)''')

            conn.commit()


def create_user(username, password):
    hashed_password = generate_password_hash(password)  # Hash the password
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # User already exists

def get_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()  # Get the user data

        if user and check_password_hash(user[2], password):  # Verify the hashed password
            return user  # Return user data if password matches
        return None  # Return None if username or password is incorrect
