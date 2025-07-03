import sqlite3

class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email

    def add_skill(self, skill, skill_type):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO skills (user_id, skill, type) VALUES (?, ?, ?)",
            (self.id, skill.lower().strip(), skill_type)
        )
        conn.commit()
        conn.close()

    def get_skills(self):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute("SELECT skill, type FROM skills WHERE user_id = ?", (self.id,))
        rows = c.fetchall()
        conn.close()
        return rows

    def get_matches(self):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute('''
            SELECT u.name, m.score
            FROM matches m
            JOIN users u
            ON (m.mentor_id = ? AND m.mentee_id = u.id)
            OR (m.mentee_id = ? AND m.mentor_id = u.id)
        ''', (self.id, self.id))
        rows = c.fetchall()
        conn.close()
        return rows
