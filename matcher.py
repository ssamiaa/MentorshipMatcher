import sqlite3

def get_users_by_role(role):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM users WHERE role = ?", (role,))
    users = c.fetchall()
    conn.close()
    return users  # List of (id, name)

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

def match_mentors_to_mentees():
    mentors = get_users_by_role('mentor')
    mentees = get_users_by_role('mentee')

    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    for mentor_id, mentor_name in mentors:
        mentor_skills = get_skills(mentor_id, 'has')

        for mentee_id, mentee_name in mentees:
            mentee_goals = get_skills(mentee_id, 'wants')
            score = calculate_score(mentor_skills, mentee_goals)

            if score > 0:
                c.execute(
                    "INSERT INTO matches (mentor_id, mentee_id, score) VALUES (?, ?, ?)",
                    (mentor_id, mentee_id, score)
                )
                print(f"Matched {mentor_name} with {mentee_name} (Score: {score})")

    conn.commit()
    conn.close()