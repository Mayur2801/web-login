from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production!

# In-memory user store (username -> password)
users = {
    'admin': 'admin123',
    'user': 'user123'
}

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('cars'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['user'] = uname
            return redirect(url_for('cars'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users:
            flash('Username already exists')
        else:
            users[uname] = pwd
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/cars')
def cars():
    if 'user' not in session:
        return redirect(url_for('login'))

    car_data = [
        {'name': 'Tesla Model S', 'image': 'https://tesla-cdn.thron.com/delivery/public/image/tesla/3dc2453c-4d4c-4b9e-a3ae-2c59220b19b3/bvlatuR/std/1920x1080/_25-Hero-D', 'info': 'Electric, 396 mi range'},
        {'name': 'BMW M4', 'image': 'https://cdn.bmwblog.com/wp-content/uploads/2021/03/BMW-M4-G82-Competition-Coupé-images-22.jpg', 'info': '503 hp, Twin-turbo inline-6'},
        {'name': 'Lamborghini Huracán', 'image': 'https://cdn.motor1.com/images/mgl/8OqKp/s1/lamborghini-huracan-evo-rwd-spyder.jpg', 'info': 'V10, 602 hp'}
    ]

    return render_template('cars.html', cars=car_data)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
