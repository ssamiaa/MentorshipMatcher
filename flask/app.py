
import os
from models import User
from matcher import match_users_by_skills 
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3


app = Flask(__name__)
app.secret_key = 'dev'  # Needed for session
app.config['SESSION_TYPE'] = 'filesystem'

DB_PATH = 'mentorship.db'
print("🔍 Using database at:", DB_PATH)

def get_user_from_session():
    if 'user_id' not in session or 'user_name' not in session:
        return None
    return User(session['user_id'], session['user_name'], session.get('user_email', 'unknown@example.com'))


# Home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/browse-courses')
def browse_courses():
    user = get_user_from_session()
    if not user:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT courses.id, title, description, is_paid, price, accepts_skill_exchange, start_date, users.name
        FROM courses
        JOIN users ON courses.created_by = users.id
    ''')
    all_courses = c.fetchall()

    # Check enrollments
    c.execute("SELECT course_id FROM course_enrollments WHERE user_id = ?", (user.id,))
    enrolled_ids = set(r[0] for r in c.fetchall())
    conn.close()

    return render_template('browse_courses.html', courses=all_courses, enrolled_ids=enrolled_ids)
@app.route('/enroll/<int:course_id>', methods=['GET', 'POST'])
def enroll(course_id):
    user = get_user_from_session()
    if not user:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM courses WHERE id = ?", (course_id,))
    course = c.fetchone()

    if not course:
        conn.close()
        flash("Course not found.")
        return redirect(url_for('browse_courses'))

    # Prevent enrolling in your own course
    if course[3] == user.id:
        conn.close()
        flash("You cannot enroll in your own course.")
        return redirect(url_for('browse_courses'))

    if request.method == 'POST':
        name = request.form.get('name')
        billing = request.form.get('billing')
        payment_method = request.form.get('payment_method')
        card_number = request.form.get('card_number')
        expiry = request.form.get('expiry')
        cvv = request.form.get('cvv')
        upi = request.form.get('upi')

        if payment_method in ['visa', 'mastercard']:
            fake_payment_code = f"{payment_method.upper()}:{card_number}|{expiry}|{cvv}"
        elif payment_method in ['googlepay', 'paytm']:
            fake_payment_code = f"{payment_method.upper()}:{upi}"
        else:
            fake_payment_code = "UNKNOWN"

        # Insert into course_enrollments
        try:
            c.execute('''
                INSERT INTO course_enrollments (course_id, user_id, fake_payment_code)
                VALUES (?, ?, ?)
            ''', (course_id, user.id, fake_payment_code))
            conn.commit()
            flash("Successfully enrolled!")
        except sqlite3.IntegrityError:
            flash("You're already enrolled in this course.")

        conn.close()
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('enroll.html', course=course)

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()

        if not name or not email:
            flash('Name and email are required.')
            return redirect(url_for('signup'))

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            session['user_id'] = c.lastrowid
            session['user_name'] = name
            return redirect(url_for('dashboard'))
        except sqlite3.IntegrityError:
            flash("Email already registered.")
            return redirect(url_for('signup'))
        finally:
            conn.close()

    return render_template('signup.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, name FROM users WHERE email = ?", (email,))
        row = c.fetchone()
        conn.close()

        if row:
            session['user_id'] = row[0]
            session['user_name'] = row[1]
            return redirect(url_for('dashboard'))
        else:
            flash("No user found with that email.")
            return redirect(url_for('login'))

    return render_template('login.html')

# Dashboard (protected route)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = get_user_from_session()
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        skill = request.form['skill'].strip()
        skill_type = request.form['skill_type']
        if skill and skill_type in ['teach', 'learn']:
            user.add_skill(skill, skill_type)
            flash(f"Added skill '{skill}' to {skill_type}")

            # Call matching algorithm
            new_matches = match_users_by_skills()
            if new_matches:
                flash(f"{new_matches} new match(es) found!")

    skills = user.get_skills()
    matches = user.get_matches()  
    enrolled_courses = user.get_enrolled_courses()

    return render_template('dashboard.html', name=user.name, skills=skills, matches=matches, enrolled_courses=enrolled_courses)

# Create course page
@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    user = get_user_from_session()
    if not user:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title'].strip()
        description = request.form['description'].strip()
        is_paid = 1 if request.form.get('is_paid') == 'yes' else 0
        price = int(request.form.get('price', 0)) if is_paid else 0
        skill_exchange = 1 if request.form.get('skill_exchange') == 'yes' else 0
        start_date = request.form['start_date']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO courses (title, description, created_by, is_paid, price, accepts_skill_exchange, start_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, user.id, is_paid, price, skill_exchange, start_date))
        conn.commit()
        conn.close()
        flash("Course created successfully!")
        return redirect(url_for('dashboard'))

    return render_template('create_course.html')


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
