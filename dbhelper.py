import sqlite3
import os

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            # Creating 'users' table
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT UNIQUE NOT NULL,
                                password TEXT NOT NULL)''')
            # You can add other tables here if needed
            conn.commit()

def create_user(username, password):
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False  # User already exists
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def get_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()  # Get the user data

        if user and user[2] == password:  # Verify the password
            return user  # Return user data if password matches
        return None  # Return None if username or password is incorrect
