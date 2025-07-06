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

    # Create the courses table - Stores information about courses created by users (mentors)
    c.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        created_by INTEGER NOT NULL,
        is_paid INTEGER NOT NULL CHECK (is_paid IN (0, 1)),
        price INTEGER DEFAULT 0,
        accepts_skill_exchange INTEGER NOT NULL CHECK (accepts_skill_exchange IN (0, 1)),
        start_date TEXT,
        FOREIGN KEY (created_by) REFERENCES users(id)
    );
    ''')

    # Create the course enrollment table - Tracks enrollments of users into courses, including payment info
    c.execute('''
    CREATE TABLE IF NOT EXISTS course_enrollments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        enrolled_on TEXT DEFAULT CURRENT_TIMESTAMP,
        fake_payment_code TEXT,
        FOREIGN KEY (course_id) REFERENCES courses(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')


    conn.commit()
    conn.close()
