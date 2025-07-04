
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
    matches = user.get_matches()  # Use your User class method

    return render_template('dashboard.html', name=user.name, skills=skills, matches=matches)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
