# matcher.py
import sqlite3

# Match mentors and mentees based on overlapping skills
def match_users_by_skills():

    # - If a user teaches a skill that another user wants to learn, they are considered a match.
    # - Matches are stored (or updated) in the 'matches' table with a score (number of shared skills).
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    # Fetch all distinct mentor user IDs
    c.execute("SELECT DISTINCT user_id FROM skills WHERE type = 'teach'")
    mentors = [r[0] for r in c.fetchall()]

    # Fetch all distinct mentee user IDs
    c.execute("SELECT DISTINCT user_id FROM skills WHERE type = 'learn'")
    mentees = [r[0] for r in c.fetchall()]

    new_matches = 0

    # Iterate through each mentor
    for mentor_id in mentors:
         # Get the list of skills the mentor can teach
        c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'teach'", (mentor_id,))
        mentor_skills = set(r[0] for r in c.fetchall())

        # Compare with each mentee
        for mentee_id in mentees:
            if mentor_id == mentee_id:
                continue # Skip matching a user with themselves

             # Get the skills the mentee wants to learn
            c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'learn'", (mentee_id,))
            mentee_skills = set(r[0] for r in c.fetchall())

            # Find common skills between mentor and mentee
            common = mentor_skills & mentee_skills
            score = len(common) # Matching score = number of overlapping skills

            if score > 0:
                # Check if a match between this pair already exists
                c.execute('SELECT score FROM matches WHERE mentor_id = ? AND mentee_id = ?', (mentor_id, mentee_id))
                row = c.fetchone()

                if row:
                     # Update existing match with new score
                    c.execute('''
                        UPDATE matches SET score = ? WHERE mentor_id = ? AND mentee_id = ?
                    ''', (score, mentor_id, mentee_id))
                else:
                     # Insert new match record
                    c.execute('''
                        INSERT INTO matches (mentor_id, mentee_id, score)
                        VALUES (?, ?, ?)
                    ''', (mentor_id, mentee_id, score))
                new_matches += 1

    conn.commit()
    conn.close()
    return new_matches

# View match results for a specific user
def view_matches_for_user(user_id):
    # This function compares a given user’s teach/learn skills with all other users to determine:
    # - Who can teach them skills they want to learn.
    # - Who they can teach skills to.
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

     # Get the current user's teach skills
    c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'teach'", (user_id,))
    my_teach_skills = set(r[0] for r in c.fetchall())

    # Get the current user's learn skills
    c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'learn'", (user_id,))
    my_learn_skills = set(r[0] for r in c.fetchall())

    # Fetch all other users except the current user
    c.execute("SELECT id, name FROM users WHERE id != ?", (user_id,))
    others = c.fetchall()

    results = []

    for other_id, other_name in others:
        # Get the other user's teach skills
        c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'teach'", (other_id,))
        their_teach_skills = set(r[0] for r in c.fetchall())

        # Get the other user's learn skills
        c.execute("SELECT skill FROM skills WHERE user_id = ? AND type = 'learn'", (other_id,))
        their_learn_skills = set(r[0] for r in c.fetchall())

        # Determine mutual learning-teaching possibilities
        they_can_teach_me = list(their_teach_skills & my_learn_skills)
        i_can_teach_them = list(my_teach_skills & their_learn_skills)

        # Only add if there's a potential match
        if they_can_teach_me or i_can_teach_them:
            results.append((other_name, they_can_teach_me, i_can_teach_them))

    conn.close()
    # List of tuples: (other_user_name, skills_they_can_teach_me, skills_i_can_teach_them)
    return results
