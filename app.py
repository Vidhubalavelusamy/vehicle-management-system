from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize DB
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        email TEXT UNIQUE,
                        password TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        email TEXT,
                        vehicle_name TEXT,
                        vehicle_model TEXT,
                        registration_number TEXT,
                        fault_description TEXT,
                        image TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if existing_user:
            conn.close()
            flash("User already exists.")
            return redirect(url_for('register'))

        conn.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                     (username, email, password))
        conn.commit()
        conn.close()
        flash("Registered successfully. Please log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form.get('email')
        password = request.form.get('password')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE (username = ? OR email = ?) AND password = ?',
                            (login_id, login_id, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash("Login successful.")
            return redirect(url_for('vehicles'))
        else:
            flash("Invalid credentials.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('login'))

@app.route('/vehicles')
def vehicles():
    conn = get_db_connection()
    vehicles = conn.execute('SELECT * FROM vehicles').fetchall()
    conn.close()
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/add_vehicle', methods=['GET', 'POST'])
def add_vehicle():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        vehicle_name = request.form.get('vehicle_name')
        vehicle_model = request.form.get('vehicle_model')
        registration_number = request.form.get('registration_number')
        fault_description = request.form.get('fault_description')

        # Handle image upload
        image = request.files.get('vehicle_image')
        image_filename = None
        if image and image.filename != '':
            image_filename = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_filename)

        # Save vehicle data
        conn = get_db_connection()
        conn.execute('''INSERT INTO vehicles (username, email, vehicle_name, vehicle_model, registration_number, fault_description, image)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                     (username, email, vehicle_name, vehicle_model, registration_number, fault_description, image_filename))
        conn.commit()
        conn.close()

        flash("Vehicle added successfully!")
        return redirect(url_for('vehicles'))

    return render_template('add_vehicle.html')

@app.route('/analytics')
def analytics():
    conn = get_db_connection()
    count = conn.execute('SELECT COUNT(*) FROM vehicles').fetchone()[0]
    conn.close()
    return render_template('analytics.html', count=count)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


