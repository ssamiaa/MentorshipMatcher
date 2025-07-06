import sqlite3
from matcher import view_matches_for_user  

# Represents a user in the mentorship platform
class User:

    # Initialize a User instance with ID, name, and email.
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email


    # Add a skill to the database for this user.
    # skill_type must be either 'teach' or 'learn'.
    def add_skill(self, skill, skill_type):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute("INSERT INTO skills (user_id, skill, type) VALUES (?, ?, ?)",
                  (self.id, skill, skill_type))
        conn.commit()
        conn.close()



    # Retrieve a list of this user's skills from the database.
    def get_skills(self):
        conn = sqlite3.connect('mentorship.db')
        c = conn.cursor()
        c.execute("SELECT skill, type FROM skills WHERE user_id = ?", (self.id,))
        skills = c.fetchall()
        conn.close()
        # Returns: List of tuples [(skill_name, skill_type), ...]
        return skills

    # Use the matching algorithm to retrieve users matched with this user.
    def get_matches(self):
        # Returns: List of matched user data (delegated to matcher.py)
        return view_matches_for_user(self.id)
    
    # Fetch all courses this user is enrolled in, including:
    #     - course title
    #     - course start date
    #     - instructor name
    #     - fake payment code (if applicable)
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
        # Returns: List of tuples [(title, start_date, instructor_name, fake_payment_code), ...]
        return data 
