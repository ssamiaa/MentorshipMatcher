import sqlite3

def get_all_users():
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM users")
    users = c.fetchall()
    conn.close()
    return users
def get_skills(user_id, skill_type):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = ?", (user_id, skill_type))
    skills = [row[0] for row in c.fetchall()]
    conn.close()
    return skills

def calculate_score(mentor_skills, mentee_goals):
    shared = set(mentor_skills).intersection(set(mentee_goals))
    return len(shared)  # 1 point per shared skill

def match_users_by_skills():
    users = get_all_users()
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    for mentor_id, mentor_name in users:
        mentor_skills = get_skills(mentor_id, 'has')
        if not mentor_skills:
            continue  # skip if this user can't teach anything

        for mentee_id, mentee_name in users:
            if mentor_id == mentee_id:
                continue  # don't match with self

            mentee_goals = get_skills(mentee_id, 'wants')
            if not mentee_goals:
                continue

            score = calculate_score(mentor_skills, mentee_goals)
            if score > 0:
                c.execute("SELECT 1 FROM matches WHERE mentor_id = ? AND mentee_id = ?", (mentor_id, mentee_id))
                if c.fetchone() is None:
                    c.execute("INSERT INTO matches (mentor_id, mentee_id, score) VALUES (?, ?, ?)", (mentor_id, mentee_id, score))
                    print(f"Matched {mentor_name} → {mentee_name} (Score: {score})")

    conn.commit()
    conn.close()