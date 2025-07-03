import sqlite3
from database import init_db
from matcher import match_users_by_skills, view_matches_for_user

def signup():
    name  = input("Name: ").strip()
    email = input("Email: ").strip()
    if not name or not email:
        print("Name and email cannot be empty.")
        return None

    conn = sqlite3.connect('mentorship.db')
    c    = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        uid = c.lastrowid
        print(f"✔ Signed up! Your user ID is {uid}")
        return uid, email
    except sqlite3.IntegrityError:
        print("✖ That email is already registered.")
        return None
    finally:
        conn.close()

def login():
    email = input("Email: ").strip()
    conn  = sqlite3.connect('mentorship.db')
    c     = conn.cursor()
    c.execute("SELECT id, name FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()

    if row:
        uid, name = row
        print(f"✔ Welcome back, {name} (ID: {uid})")
        return uid, email
    else:
        print("✖ No account found with that email.")
        return None

def add_skill_cli(current_id):
    stype = input("Are you adding a skill to 'teach' or 'learn'? ").lower()
    if stype not in ('teach','learn'):
        print("Please type exactly 'teach' or 'learn'.")
        return

    skill = input(f"Enter the skill to {('teach' if stype=='teach' else 'learn')}: ").strip().lower()
    if not skill:
        print("Skill cannot be blank.")
        return

    conn = sqlite3.connect('mentorship.db')
    c    = conn.cursor()
    c.execute("INSERT INTO skills (user_id, skill, type) VALUES (?, ?, ?)",
              (current_id, skill, stype))
    conn.commit()
    conn.close()

    print(f"✔ Skill '{skill}' saved as '{stype}'.")
    created = match_users_by_skills()
    if created:
        print(f"✔ {created} match(es) generated.")

def view_my_skills(current_id):
    conn = sqlite3.connect('mentorship.db')
    c    = conn.cursor()
    c.execute("SELECT skill, type FROM skills WHERE user_id = ?", (current_id,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("You haven’t added any skills yet.")
    else:
        print("\nYour Skills:")
        for skill, stype in rows:
            tag = "Teach" if stype=='teach' else "Learn"
            print(f"  • {skill}  ({tag})")

def view_my_matches(current_id):
    conn = sqlite3.connect('mentorship.db')
    c    = conn.cursor()
    c.execute('''
        SELECT u2.name, m.score
        FROM matches m
        JOIN users u2 ON 
            (m.mentor_id = ? AND m.mentee_id = u2.id)
         OR (m.mentee_id = ? AND m.mentor_id = u2.id)
    ''', (current_id, current_id))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No matches found yet. Try adding some skills!")
    else:
        print("\nYour Matches:")
        for name, score in rows:
            print(f"  • {name}  (Score: {score})")

def main():
    init_db()
    print("Welcome to Mentorship Matching Platform!  Sign up or log in to continue.\n")

    # --- signup/login loop ---
    user = None
    while not user:
        choice = input("1) Sign up   2) Log in   3) Exit  > ").strip()
        if choice == "1":
            user = signup()
        elif choice == "2":
            user = login()
        elif choice == "3":
            print("Goodbye."); return
        else:
            print("Invalid choice.")

    current_id, _ = user

    # --- main menu ---
    while True:
        print("\nWhat would you like to do?")
        print("1) Add a skill")
        print("2) View my skills")
        print("3) View my matches")
        print("4) Logout / Exit")
        cmd = input("> ").strip()

        if cmd == "1":
            add_skill_cli(current_id)
        elif cmd == "2":
            view_my_skills(current_id)
        elif cmd == "3":
            view_my_matches(current_id)
        elif cmd in ("4", "exit", "logout"):
            print("See you next time.")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
