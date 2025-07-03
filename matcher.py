# matcher.py
import sqlite3

def match_users_by_skills():
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    # Find all users with teach skills
    c.execute("SELECT DISTINCT user_id FROM skills WHERE type = 'teach'")
    mentors = [r[0] for r in c.fetchall()]

    # Find all users with learn skills
    c.execute("SELECT DISTINCT user_id FROM skills WHERE type = 'learn'")
    mentees = [r[0] for r in c.fetchall()]

    new_matches = 0

    for mentor_id in mentors:
        c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'teach'", (mentor_id,))
        mentor_skills = set(r[0] for r in c.fetchall())

        for mentee_id in mentees:
            if mentor_id == mentee_id:
                continue

            c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'learn'", (mentee_id,))
            mentee_skills = set(r[0] for r in c.fetchall())

            common = mentor_skills & mentee_skills
            score = len(common)

            if score > 0:
                # Insert or update the match
                c.execute('''
                    INSERT INTO matches (mentor_id, mentee_id, score)
                    VALUES (?, ?, ?)
                    ON CONFLICT(mentor_id, mentee_id)
                    DO UPDATE SET score=excluded.score
                ''', (mentor_id, mentee_id, score))
                new_matches += 1

    conn.commit()
    conn.close()
    return new_matches
def view_matches_for_user(user_id):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute('''
        SELECT u.name, m.score
        FROM matches m
        JOIN users u
            ON (m.mentor_id = ? AND m.mentee_id = u.id)
            OR (m.mentee_id = ? AND m.mentor_id = u.id)
    ''', (user_id, user_id))
    rows = c.fetchall()
    conn.close()
    return rows

