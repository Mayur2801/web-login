from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Simple in-memory user store: {username: hashed_password}
users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('landing'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            flash('Username already exists', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        flash('Registration successful!', 'success')
        return render_template('success.html')

    return render_template('register.html')

@app.route('/landing')
def landing():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Example cars data
    cars = [
        {'name': 'Tesla Model S', 'year': 2023, 'desc': 'Electric luxury sedan', 'img': 'https://cdn.motor1.com/images/mgl/6jG60/s1/tesla-model-s.jpg'},
        {'name': 'Ford Mustang', 'year': 2022, 'desc': 'Iconic muscle car', 'img': 'https://cdn.motor1.com/images/mgl/Qg8XP/s1/2022-ford-mustang-gt.jpg'},
        {'name': 'BMW i8', 'year': 2021, 'desc': 'Hybrid sports car', 'img': 'https://cdn.motor1.com/images/mgl/zzd7p/s1/2021-bmw-i8.jpg'},
    ]
    return render_template('landing.html', cars=cars, username=session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
