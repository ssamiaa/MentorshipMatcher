import sqlite3

def init_db():
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    # Create the 'users' table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    ''')

    # Create the 'skills' table to track teaching ('has') or learning ('wants') skills
    c.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        type TEXT CHECK(type IN ('teach', 'learn')) NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    );
    ''')

    # Create the 'matches' table to track mentor–mentee matches with a match score
    c.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mentor_id INTEGER NOT NULL,
        mentee_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        FOREIGN KEY(mentor_id) REFERENCES users(id),
        FOREIGN KEY(mentee_id) REFERENCES users(id),
        UNIQUE(mentor_id, mentee_id)  -- prevent duplicates
    );
    ''')

    conn.commit()
    conn.close()
