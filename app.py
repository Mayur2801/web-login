from flask import Flask, render_template, request, redirect, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# In-memory user storage (use a DB in production)
users = {}

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            return render_template('dashboard.html', username=uname)
        else:
            flash(('error', 'Invalid username or password'))
            return redirect('/login')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users:
            flash(('error', 'Username already exists'))
            return redirect('/register')
        users[uname] = pwd
        flash(('success', 'Registration successful! Please log in.'))
        return redirect('/login')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
