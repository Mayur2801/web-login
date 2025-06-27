@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        if not username or not password:
            flash(('error', 'Username and password are required.'))
            return redirect('/register')

        if username in users:
            flash(('error', 'Username already exists.'))
            return redirect('/register')

        users[username] = password
        flash(('success', 'Registration successful. Please log in.'))
        return redirect('/login')
    
    return render_template('register.html')
