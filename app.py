from flask import Flask, render_template, request, redirect, url_for, session, flash
from dbhelper import create_user, get_user, init_db

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
        username = request.form['username'].strip()  # Remove whitespace
        password = request.form['password'].strip()  # Remove whitespace
        
        user = get_user(username, password)
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()  # Remove whitespace
        password = request.form['password'].strip()  # Remove whitespace
        
        if create_user(username, password):
            flash('User registered successfully!')
            return redirect(url_for('login'))
        else:
            flash('Username already exists! Please choose another one.')
            return redirect(url_for('register'))

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

if __name__ == '__main__':
    app.run(debug=True)
    