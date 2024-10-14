from flask import Flask, render_template, request, redirect, url_for, session, flash
from dbhelper import create_user, get_user, init_db, print_users

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()  # Remove whitespace
        password = request.form['password'].strip()  # Remove whitespace
        
        print(f"Attempting to log in with username: '{username}' and password: '{password}'")  # Debug: Log login attempt
        
        user = get_user(username, password)
        if user:
            session['username'] = username
            print(f"Login successful for user: {username}")  # Debug: Successful login
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
            print("Invalid credentials!")  # Debug: Invalid credentials
            return redirect(url_for('home'))
    
    # Render the login form if it's a GET request
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()  # Remove whitespace
        password = request.form['password'].strip()  # Remove whitespace
        
        print(f"Registering user with username: '{username}' and password: '{password}'")  # Debug: Log registration attempt
        
        if create_user(username, password):
            flash('User registered successfully!')
            print_users()  # Debugging: Print users after registration
            return redirect(url_for('home'))
        else:
            flash('User already exists!')
            print("User already exists!")  # Debug: User already exists
            return redirect(url_for('home'))
    return render_template('register.html')  # Render registration form if GET request

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
