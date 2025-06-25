import sqlite3

def init_db(): 
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    # Create the 'users' table to store basic user info
    # Each user has an id, name, email, and role (either mentor or mentee)
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT CHECK(role IN ('mentor', 'mentee')) NOT NULL
    )
    ''')

    # Create the 'skills' table to track what users can teach or want to learn
    # Each entry is linked to a user by user_id
    c.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        skill TEXT,
        type TEXT CHECK(type IN ('has', 'wants')),
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')

    # Create the 'matches' table to store mentor-mentee pairs
    c.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY,
        mentor_id INTEGER,
        mentee_id INTEGER,
        score INTEGER,
        FOREIGN KEY(mentor_id) REFERENCES users(id),
        FOREIGN KEY(mentee_id) REFERENCES users(id)
    )
    ''')

    conn.commit()
    conn.close()