import sqlite3
from models import User
from matcher import match_users_by_skills, view_matches_for_user

def signup():
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    if not name or not email:
        print("Name and email cannot be empty.")
        return None

    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        uid = c.lastrowid
        print(f"✔ Signed up! Your user ID is {uid}")
        # Return a User object here
        return User(uid, name, email)
    except sqlite3.IntegrityError:
        print("✖ That email is already registered.")
        return None
    finally:
        conn.close()

def login():
    email = input("Email: ").strip()
    conn = sqlite3.connect('mentorship.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()

    if row:
        uid, name = row
        print(f"✔ Welcome back, {name} (ID: {uid})")
        # Return a User object
        return User(uid, name, email)
    else:
        print("✖ No account found with that email.")
        return None

def main():
    from database import init_db
    init_db()
    print("Welcome to Mentorship Matching Platform! Sign up or log in to continue.\n")

    # --- signup/login loop ---
    user = None
    while not user:
        choice = input("1) Sign up   2) Log in   3) Exit  > ").strip()
        if choice == "1":
            user = signup()
        elif choice == "2":
            user = login()
        elif choice == "3":
            print("Goodbye.")
            return
        else:
            print("Invalid choice.")

    # --- main menu using User methods ---
    while True:
        print("\nWhat would you like to do?")
        print("1) Add a skill")
        print("2) View my skills")
        print("3) View my matches")
        print("4) Logout / Exit")
        cmd = input("> ").strip()

        if cmd == "1":
            stype = input("Are you adding a skill to 'teach' or 'learn'? ").lower().strip()
            if stype not in ('teach', 'learn'):
                print("Please type exactly 'teach' or 'learn'.")
                continue
            skill = input(f"Enter the skill to {stype}: ").strip()
            if not skill:
                print("Skill cannot be blank.")
                continue
            user.add_skill(skill, stype)
            print(f"✔ Skill '{skill}' saved as '{stype}'.")
            created = match_users_by_skills()
            if created:
                print(f"✔ {created} match(es) generated.")
        elif cmd == "2":
            skills = user.get_skills()
            if not skills:
                print("You haven’t added any skills yet.")
            else:
                print("\nYour Skills:")
                for skill, stype in skills:
                    tag = "Teach" if stype == 'teach' else "Learn"
                    print(f"  • {skill}  ({tag})")
        elif cmd == "3":
            matches = user.get_matches()
            if not matches:
                print("No matches found yet. Try adding some skills!")
            else:
                print("\nYour Matches:")
                for name, score in matches:
                    print(f"  • {name}  (Score: {score})")
        elif cmd in ("4", "exit", "logout"):
            print("See you next time.")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
