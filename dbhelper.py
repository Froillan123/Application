import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'database.db'

def print_users():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        print("Current users in the database:")
        for user in users:
            print(user)  # Print each user

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')
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

        if user:
            print(f"User found: {user}")  # Debug: Print user information
            if check_password_hash(user[2], password):  # Verify the hashed password
                return user  # Return user data if password matches
            else:
                print("Password does not match!")  # Debug: Password mismatch
        else:
            print("User not found!")  # Debug: User not found
        return None  # Return None if username or password is incorrect
