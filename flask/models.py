import sqlite3
from matcher import view_matches_for_user  

class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

    def add_skill(self, skill, skill_type):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute("INSERT INTO skills (user_id, skill, type) VALUES (?, ?, ?)",
                  (self.id, skill, skill_type))
        conn.commit()
        conn.close()

    def get_skills(self):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute("SELECT skill, type FROM skills WHERE user_id = ?", (self.id,))
        skills = c.fetchall()
        conn.close()
        return skills

    def get_matches(self):
        return view_matches_for_user(self.id)
    
    def get_enrolled_courses(self):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute('''
            SELECT courses.title, courses.start_date, users.name, course_enrollments.fake_payment_code
            FROM course_enrollments
            JOIN courses ON course_enrollments.course_id = courses.id
            JOIN users ON courses.created_by = users.id
            WHERE course_enrollments.user_id = ?
        ''', (self.id,))
        data = c.fetchall()
        conn.close()
        return data  # [(title, start_date, instructor, fake_payment_code), ...]
