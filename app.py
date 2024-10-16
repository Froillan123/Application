from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dbhelper import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Initialize the database
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        
        user = get_user(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials! Please try again.')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()  # Remove whitespace
        password = request.form['password'].strip()  # Remove whitespace
        
        # Attempt to create a user
        if create_user(username, password):  # Assume create_user returns True on success
            flash('User registered successfully!', 'success')  # Success category
            return redirect(url_for('login'))  # Redirect to login
        else:
            flash('Username already exists! Please choose another one.', 'error')  # Error category

    # Render the registration template with flashed messages
    return render_template('register.html')




@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/data')
def data():
    conn = get_db_connection()
    data = conn.execute('SELECT * FROM your_table_name').fetchall()
    conn.close()
    if data:
        return jsonify([dict(row) for row in data])
    else:
        return jsonify([])  # Return an empty list if no data is found

if __name__ == '__main__':
    app.run(debug=True)
