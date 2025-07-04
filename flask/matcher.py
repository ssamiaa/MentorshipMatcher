# matcher.py
import sqlite3

def match_users_by_skills():
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    c.execute("SELECT DISTINCT user_id FROM skills WHERE type = 'teach'")
    mentors = [r[0] for r in c.fetchall()]

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
                c.execute('SELECT score FROM matches WHERE mentor_id = ? AND mentee_id = ?', (mentor_id, mentee_id))
                row = c.fetchone()

                if row:
                    # Always update with fresh score
                    c.execute('''
                        UPDATE matches SET score = ? WHERE mentor_id = ? AND mentee_id = ?
                    ''', (score, mentor_id, mentee_id))
                else:
                    c.execute('''
                        INSERT INTO matches (mentor_id, mentee_id, score)
                        VALUES (?, ?, ?)
                    ''', (mentor_id, mentee_id, score))
                new_matches += 1

    conn.commit()
    conn.close()
    return new_matches

def view_matches_for_user(user_id):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'teach'", (user_id,))
    my_teach_skills = set(r[0] for r in c.fetchall())

    c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'learn'", (user_id,))
    my_learn_skills = set(r[0] for r in c.fetchall())

    c.execute("SELECT id, name FROM users WHERE id != ?", (user_id,))
    others = c.fetchall()

    results = []

    for other_id, other_name in others:
        c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'teach'", (other_id,))
        their_teach_skills = set(r[0] for r in c.fetchall())

        c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'learn'", (other_id,))
        their_learn_skills = set(r[0] for r in c.fetchall())

        they_can_teach_me = list(their_teach_skills & my_learn_skills)
        i_can_teach_them = list(my_teach_skills & their_learn_skills)

        # Always return three values, even if some lists are empty
        if they_can_teach_me or i_can_teach_them:
            results.append((other_name, they_can_teach_me, i_can_teach_them))

    conn.close()
    return results
