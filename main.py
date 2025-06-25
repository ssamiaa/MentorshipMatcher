from database import init_db 
import sqlite3

def add_user():
    name = input("Name: ")
    email = input("Email: ")
    role = input("Role (mentor or mentee): ")

    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()

    c.execute("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", (name, email, role))
    conn.commit()
    conn.close()

def add_skills(user_id, skill_type):
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    while True: 
        skill = input(f"Enter skill to {'teach' if skill_type == 'has' else 'learn'} (or 'done'): ")
        if skill == 'done':
            break
        c.execute("INSERT INTO skills (user_id, skill, type) VALUES (?, ?, ?)", (user_id, skill, skill_type))

    conn.commit()
    conn.close

def get_users():
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    for row in c.execute("SELECT id, name, role FROM users"):
        print(row)
    conn.close()

# Initialize
if __name__ == "__main__":
    init_db()
    print("1. Add user\n2. View users\n3. Add skills")
    choice = input("Choice: ")
    if choice == "1":
        add_user()
    elif choice == "2":
        get_users()
    elif choice == "3":
        user_id = int(input("Enter user ID: "))
        skill_type = input("Type ('has' or 'wants'): ")
        add_skills(user_id, skill_type)

#TODO NEXT: matching logic -- have to create new file - matcher.py