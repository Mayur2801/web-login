from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Simple in-memory user store (replace with DB for production)
users = {}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'message': 'Username and password are required.'}), 400

    if username in users:
        return jsonify({'success': False, 'message': 'Username already exists.'})

    users[username] = password
    return jsonify({'success': True})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if users.get(username) == password:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password.'})

@app.route('/landing')
def landing_page():
    # Sample car data
    cars = [
        {'name': 'Tesla Model S', 'info': 'Electric, 396 mi range, 0-60 mph in 1.99s'},
        {'name': 'Ford Mustang', 'info': 'Classic muscle car, V8 engine, great sound'},
        {'name': 'Chevrolet Camaro', 'info': 'Sporty, powerful engine, aggressive styling'},
        {'name': 'BMW M3', 'info': 'High performance, luxury, German engineering'},
    ]
    return render_template('landing.html', cars=cars)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
